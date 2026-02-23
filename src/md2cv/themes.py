"""Theme registry: discover, load, and list themes."""

from __future__ import annotations

import tomllib
from dataclasses import fields
from importlib import resources
from typing import NamedTuple

from md2cv.models import StyleParams

_TEMPLATES_PKG = "md2cv.templates"


class Theme(NamedTuple):
    """A loaded theme with its template and default style."""

    name: str
    display_name: str
    description: str
    template_string: str
    default_style: StyleParams


def list_themes() -> list[str]:
    """List available theme names by scanning the templates package."""
    names: list[str] = []
    templates = resources.files(_TEMPLATES_PKG)
    for item in templates.iterdir():
        if item.is_dir() and (item / "template.html").is_file():
            names.append(item.name)
    return sorted(names)


def get_theme(name: str) -> Theme:
    """Load a theme by name from templates/<name>/."""
    theme_dir = resources.files(_TEMPLATES_PKG) / name
    template_path = theme_dir / "template.html"
    toml_path = theme_dir / "theme.toml"

    if not template_path.is_file():
        available = list_themes()
        raise ValueError(
            f"Theme '{name}' not found. Available themes: {', '.join(available)}"
        )

    template_string = template_path.read_text(encoding="utf-8")
    style = StyleParams()

    if toml_path.is_file():
        data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
        meta = data.get("meta", {})
        style_data = data.get("style", {})
        valid_fields = {f.name for f in fields(StyleParams)}
        filtered = {k: v for k, v in style_data.items() if k in valid_fields}
        style = StyleParams(**filtered)
    else:
        meta = {}

    return Theme(
        name=name,
        display_name=meta.get("display_name", name.title()),
        description=meta.get("description", ""),
        template_string=template_string,
        default_style=style,
    )
