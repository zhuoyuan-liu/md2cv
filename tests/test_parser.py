"""Tests for the markdown parser."""

from md2cv.parser import parse_cv


class TestParseCV:
    def test_extracts_name(self, sample_short):
        cv = parse_cv(sample_short)
        assert cv.name == "John Smith"

    def test_extracts_contact(self, sample_short):
        cv = parse_cv(sample_short)
        assert len(cv.contact.items) == 4
        assert "john.smith@email.com" in cv.contact.items[0]

    def test_extracts_sections(self, sample_short):
        cv = parse_cv(sample_short)
        headings = [s.heading for s in cv.sections]
        assert "Experience" in headings
        assert "Education" in headings
        assert "Skills" in headings

    def test_experience_entries(self, sample_short):
        cv = parse_cv(sample_short)
        exp = next(s for s in cv.sections if s.heading == "Experience")
        assert len(exp.entries) == 2
        assert exp.entries[0].title == "Senior Software Engineer"
        assert exp.entries[0].organization == "Acme Corp"
        assert exp.entries[0].date_range == "Jan 2022–Present"
        assert len(exp.entries[0].details) == 3

    def test_education_entries(self, sample_short):
        cv = parse_cv(sample_short)
        edu = next(s for s in cv.sections if s.heading == "Education")
        assert len(edu.entries) == 2
        assert edu.entries[0].title == "M.Sc. Computer Science"
        assert edu.entries[0].organization == "Stanford University"

    def test_skills_raw_html(self, sample_short):
        cv = parse_cv(sample_short)
        skills = next(s for s in cv.sections if s.heading == "Skills")
        # Skills section has no bold entries, so falls back to raw HTML
        assert skills.raw_html
        assert "Python" in skills.raw_html

    def test_minimal_cv(self, sample_minimal):
        cv = parse_cv(sample_minimal)
        assert cv.name == "Jane Doe"
        assert len(cv.contact.items) == 2
        assert len(cv.sections) == 1
        assert cv.sections[0].heading == "Education"

    def test_long_cv_sections(self, sample_long):
        cv = parse_cv(sample_long)
        assert cv.name == "Alexandra Johnson"
        headings = [s.heading for s in cv.sections]
        assert "Experience" in headings
        assert "Publications" in headings

    def test_no_photo_by_default(self, sample_short):
        cv = parse_cv(sample_short)
        assert cv.photo_path is None

    def test_entry_with_only_title(self):
        md = "# Name\n\nemail\n\n## Section\n\n**Just a title**\n"
        cv = parse_cv(md)
        section = cv.sections[0]
        assert len(section.entries) == 1
        assert section.entries[0].title == "Just a title"
        assert section.entries[0].organization == ""
        assert section.entries[0].date_range == ""

    def test_entry_with_date_only(self):
        md = "# Name\n\nemail\n\n## Section\n\n**Title** | 2020–2023\n"
        cv = parse_cv(md)
        entry = cv.sections[0].entries[0]
        assert entry.title == "Title"
        assert entry.date_range == "2020–2023"
