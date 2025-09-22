# src/content_tool/core/config_manager.py
"""Configuration management for content-tool."""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ConfigManager:
    """Manage configuration settings for the content-tool."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()

    def _get_default_config_path(self) -> Path:
        """Get the default configuration file path."""
        config_dir = Path.home() / ".content-tool"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.yaml"

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults."""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f) or {}
        return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "defaults": {
                "ignore_dirs": [".git", "__pycache__", "node_modules", "venv"],
                "ignore_files": [".DS_Store", "Thumbs.db", "*.pyc"],
                "output_format": "markdown",
            },
            "index": {
                "output_name": "index.md",
                "max_depth": 10,
            },
            "clipboard": {
                "storage_file": str(Path.home() / ".content-tool" / "clipboard.md"),
            },
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        # Implementation for setting config values
        pass
