"""Renderer: CVData + StyleParams → HTML string via Jinja2."""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

from jinja2 import Environment

from md2cv.models import CVData, StyleParams
from md2cv.themes import Theme, get_theme


def render_html(
    cv: CVData,
    style: StyleParams | None = None,
    theme: Theme | None = None,
    theme_name: str = "professional",
) -> str:
    """Render CVData to a self-contained HTML string.

    Args:
        cv: Parsed CV data.
        style: Style parameters (overrides theme defaults if provided).
        theme: Pre-loaded theme (if None, loads by theme_name).
        theme_name: Theme to load if theme is not provided.

    Returns:
        Complete HTML string with inline CSS and embedded assets.
    """
    if theme is None:
        theme = get_theme(theme_name)
    if style is None:
        style = theme.default_style

    # Handle photo embedding
    photo_b64 = None
    photo_mime = None
    if cv.photo_path:
        photo_path = Path(cv.photo_path)
        if photo_path.is_file():
            photo_b64 = base64.b64encode(photo_path.read_bytes()).decode("ascii")
            mime, _ = mimetypes.guess_type(str(photo_path))
            photo_mime = mime or "image/jpeg"

    env = Environment(autoescape=False)
    template = env.from_string(theme.template_string)

    return template.render(
        cv=cv,
        style=style,
        photo=photo_b64,
        photo_mime=photo_mime,
    )
