---
name: tailor-cv
description: "Tailor a CV/resume for a specific job application. Accepts a job description (pasted text or URL), extracts company and role, creates an application folder, generates a tailored CV.md from a full CV, and converts to PDF via md2cv."
---

# Tailor CV for Job Application

Generate a tailored, 1-2 page CV from a detailed full CV, targeted at a specific job description. Creates an organized application folder with the JD, tailored CV markdown, and rendered PDF.

## Prerequisites

The user's full CV must be placed at `cv/cv.md` in the md2cv project root. This file is gitignored and never committed.

**If `cv/cv.md` does not exist, stop immediately and ask the user to provide their full CV in markdown format at `cv/cv.md` before continuing.** Do not proceed without it.

Ensure md2cv is installed: run `uv sync` in the md2cv project directory if needed.

## Workflow

### Step 1: Receive the Job Description

The user provides the JD in one of two ways:

- **Pasted text**: The user pastes the full JD directly in the conversation.
- **URL**: The user provides a URL. Use WebFetch to retrieve and extract the full job description text. If the URL fails or returns unusable content, ask the user to paste the JD text manually.

### Step 2: Extract Company Name and Role Title

Read the JD text and extract:
- **Company name**: The hiring company.
- **Role title**: The specific position title.

If either is ambiguous, missing, or unclear from the JD text, **ask the user** to confirm or provide the values before continuing. Do not guess.

### Step 3: Create Application Folder

Sanitize the company name and role title for use as a folder name:
- Remove all punctuation except hyphens.
- Use PascalCase for each word (e.g., "Senior Software Engineer" becomes "SeniorSoftwareEngineer").
- Strip leading/trailing hyphens and collapse consecutive hyphens.

Get today's date using `date +%Y-%m-%d`.

Create the folder:
```bash
mkdir -p applications/YYYY-MM-DD-CompanyName-RoleTitle/
```

Example: `applications/2026-02-23-AcmeCorp-SeniorSoftwareEngineer/`

If a folder with the same name already exists, append `-2`, `-3`, etc.

### Step 4: Save the Job Description

Write the JD to `jd.md` in the application folder with a metadata header:

```markdown
# Job Description

- **Company:** [Company Name]
- **Role:** [Role Title]
- **Source:** [URL or "Pasted by user"]
- **Date:** [YYYY-MM-DD]

---

[Full JD text here, preserving original formatting]
```

### Step 5: Read the Full CV

Read `cv/cv.md`. If the file does not exist, **stop and ask the user** to place their full CV at `cv/cv.md` in markdown format. Do not proceed without it.

### Step 6: Generate Tailored CV

With both the full CV and JD in context, generate a tailored `cv.md` that:

1. **Follows the md2cv markdown format exactly** — see [cv-markdown-format.md](references/cv-markdown-format.md) for the format specification.
2. **Selects and prioritizes content** based on the JD — see [tailoring-guidelines.md](references/tailoring-guidelines.md) for the detailed tailoring strategy.
3. **Targets 1-2 pages** when rendered to PDF (~40-80 lines for 1 page, ~80-140 lines for 2 pages).
4. **Preserves the same markdown format** as the full CV (H3-based or bold-paragraph entries).
5. **Never fabricates** experience or skills not in the full CV.

Write the tailored CV to `applications/<folder>/cv.md`.

### Step 7: Generate PDF

Convert the tailored CV to PDF:

```bash
cd <md2cv-project-root> && uv run md2cv applications/<folder>/cv.md -o applications/<folder>/cv.pdf
```

If the command fails, report the error. Common issues:
- Run `uv sync` to install dependencies.
- WeasyPrint requires system libs (pango, cairo, gdk-pixbuf).

### Step 8: Report Results

Tell the user:
1. The application folder path and its contents (`jd.md`, `cv.md`, `cv.pdf`).
2. A brief summary of tailoring decisions: which sections were kept, what was emphasized, what was dropped or compressed.
3. Suggest the user review `cv.md` and `cv.pdf` before submitting.

## Edge Cases

- **Full CV not found at `cv/cv.md`**: Stop and ask the user to provide their full CV at `cv/cv.md`. Do not proceed.
- **JD URL fails**: Ask the user to paste the JD text instead.
- **Company/role ambiguous**: Ask the user to confirm before creating the folder.
- **Duplicate folder**: Append a numeric suffix (`-2`, `-3`).
- **md2cv fails**: Display the error and suggest running `uv sync`.
- **Full CV too short** (< 10 lines): Warn the user that the tailored CV may lack detail.
- **Generated CV exceeds 2 pages**: Trim content further and re-generate the PDF.
