"""Markdown parser: converts markdown CV to CVData model."""

from __future__ import annotations

import html
import re

import mistune

from md2cv.models import CVData, CVEntry, CVSection, ContactInfo


def parse_cv(markdown_text: str) -> CVData:
    """Parse a markdown CV into structured CVData."""
    md = mistune.create_markdown(renderer="ast")
    tokens = md(markdown_text)
    return _walk_tokens(tokens)


def _walk_tokens(tokens: list[dict]) -> CVData:
    """Walk AST tokens and extract CV structure."""
    cv = CVData()
    i = 0

    # Find h1 → name
    while i < len(tokens):
        tok = tokens[i]
        if tok["type"] == "heading" and tok["attrs"]["level"] == 1:
            cv.name = _extract_text(tok["children"])
            i += 1
            break
        i += 1

    # After h1: look for optional subtitle (bold paragraph, no "|") then contact
    # (pipe-delimited paragraph or bullet list).
    while i < len(tokens):
        tok = tokens[i]
        t = tok["type"]

        if t in ("blank_line", "thematic_break"):
            i += 1
            continue

        if t == "heading":
            break

        if t == "paragraph":
            text = _extract_text(tok["children"])
            if not cv.subtitle and _has_bold(tok["children"]) and "|" not in text:
                # Bold-only paragraph with no pipe → subtitle
                cv.subtitle = text.strip()
                i += 1
                continue
            else:
                # Pipe-delimited contact paragraph (existing format)
                cv.contact = ContactInfo(
                    items=[item.strip() for item in text.split("|") if item.strip()]
                )
                i += 1
                break

        if t == "list":
            # Contact as bullet list (CV.md format)
            cv.contact = ContactInfo(items=_extract_list_items(tok))
            i += 1
            break

        i += 1

    # Remaining tokens: h2 headings → sections
    while i < len(tokens):
        tok = tokens[i]
        if tok["type"] == "heading" and tok["attrs"]["level"] == 2:
            heading = _extract_text(tok["children"])
            i += 1
            # Collect tokens until next h2 or end
            section_tokens = []
            while i < len(tokens):
                if tokens[i]["type"] == "heading" and tokens[i]["attrs"]["level"] <= 2:
                    break
                section_tokens.append(tokens[i])
                i += 1
            section = _parse_section(heading, section_tokens)
            cv.sections.append(section)
        else:
            i += 1

    return cv


def _parse_section(heading: str, tokens: list[dict]) -> CVSection:
    """Parse section tokens into a CVSection with structured entries or raw HTML."""
    # Try H3-based entries first (CV.md format)
    entries = _try_parse_h3_entries(tokens)
    if entries:
        return CVSection(heading=heading, entries=entries)

    # Try bold-paragraph entries (existing format)
    entries = _try_parse_entries(tokens)
    if entries:
        return CVSection(heading=heading, entries=entries)

    # Fallback: render as raw HTML
    raw = _tokens_to_html(tokens)
    return CVSection(heading=heading, raw_html=raw)


