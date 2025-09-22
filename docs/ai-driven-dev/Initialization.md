# Project Initialization: Step-by-Step Instructions

## Step 1: Create Project Structure

```bash
# Navigate to project directory
cd C:/Atari-Monk-Art/content-tool

# Create standard Python project structure
mkdir -p src/content_tool/{core,commands,utils}
mkdir -p tests/{unit,integration}
mkdir -p docs/{api,examples}
mkdir -p scripts config data
```

## Step 2: Initialize Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/macOS)
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## Step 3: Set Up Version Control

```bash
# Initialize git repository
git init

# Create .gitignore file
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Configuration
config/local.yaml

# Test data
test_data/
*.test
EOF
```

## Step 4: Create Project Configuration Files

### setup.py
```python
# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="content-tool",
    version="0.1.0",
    author="Atari-Monk-Art",
    author_email="your-email@example.com",
    description="A unified CLI tool for file and content management operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Atari-Monk-Art/content-tool",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "content-tool=content_tool.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "content_tool": ["config/default.yaml"],
    },
)
```

### requirements.txt
```txt
# Core Dependencies
click>=8.0.0
pyperclip>=1.8.0
pyyaml>=5.4.0
pathlib2>=2.3.0; python_version < '3.4'

# Development Dependencies
pytest>=6.0.0
pytest-cov>=2.0.0
black>=21.0.0
flake8>=3.9.0
mypy>=0.900.0
isort>=5.9.0

# Documentation
mkdocs>=1.1.0
mkdocs-material>=7.0.0
```

### pyproject.toml (Modern Python configuration)
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=content_tool --cov-report=html --cov-report=term-missing"
```

## Step 5: Create Core Project Files

### src/content_tool/__init__.py
```python
# src/content_tool/__init__.py
"""Content Tool - A unified CLI tool for file and content management operations."""

__version__ = "0.1.0"
__author__ = "Atari-Monk-Art"
__email__ = "your-email@example.com"

from content_tool.cli import main

__all__ = ["main"]
```

### src/content_tool/cli.py
```python
# src/content_tool/cli.py
"""Main CLI entry point for content-tool."""

import click
from content_tool.core.config_manager import ConfigManager
from content_tool.core.logging import setup_logging

