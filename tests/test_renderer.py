"""Tests for the HTML renderer."""

from md2cv.models import CVData, CVEntry, CVSection, ContactInfo, StyleParams
from md2cv.renderer import render_html


class TestRenderHTML:
    def test_renders_name(self):
        cv = CVData(name="Jane Doe")
        html = render_html(cv)
        assert "Jane Doe" in html

    def test_renders_contact(self):
        cv = CVData(
            name="Jane",
            contact=ContactInfo(items=["jane@test.com", "+1-555-0100"]),
        )
        html = render_html(cv)
        assert "jane@test.com" in html
        assert "+1-555-0100" in html

    def test_renders_section_heading(self):
        cv = CVData(
            name="Jane",
            sections=[CVSection(heading="Experience")],
        )
        html = render_html(cv)
        assert "Experience" in html

    def test_renders_entry(self):
        entry = CVEntry(
            title="Engineer",
            organization="Acme",
            date_range="2020–2023",
            details=["Built things", "Fixed bugs"],
        )
        cv = CVData(
            name="Jane",
            sections=[CVSection(heading="Experience", entries=[entry])],
        )
        html = render_html(cv)
        assert "Engineer" in html
        assert "Acme" in html
        assert "2020–2023" in html
        assert "Built things" in html

    def test_renders_raw_html_section(self):
        cv = CVData(
            name="Jane",
            sections=[CVSection(heading="Skills", raw_html="<p>Python, Go</p>")],
        )
        html = render_html(cv)
        assert "Python, Go" in html

    def test_self_contained_html(self):
        cv = CVData(name="Jane")
        html = render_html(cv)
        assert "<html" in html
        assert "<style>" in html
        assert "</html>" in html

    def test_custom_style(self):
        cv = CVData(name="Jane")
        style = StyleParams(base_font_size=12.0)
        html = render_html(cv, style=style)
        assert "12.0pt" in html

    def test_no_photo_no_img_tag(self):
        cv = CVData(name="Jane")
        html = render_html(cv)
        assert "<img" not in html

    def test_photo_embedding(self, tmp_path):
        # Create a tiny valid PNG
        import base64

        # 1x1 red PNG
        png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4"
            "2mP8/58BAwAI/AL+hc2rNAAAAABJRU5ErkJggg=="
        )
        photo = tmp_path / "photo.png"
        photo.write_bytes(base64.b64decode(png_b64))

        cv = CVData(name="Jane", photo_path=str(photo))
        html = render_html(cv)
        assert "<img" in html
        assert "base64" in html
        assert 'class="photo"' in html