def _try_parse_h3_entries(tokens: list[dict]) -> list[CVEntry]:
    """Try to parse tokens as H3-based CVEntry items.

    Handles CV.md format: ### Title | Date, **Org**, **Skills:** tags, - bullets.
    """
    # Quick check: must have at least one h3
    if not any(
        t["type"] == "heading" and t["attrs"].get("level") == 3 for t in tokens
    ):
        return []

    entries: list[CVEntry] = []
    current: CVEntry | None = None
    i = 0

    while i < len(tokens):
        tok = tokens[i]
        t = tok["type"]

        if t in ("blank_line", "thematic_break"):
            i += 1
            continue

        if t == "heading" and tok["attrs"].get("level") == 3:
            if current is not None:
                entries.append(current)
            heading_text = _extract_text(tok["children"])
            parts = [p.strip() for p in heading_text.split("|")]
            current = CVEntry(title=parts[0].strip())
            if len(parts) >= 2:
                current.date_range = parts[1].strip()
            i += 1
            continue

        if t == "paragraph" and current is not None:
            if _has_bold(tok["children"]):
                first_strong = _get_first_strong_text(tok["children"])
                if first_strong.endswith(":"):
                    # Tags line: e.g., **Skills:** Go, OpenTelemetry, ...
                    full_text = _extract_text(tok["children"])
                    colon_idx = full_text.find(":")
                    current.tags = (
                        full_text[colon_idx + 1:].strip() if colon_idx >= 0 else full_text
                    )
                else:
                    # Organization line: e.g., **Acme Corp** | New York
                    full_text = _extract_text(tok["children"])
                    parts = [p.strip() for p in full_text.split("|") if p.strip()]
                    current.organization = ", ".join(parts)
            else:
                # Plain paragraph: description text
                current.description = _extract_text(tok["children"]).strip()
            i += 1
            continue

        if t == "list" and current is not None:
            current.details = _extract_list_items(tok)
            i += 1
            continue

        # Any other token: skip
        i += 1

    if current is not None:
        entries.append(current)

    return entries


def _try_parse_entries(tokens: list[dict]) -> list[CVEntry]:
    """Try to parse tokens as structured CVEntry items.

    Looks for pattern: paragraph with **bold** (optionally with | separators)
    followed by optional bullet list.
    """
    entries: list[CVEntry] = []
    i = 0

    while i < len(tokens):
        tok = tokens[i]
        # Skip blank_line tokens
        if tok["type"] == "blank_line":
            i += 1
            continue
        if tok["type"] == "paragraph" and _has_bold(tok["children"]):
            entry = _parse_entry_header(tok["children"])
            i += 1
            # Skip blank lines before list
            while i < len(tokens) and tokens[i]["type"] == "blank_line":
                i += 1
            # Check for following list
            if i < len(tokens) and tokens[i]["type"] == "list":
                entry.details = _extract_list_items(tokens[i])
                i += 1
            entries.append(entry)
        else:
            # Not a structured entry pattern — bail out
            if entries:
                return entries
            return []
    return entries


def _has_bold(children: list[dict]) -> bool:
    """Check if children contain a bold/strong element."""
    for child in children:
        if child["type"] == "strong":
            return True
    return False


def _get_first_strong_text(children: list[dict]) -> str:
    """Get text of the first strong element in children."""
    for child in children:
        if child["type"] == "strong":
            return _extract_text(child["children"])
    return ""


def _parse_entry_header(children: list[dict]) -> CVEntry:
    """Parse a paragraph with bold text into a CVEntry header.

    Supports formats:
    - **Title**
    - **Title** | Organization | Date Range
    - **Title** | Date Range
    - **Title** | Date Range (softbreak) Organization | Detail
    """
    entry = CVEntry()

    # Split children at softbreak (for multi-line education entries)
    first_line: list[dict] = []
    second_line: list[dict] = []
    in_second = False
    for child in children:
        if child["type"] == "softbreak":
            in_second = True
            continue
        if in_second:
            second_line.append(child)
        else:
            first_line.append(child)

    # Parse first line: bold title + pipe-separated org/date
    parts: list[str] = []
    for child in first_line:
        if child["type"] == "strong":
            entry.title = _extract_text(child["children"])
        parts.append(_extract_text_from_node(child))

    full_text = "".join(parts)

    # Find everything after the bold title
    title_end = full_text.find(entry.title) + len(entry.title)
    remainder = full_text[title_end:].strip()

    if remainder.startswith("|"):
        remainder = remainder[1:]

    segments = [s.strip() for s in remainder.split("|") if s.strip()]

    if len(segments) >= 2:
        entry.organization = segments[0]
        entry.date_range = segments[1]
    elif len(segments) == 1:
        # Could be org or date — heuristic: if it contains digits, it's a date
        seg = segments[0]
        if re.search(r"\d", seg):
            entry.date_range = seg
        else:
            entry.organization = seg

    # Parse second line (softbreak case): organization | additional info from second line
    if second_line and not entry.organization:
        second_text = _extract_text(second_line)
        parts = [p.strip() for p in second_text.split("|") if p.strip()]
        if parts:
            entry.organization = ", ".join(parts)

    return entry


