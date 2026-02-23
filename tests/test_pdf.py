"""Tests for PDF generation."""

from md2cv.models import CVData, CVEntry, CVSection, ContactInfo, StyleParams
from md2cv.parser import parse_cv
from md2cv.pdf import _scale_params, generate_pdf


class TestScaleParams:
    def test_scale_factor_1_returns_same(self):
        style = StyleParams()
        scaled = _scale_params(style, 1.0)
        assert scaled.base_font_size == style.base_font_size
        assert scaled.margin_top == style.margin_top
        assert scaled.line_height == style.line_height

    def test_scale_factor_reduces_font(self):
        style = StyleParams(base_font_size=10.0)
        scaled = _scale_params(style, 0.8)
        assert scaled.base_font_size == 8.0

    def test_margins_shrink_slower(self):
        style = StyleParams(margin_top=20.0)
        scaled = _scale_params(style, 0.8)
        # margin_factor = 0.5 + 0.5 * 0.8 = 0.9
        assert abs(scaled.margin_top - 18.0) < 0.01

    def test_line_height_shrink_slower(self):
        style = StyleParams(line_height=1.4)
        scaled = _scale_params(style, 0.8)
        # lh_factor = 0.85 + 0.15 * 0.8 = 0.97
        expected = 1.4 * 0.97
        assert abs(scaled.line_height - expected) < 0.01

    def test_min_scale(self):
        style = StyleParams(base_font_size=10.0)
        scaled = _scale_params(style, 0.65)
        assert scaled.base_font_size == 6.5


class TestGeneratePDF:
    def test_generates_pdf_file(self, tmp_path, sample_short):
        cv = parse_cv(sample_short)
        out = tmp_path / "test.pdf"
        result = generate_pdf(cv, out)
        assert result.exists()
        assert result.stat().st_size > 0
        # Check PDF magic bytes
        data = result.read_bytes()
        assert data[:5] == b"%PDF-"

    def test_letter_page_size(self, tmp_path, sample_minimal):
        cv = parse_cv(sample_minimal)
        out = tmp_path / "test.pdf"
        result = generate_pdf(cv, out, page_size="letter")
        assert result.exists()

    def test_no_auto_fit(self, tmp_path, sample_minimal):
        cv = parse_cv(sample_minimal)
        out = tmp_path / "test.pdf"
        result = generate_pdf(cv, out, auto_fit=False)
        assert result.exists()

    def test_auto_fit_long_cv(self, tmp_path, sample_long):
        cv = parse_cv(sample_long)
        out = tmp_path / "test.pdf"
        result = generate_pdf(cv, out, auto_fit=True)
        assert result.exists()
        assert result.stat().st_size > 0
