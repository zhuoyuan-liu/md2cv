# md2cv Markdown Format Reference

The generated `cv.md` **must** follow this format exactly for md2cv to parse it correctly.

## Header

```markdown
# Full Name

**Job Title or Subtitle**

- **Phone:** +1-555-0100
- **Email:** you@example.com
- **LinkedIn:** [linkedin.com/in/you](https://linkedin.com/in/you)
- **GitHub:** [github.com/you](https://github.com/you)
- **Address:** City, State, Country
```

Rules:
- `# H1` is the person's name (exactly one H1, required).
- An optional **bold paragraph** immediately after H1 is the subtitle/title.
- Contact info is a **bullet list** with `**Label:** value` items. Links are supported.
- Alternative contact format: a single pipe-delimited paragraph (`email | phone | location`).

## Section Headings

```markdown
---

## Experience
```

- `## H2` starts a new section (Experience, Education, Skills, About Me, etc.).
- `---` horizontal rules are optional visual separators (the parser ignores them).

## Structured Entries (H3 Format)

Use this format for Experience, Education, and similar sections:

```markdown
### Job Title | Start Date --- End Date
**Company Name** | Location

Optional description paragraph.

**Skills:** Python, Go, Kubernetes

- Achievement or responsibility bullet
- Another bullet point
- Yet another bullet
```

Rules:
- `### H3` contains the entry title. Use `|` to separate title from date range.
- Use `---` (three hyphens) as the date separator within date ranges (rendered as en-dash).
- `**Bold text**` on the line after H3 is the organization. Use `|` to separate org from location.
- An optional plain paragraph after the org line is the description.
- An optional `**Skills:**` or `**Tags:**` line provides tags.
- Bullet list items are the detail points.

## Structured Entries (Bold-Paragraph Format)

Alternative format (also supported):

```markdown
**Degree Name** | Start --- End
University Name | GPA: 3.8/4.0

- Relevant coursework or achievement
```

Rules:
- `**Bold text**` starts the entry. Use `|` to separate fields (title, org, date in any order).
- Bullet list items follow as details.

## Free-Form Sections

For sections like Skills that don't have structured entries:

```markdown
## Skills

- Python, Go, TypeScript; Bash, SQL
- Docker, Kubernetes, AWS, GCP
- PostgreSQL, Redis, Kafka
```

These render as raw HTML. No special parsing — just standard markdown.

## Complete Example

```markdown
# Alex Chen

**Software / Platform Engineer**

- **Phone:** +1-555-0142
- **Email:** alex.chen@example.com
- **LinkedIn:** [linkedin.com/in/alexchen](https://linkedin.com/in/alexchen)
- **GitHub:** [github.com/alex-chen](https://github.com/alex-chen)

---

## About Me

Platform engineer with 5+ years of experience building scalable systems.

---

## Experience

### Software / Platform Engineer | Nov 2022 --- Now
**Acme Corp** | San Francisco

Core member of the Observability team.

- Led the endpoint device management platform
- Developed the telemetry ingestion gateway processing 50K events/sec
- Designed multi-tenancy authorization service

### Backend Developer | Jun 2020 --- Oct 2022
**StartupXYZ** | Remote

- Built REST APIs serving 10M requests/day
- Implemented CI/CD pipelines reducing deploy time by 60%

---

## Education

**MSc in Computer Science** | 2018 --- 2020
State University | GPA: 3.8/4.0

---

## Skills

- Go, Python, TypeScript; Bash
- Kubernetes, Docker, Helm, Terraform
- PostgreSQL, Redis, Kafka
```
