# tests/test_cli.py
"""Tests for CLI functionality."""

from click.testing import CliRunner

from content_tool.cli import cli


class TestCLI:
    """Test CLI commands."""

    def setup_method(self):
        self.runner = CliRunner()

    def test_version(self):
        """Test version command."""
        result = self.runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "Content Tool v" in result.output

    def test_help(self):
        """Test help command."""
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Content Tool" in result.output
