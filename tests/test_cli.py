"""Tests for Serena CLI components."""

import pytest
from typer.testing import CliRunner

from serena.cli.cli import app
from serena.cli.formatters import OutputFormatter


runner = CliRunner()


class TestCLI:
    """Test CLI commands."""

    def test_help(self):
        """Test --help flag."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Semantic code navigation" in result.stdout

    def test_version_command(self):
        """Test version command."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "2.0.0" in result.stdout  # CLI version

    def test_unknown_command(self):
        """Test unknown command handling."""
        result = runner.invoke(app, ["unknown_command_xyz"])
        assert result.exit_code != 0


class TestFormatters:
    """Test output formatters."""

    def test_format_error(self):
        """Test error formatting."""
        fmt = OutputFormatter(json_mode=False)
        result = fmt.format_error("Test error", hint="Try again")
        assert "Test error" in result
        assert "Try again" in result

    def test_format_error_json(self):
        """Test error formatting in JSON mode."""
        fmt = OutputFormatter(json_mode=True)
        result = fmt.format_error("Test error")
        assert '"error"' in result
        assert "Test error" in result

    def test_format_success(self):
        """Test success formatting."""
        fmt = OutputFormatter(json_mode=False)
        result = fmt.format_success("Operation completed")
        assert "Operation completed" in result

    def test_format_success_json(self):
        """Test success formatting in JSON mode."""
        fmt = OutputFormatter(json_mode=True)
        result = fmt.format_success("Done")
        assert '"success"' in result

    def test_format_status_string(self):
        """Test status formatting with string input."""
        fmt = OutputFormatter(json_mode=False)
        result = fmt.format_status("Serena version: 1.0.0\nProject: test")
        assert "Serena Status" in result
        assert "version" in result.lower()

    def test_format_status_dict(self):
        """Test status formatting with dict input."""
        fmt = OutputFormatter(json_mode=False)
        result = fmt.format_status({"project": "myproject", "root": "/path"})
        assert "myproject" in result
        assert "/path" in result

    def test_format_memory_list_empty(self):
        """Test empty memory list formatting."""
        fmt = OutputFormatter(json_mode=False)
        result = fmt.format_memory_list([])
        assert "No memories" in result

    def test_format_memory_list(self):
        """Test memory list formatting."""
        fmt = OutputFormatter(json_mode=False)
        result = fmt.format_memory_list(["mem1", "mem2"])
        assert "mem1" in result
        assert "mem2" in result

    def test_format_symbols_empty(self):
        """Test empty symbols formatting."""
        fmt = OutputFormatter(json_mode=False)
        result = fmt.format_symbols([])
        assert "no symbols" in result.lower() or result == ""

    def test_format_symbols(self):
        """Test symbol formatting."""
        fmt = OutputFormatter(json_mode=False)
        symbols = [
            {"name_path": "MyClass", "kind": 5, "relative_path": "src/MyClass.php"}
        ]
        result = fmt.format_symbols(symbols)
        assert "MyClass" in result