def _extract_list_items(list_token: dict) -> list[str]:
    """Extract text from list items."""
    items: list[str] = []
    for li in list_token["children"]:
        if li["type"] == "list_item":
            text_parts = []
            for child in li["children"]:
                text_parts.append(_extract_text(child.get("children", [])))
            items.append(" ".join(text_parts).strip())
    return items


def _extract_text(children: list[dict]) -> str:
    """Recursively extract plain text from AST children."""
    parts: list[str] = []
    for child in children:
        parts.append(_extract_text_from_node(child))
    return "".join(parts)


def _extract_text_from_node(node: dict) -> str:
    """Extract text from a single AST node."""
    if node["type"] == "text":
        return node.get("raw", node.get("text", ""))
    if node["type"] == "codespan":
        return node.get("raw", node.get("text", ""))
    if node["type"] in ("strong", "emphasis"):
        return _extract_text(node["children"])
    if node["type"] == "link":
        return _extract_text(node["children"])
    if node["type"] == "softbreak":
        return " "
    if "children" in node and node["children"]:
        return _extract_text(node["children"])
    return node.get("raw", node.get("text", ""))


def _tokens_to_html(tokens: list[dict]) -> str:
    """Render AST tokens to simple HTML for raw_html fallback."""
    md_renderer = mistune.create_markdown()
    # Re-render by reconstructing markdown and parsing with default renderer
    # Simpler: directly walk and produce HTML
    parts: list[str] = []
    for tok in tokens:
        parts.append(_token_to_html(tok))
    return "\n".join(parts)


def _token_to_html(tok: dict) -> str:
    """Convert a single AST token to HTML."""
    t = tok["type"]
    if t == "paragraph":
        inner = _children_to_html(tok.get("children", []))
        return f"<p>{inner}</p>"
    if t == "list":
        tag = "ul" if not tok["attrs"].get("ordered") else "ol"
        items = []
        for li in tok["children"]:
            li_inner_parts = []
            for child in li.get("children", []):
                if child["type"] in ("paragraph", "block_text"):
                    li_inner_parts.append(_children_to_html(child.get("children", [])))
                elif child["type"] == "list":
                    li_inner_parts.append(_token_to_html(child))
                else:
                    li_inner_parts.append(_children_to_html([child]))
            items.append(f"<li>{''.join(li_inner_parts)}</li>")
        return f"<{tag}>{''.join(items)}</{tag}>"
    if t == "heading":
        level = tok["attrs"]["level"]
        inner = _children_to_html(tok.get("children", []))
        return f"<h{level}>{inner}</h{level}>"
    if t == "block_code":
        raw = tok.get("raw", tok.get("text", ""))
        return f"<pre><code>{_escape_html(raw)}</code></pre>"
    return ""


def _children_to_html(children: list[dict]) -> str:
    """Convert AST children nodes to inline HTML."""
    parts: list[str] = []
    for node in children:
        t = node["type"]
        if t == "text":
            parts.append(_escape_html(node.get("raw", node.get("text", ""))))
        elif t == "strong":
            inner = _children_to_html(node["children"])
            parts.append(f"<strong>{inner}</strong>")
        elif t == "emphasis":
            inner = _children_to_html(node["children"])
            parts.append(f"<em>{inner}</em>")
        elif t == "codespan":
            raw = node.get("raw", node.get("text", ""))
            parts.append(f"<code>{_escape_html(raw)}</code>")
        elif t == "link":
            href = node["attrs"].get("url", node.get("link", ""))
            inner = _children_to_html(node["children"])
            parts.append(f'<a href="{_escape_html(href)}">{inner}</a>')
        elif t == "softbreak":
            parts.append(" ")
        elif t == "linebreak":
            parts.append("<br>")
        else:
            parts.append(_extract_text_from_node(node))
    return "".join(parts)


def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(text, quote=True)
