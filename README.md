# md2cv

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Markdown to CV/resume converter with auto-fit PDF generation.

Write your CV in Markdown, get a professionally styled PDF that automatically fits on a single page.

## Quick Start

**Prerequisites:** Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (it will manage Python automatically):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**1. Install system dependencies** (required by WeasyPrint for PDF rendering):

```bash
# Ubuntu/Debian
sudo apt install libpango1.0-dev libcairo2-dev libgdk-pixbuf2.0-dev

# macOS
brew install pango cairo gdk-pixbuf

# Fedora
sudo dnf install pango-devel cairo-devel gdk-pixbuf2-devel
```

**2. Clone and install:**

```bash
git clone https://github.com/zhuoyuan-liu/md2cv.git
cd md2cv
uv sync
```

**3. Generate your CV:**

```bash
uv run md2cv resume.md -o resume.pdf
```

## Usage

```bash
# Generate PDF (auto-fit to 1 page)
uv run md2cv resume.md -o resume.pdf

# Generate both PDF and HTML
uv run md2cv resume.md -o resume.pdf --html

# Generate HTML only
uv run md2cv resume.md --html-only

# Use letter page size instead of A4
uv run md2cv resume.md --page-size letter

# Include a portrait photo
uv run md2cv resume.md --photo headshot.jpg

# Disable auto-fit (allow multi-page output)
uv run md2cv resume.md --no-auto-fit
```

## Markdown Format

```markdown
# Your Name

**Your Title**

- **Phone:** +1-555-0100
- **Email:** you@example.com
- **LinkedIn:** [linkedin.com/in/you](https://linkedin.com/in/you)
- **GitHub:** [github.com/you](https://github.com/you)

---

## About Me

A short summary paragraph about yourself.

---

## Experience

### Job Title | Start Date --- End Date
**Company Name** | Location

- Achievement or responsibility
- Another bullet point

## Education

**Degree** | Year --- Year
University Name | GPA: 3.8/4.0

## Skills

- Python, Go, TypeScript
- Docker, Kubernetes, AWS
```

See [`examples/example_cv.md`](examples/example_cv.md) for a full example.

### Structure rules

- `# Heading 1` — your name
- Bold paragraph after `#` — subtitle/title
- Bullet list with `**Label:**` — contact info
- `## Heading 2` — section headings (Experience, Education, Skills, etc.)
- `### Heading 3` with `| Date` — entry titles with date range (use `---` for date separator)
- `**Bold text**` after H3 — organization and location
- Bullet lists after entries — details/achievements
- Sections without entries render as free-form content (e.g., Skills)

## Themes

md2cv ships with two built-in themes:

- **professional** (default) — clean, professional layout with a modern feel
- **modern** — modern layout with photo support, subtitle, and accent headings

Select a theme with `--theme`:

```bash
uv run md2cv resume.md -o resume.pdf --theme modern
```

## Auto-Fit

md2cv automatically adjusts font sizes, margins, and spacing to fit your CV on a single page. If content still overflows at minimum scale, it produces a multi-page PDF with a warning.

## Development

```bash
uv sync
uv run pytest tests/ -v --cov=md2cv
```

## License

[MIT](LICENSE)
