"""Tests for the CLI."""

from pathlib import Path

from click.testing import CliRunner

from md2cv.cli import main

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestCLI:
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_basic_pdf(self, tmp_path):
        runner = CliRunner()
        out = tmp_path / "out.pdf"
        result = runner.invoke(
            main,
            [str(FIXTURES_DIR / "sample_short.md"), "-o", str(out)],
        )
        assert result.exit_code == 0, result.output
        assert out.exists()
        assert out.stat().st_size > 0

    def test_html_only(self, tmp_path):
        runner = CliRunner()
        out = tmp_path / "out.html"
        result = runner.invoke(
            main,
            [
                str(FIXTURES_DIR / "sample_short.md"),
                "-o",
                str(out),
                "--html-only",
            ],
        )
        assert result.exit_code == 0, result.output
        assert out.exists()
        content = out.read_text()
        assert "<html" in content

    def test_both_pdf_and_html(self, tmp_path):
        runner = CliRunner()
        out = tmp_path / "out.pdf"
        result = runner.invoke(
            main,
            [
                str(FIXTURES_DIR / "sample_short.md"),
                "-o",
                str(out),
                "--html",
            ],
        )
        assert result.exit_code == 0, result.output
        assert out.exists()
        html_out = tmp_path / "out.html"
        assert html_out.exists()

    def test_page_size_letter(self, tmp_path):
        runner = CliRunner()
        out = tmp_path / "out.pdf"
        result = runner.invoke(
            main,
            [
                str(FIXTURES_DIR / "sample_minimal.md"),
                "-o",
                str(out),
                "--page-size",
                "letter",
            ],
        )
        assert result.exit_code == 0, result.output
        assert out.exists()

    def test_no_auto_fit_flag(self, tmp_path):
        runner = CliRunner()
        out = tmp_path / "out.pdf"
        result = runner.invoke(
            main,
            [
                str(FIXTURES_DIR / "sample_short.md"),
                "-o",
                str(out),
                "--no-auto-fit",
            ],
        )
        assert result.exit_code == 0, result.output

    def test_missing_input_file(self):
        runner = CliRunner()
        result = runner.invoke(main, ["nonexistent.md"])
        assert result.exit_code != 0

    def test_default_output_name(self, tmp_path):
        """When no -o flag, output should be <input_stem>.pdf in same dir."""
        import shutil

        # Copy fixture to tmp_path so output goes there
        src = FIXTURES_DIR / "sample_minimal.md"
        dest = tmp_path / "resume.md"
        shutil.copy(src, dest)

        runner = CliRunner()
        result = runner.invoke(main, [str(dest)])
        assert result.exit_code == 0, result.output
        expected = tmp_path / "resume.pdf"
        assert expected.exists()
