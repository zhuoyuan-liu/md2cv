"""PDF generation with auto-fit binary search."""

from __future__ import annotations

import logging
from dataclasses import replace
from pathlib import Path

from md2cv.models import CVData, StyleParams
from md2cv.renderer import render_html
from md2cv.themes import Theme, get_theme

logger = logging.getLogger(__name__)

# Auto-fit binary search parameters
MIN_SCALE = 0.65
MAX_ITERATIONS = 12
CONVERGENCE_THRESHOLD = 0.005


def _scale_params(base: StyleParams, factor: float) -> StyleParams:
    """Scale style parameters by a factor.

    Font sizes scale linearly. Margins and line height shrink more slowly.
    """
    margin_factor = 0.5 + 0.5 * factor
    line_height_factor = 0.85 + 0.15 * factor

    return replace(
        base,
        base_font_size=base.base_font_size * factor,
        heading_font_size=base.heading_font_size * factor,
        name_font_size=base.name_font_size * factor,
        contact_font_size=base.contact_font_size * factor,
        margin_top=base.margin_top * margin_factor,
        margin_bottom=base.margin_bottom * margin_factor,
        margin_left=base.margin_left * margin_factor,
        margin_right=base.margin_right * margin_factor,
        line_height=base.line_height * line_height_factor,
        section_gap=base.section_gap * factor,
        entry_gap=base.entry_gap * factor,
        detail_gap=base.detail_gap * factor,
    )


def _render_and_count_pages(
    cv: CVData,
    style: StyleParams,
    theme: Theme,
) -> tuple[bytes, int]:
    """Render CV to PDF bytes and return (pdf_bytes, page_count)."""
    from weasyprint import HTML

    html_str = render_html(cv, style=style, theme=theme)
    doc = HTML(string=html_str).render()
    page_count = len(doc.pages)
    pdf_bytes = doc.write_pdf()
    return pdf_bytes, page_count


def generate_pdf(
    cv: CVData,
    output_path: str | Path,
    page_size: str = "a4",
    auto_fit: bool = True,
    theme_name: str = "professional",
) -> Path:
    """Generate a PDF from CVData with optional auto-fit.

    Args:
        cv: Parsed CV data.
        output_path: Where to write the PDF.
        page_size: Page size ('a4' or 'letter').
        auto_fit: Whether to auto-shrink to fit one page.
        theme_name: Theme to use.

    Returns:
        Path to the generated PDF file.
    """
    output_path = Path(output_path)
    theme = get_theme(theme_name)
    base_style = theme.default_style

    # Set page dimensions
    if page_size.lower() == "letter":
        base_style = replace(base_style, page_width="8.5in", page_height="11in")

    # First render at full scale
    pdf_bytes, page_count = _render_and_count_pages(cv, base_style, theme)

    if page_count <= 1 or not auto_fit:
        output_path.write_bytes(pdf_bytes)
        return output_path

    # Binary search for largest scale factor that fits on one page
    lo, hi = MIN_SCALE, 1.0
    best_pdf = pdf_bytes
    best_factor = 1.0

    for _ in range(MAX_ITERATIONS):
        mid = (lo + hi) / 2
        scaled_style = _scale_params(base_style, mid)
        pdf_bytes, pages = _render_and_count_pages(cv, scaled_style, theme)

        if pages <= 1:
            best_pdf = pdf_bytes
            best_factor = mid
            lo = mid
        else:
            hi = mid

        if hi - lo < CONVERGENCE_THRESHOLD:
            break

    if best_factor < 1.0:
        # Check if min scale still overflows
        min_style = _scale_params(base_style, MIN_SCALE)
        _, min_pages = _render_and_count_pages(cv, min_style, theme)
        if min_pages > 1:
            logger.warning(
                "Content overflows even at minimum scale. "
                "Producing multi-page PDF."
            )
            best_pdf = _render_and_count_pages(cv, min_style, theme)[0]

    output_path.write_bytes(best_pdf)
    return output_path
