"""CLI entry point for md2cv."""

from __future__ import annotations

from pathlib import Path

import click

from md2cv import __version__


@click.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False),
    default=None,
    help="Output file path (default: <input_stem>.pdf)",
)
@click.option(
    "--html",
    "emit_html",
    is_flag=True,
    help="Also produce an HTML file alongside the PDF.",
)
@click.option(
    "--html-only",
    is_flag=True,
    help="Produce only HTML output, skip PDF generation.",
)
@click.option(
    "--page-size",
    type=click.Choice(["a4", "letter"], case_sensitive=False),
    default="a4",
    help="Page size for PDF output.",
)
@click.option(
    "--no-auto-fit",
    is_flag=True,
    help="Disable auto-shrink to fit content on one page.",
)
@click.option(
    "--photo",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Path to a portrait photo (JPEG/PNG) to embed in the CV.",
)
@click.option(
    "--theme",
    default="professional",
    help="Theme to use for rendering.",
)
@click.version_option(version=__version__)
def main(
    input_file: str,
    output: str | None,
    emit_html: bool,
    html_only: bool,
    page_size: str,
    no_auto_fit: bool,
    photo: str | None,
    theme: str,
) -> None:
    """Convert a Markdown CV/resume to PDF or HTML.

    INPUT_FILE is the path to a Markdown (.md) file containing your CV.
    """
    from md2cv.parser import parse_cv
    from md2cv.pdf import generate_pdf
    from md2cv.renderer import render_html

    input_path = Path(input_file)
    markdown_text = input_path.read_text(encoding="utf-8")

    # Parse
    cv = parse_cv(markdown_text)

    # Attach photo if provided
    if photo:
        cv.photo_path = photo

    # Determine output path
    if output:
        out = Path(output)
    else:
        suffix = ".html" if html_only else ".pdf"
        out = input_path.with_suffix(suffix)

    # Generate outputs
    if html_only:
        html_str = render_html(cv, theme_name=theme)
        html_path = out.with_suffix(".html")
        html_path.write_text(html_str, encoding="utf-8")
        click.echo(f"HTML written to {html_path}")
    else:
        pdf_path = out.with_suffix(".pdf")
        generate_pdf(
            cv,
            output_path=pdf_path,
            page_size=page_size,
            auto_fit=not no_auto_fit,
            theme_name=theme,
        )
        click.echo(f"PDF written to {pdf_path}")

        if emit_html:
            html_str = render_html(cv, theme_name=theme)
            html_path = out.with_suffix(".html")
            html_path.write_text(html_str, encoding="utf-8")
            click.echo(f"HTML written to {html_path}")