@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
@click.option('--config', type=click.Path(), help='Path to configuration file')
@click.pass_context
def cli(ctx, verbose, config):
    """Content Tool - Unified file and content management CLI"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = ConfigManager(config_path=config)
    
    # Setup logging
    setup_logging(verbose=verbose)

@cli.command()
def version():
    """Show version information"""
    from content_tool import __version__
    click.echo(f"Content Tool v{__version__}")

def main():
    """Main entry point"""
    cli(obj={})

if __name__ == '__main__':
    main()
```

### src/content_tool/core/__init__.py
```python
# src/content_tool/core/__init__.py
"""Core functionality for content-tool."""
```

### src/content_tool/core/config_manager.py
```python
# src/content_tool/core/config_manager.py
"""Configuration management for content-tool."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
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
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'defaults': {
                'ignore_dirs': ['.git', '__pycache__', 'node_modules', 'venv'],
                'ignore_files': ['.DS_Store', 'Thumbs.db', '*.pyc'],
                'output_format': 'markdown',
            },
            'index': {
                'output_name': 'index.md',
                'max_depth': 10,
            },
            'clipboard': {
                'storage_file': str(Path.home() / '.content-tool' / 'clipboard.md'),
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        # Implementation for setting config values
        pass
```

### src/content_tool/core/logging.py
```python
# src/content_tool/core/logging.py
"""Logging configuration for content-tool."""

import logging
import sys
from typing import Optional

def setup_logging(verbose: bool = False, log_file: Optional[str] = None) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create logger
    logger = logging.getLogger('content_tool')
    logger.setLevel(level)
    
    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
```

### src/content_tool/core/exceptions.py
```python
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
```

## Step 6: Create Basic Test Structure

### tests/__init__.py
```python
# tests/__init__.py
"""Test package for content-tool."""
```

### tests/test_cli.py
```python
# tests/test_cli.py
"""Tests for CLI functionality."""

import pytest
from click.testing import CliRunner
from content_tool.cli import cli

class TestCLI:
    """Test CLI commands."""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    def test_version(self):
        """Test version command."""
        result = self.runner.invoke(cli, ['version'])
        assert result.exit_code == 0
        assert 'Content Tool v' in result.output
    
    def test_help(self):
        """Test help command."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Content Tool' in result.output
```

### tests/conftest.py
```python
# tests/conftest.py
"""Pytest configuration and fixtures."""

import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_config():
    """Provide sample configuration."""
    return {
        'defaults': {
            'ignore_dirs': ['.git', '__pycache__'],
            'output_format': 'markdown'
        }
    }
```

## Step 7: Create Documentation Files

### README.md
```markdown
# Content Tool

A unified CLI tool for file and content management operations with git-like command structure.

## Features

- **Directory Indexing**: Generate Markdown indices for directory structures
- **Clipboard Management**: Advanced clipboard content management
- **Path Operations**: Path manipulation and analysis
- **Content Scanning**: Recursive file scanning and processing
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Installation

### From Source

```bash
git clone https://github.com/Atari-Monk-Art/content-tool
cd content-tool
pip install -e .
```

### From PyPI (Coming Soon)

```bash
pip install content-tool
```

## Quick Start

```bash
# Generate a blog index from content directory
content-tool index generate --format nested ~/my-blog/content

# Save current clipboard content with a name
content-tool clipboard save --name "api-response"

# Scan directory and save paths to markdown
content-tool scan paths --recursive --output paths.md ./src
```

## Command Structure

```
content-tool <command> [sub-command] [options] [arguments]

Main commands:
  config     - Tool configuration
  index      - Content indexing operations  
  clipboard  - Clipboard management
  path       - Path manipulation and analysis
  scan       - Directory scanning operations
  tree       - Directory tree generation
```

## Documentation

- [User Guide](docs/user_guide.md)
- [API Reference](docs/api/reference.md)
- [Examples](docs/examples/)

## Development

```bash
# Setup development environment
git clone https://github.com/Atari-Monk-Art/content-tool
cd content-tool
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests
isort src tests
```

## License

MIT License - see LICENSE file for details.
```

### docs/user_guide.md
```markdown
# User Guide

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)

## Installation

Detailed installation instructions...

## Configuration

How to configure the tool...

## Basic Usage

Examples of common use cases...

## Advanced Features

Advanced functionality and customization...
```

## Step 8: Create Additional Configuration Files

### config/default.yaml
```yaml
# config/default.yaml
defaults:
  ignore_dirs:
    - ".git"
    - "__pycache__"
    - "node_modules"
    - "venv"
  ignore_files:
    - ".DS_Store"
    - "Thumbs.db"
    - "*.pyc"
  output_format: "markdown"

index:
  output_name: "index.md"
  ignore_dirs:
    - "_layouts"
    - "assets"
  max_depth: 10

clipboard:
  storage_file: "~/.content-tool/clipboard.md"
  max_history: 100

scan:
  include_hidden: false
  follow_symlinks: false
```

### scripts/install-dev.sh
```bash
#!/bin/bash
# scripts/install-dev.sh
# Development environment setup script

echo "Setting up content-tool development environment..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

echo "Development environment setup complete!"
echo "Activate virtual environment with: source venv/bin/activate"
```

## Step 9: Final Setup Steps

```bash
# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt

# Run initial tests
pytest

# Format code
black src tests
isort src tests

# Initialize git
git add .
git commit -m "Initial project structure"
```

## Project Structure Summary

```
content-tool/
├── src/
│   └── content_tool/
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config_manager.py
│       │   ├── logging.py
│       │   └── exceptions.py
│       ├── commands/          # Future command implementations
│       ├── utils/             # Utility functions
│       ├── __init__.py
│       └── cli.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── __init__.py
│   ├── test_cli.py
│   └── conftest.py
├── docs/
│   ├── api/
│   ├── examples/
│   └── user_guide.md
├── config/
│   └── default.yaml
├── scripts/
│   └── install-dev.sh
├── venv/                     # Virtual environment (gitignored)
├── .gitignore
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

The project structure is now initialized with proper Python packaging, virtual environment configuration, testing setup, and documentation foundation. The architecture follows Python best practices and is ready for implementing the CLI commands as outlined in the architecture document.