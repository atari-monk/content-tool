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