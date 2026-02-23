# md2cv — Development Guide

## Build & Run

```bash
uv sync                                          # install deps
uv run md2cv examples/example_cv.md -o out.pdf   # run CLI
uv run pytest tests/ -v --cov=md2cv              # run tests with coverage
```

## Architecture

```
Markdown → Parser (mistune AST) → CVData model → Renderer (Jinja2) → PDF (WeasyPrint)
```

- `src/md2cv/models.py` — dataclasses: CVData, CVSection, CVEntry, StyleParams
- `src/md2cv/parser.py` — markdown to CVData using mistune AST walker
- `src/md2cv/renderer.py` — CVData + StyleParams → HTML via Jinja2
- `src/md2cv/pdf.py` — HTML → PDF with auto-fit binary search
- `src/md2cv/cli.py` — Click CLI entry point
- `src/md2cv/themes.py` — theme discovery and loading
- `src/md2cv/templates/<theme>/` — theme folders with template.html + theme.toml

## Adding a Theme

Create `src/md2cv/templates/<name>/` with:
- `template.html` — Jinja2 template receiving `cv`, `style`, `photo`, `photo_mime`
- `theme.toml` — `[meta]` (display_name, description) + `[style]` (StyleParams defaults)

## Key Conventions

- Python >=3.12, managed with uv
- Tests in `tests/`, fixtures in `tests/fixtures/`
- WeasyPrint requires system libs: pango, cairo, gdk-pixbuf
