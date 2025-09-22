# src/content_tool/core/exceptions.py
"""Custom exceptions for content-tool."""


class ContentToolError(Exception):
    """Base exception for all content-tool errors."""

    pass


class ConfigError(ContentToolError):
    """Configuration-related errors."""

    pass


class FileSystemError(ContentToolError):
    """File system operation errors."""

    pass


class ClipboardError(ContentToolError):
    """Clipboard operation errors."""

    pass


class ValidationError(ContentToolError):
    """Input validation errors."""

    pass
