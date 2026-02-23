"""Data models for md2cv."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ContactInfo:
    """Parsed contact items from the CV header."""

    items: list[str] = field(default_factory=list)


@dataclass
class CVEntry:
    """A structured entry within a CV section.

    Examples: job position, education degree, project.
    """

    title: str = ""
    organization: str = ""
    date_range: str = ""
    description: str = ""
    tags: str = ""
    details: list[str] = field(default_factory=list)


@dataclass
class CVSection:
    """A section of the CV (e.g., Experience, Education)."""

    heading: str = ""
    entries: list[CVEntry] = field(default_factory=list)
    raw_html: str = ""


@dataclass
class CVData:
    """Complete parsed CV data."""

    name: str = ""
    subtitle: str = ""
    contact: ContactInfo = field(default_factory=ContactInfo)
    photo_path: str | None = None
    sections: list[CVSection] = field(default_factory=list)


@dataclass
class StyleParams:
    """All adjustable CSS values for rendering."""

    base_font_size: float = 10.0
    heading_font_size: float = 14.0
    name_font_size: float = 22.0
    contact_font_size: float = 9.0
    margin_top: float = 15.0
    margin_bottom: float = 15.0
    margin_left: float = 18.0
    margin_right: float = 18.0
    line_height: float = 1.35
    section_gap: float = 8.0
    entry_gap: float = 5.0
    detail_gap: float = 2.0
    page_width: str = "210mm"
    page_height: str = "297mm"
