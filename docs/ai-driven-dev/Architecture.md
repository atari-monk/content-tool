# Unified CLI Tool Architecture Analysis

## Executive Summary

This document analyzes eight file and content management scripts to design a unified CLI tool with git-like command structure. The analysis identifies shared functionality, dependencies, and provides a comprehensive integration plan.

## 1. Technical Audit

### 1.1 Script Overview

| Script | Purpose | Language | Dependencies | Input | Output |
|--------|---------|----------|--------------|-------|---------|
| `blog_indexer.py` | Generate Markdown indices for directory structures | Python | argparse, pathlib | Directory path | Markdown files |
| `tree_to_clipboard.py` | Generate directory tree to clipboard | Python | pyperclip, pathlib | Directory path | Clipboard (text) |
| `scan_and_save_paths.py` | Recursively list files to paths.md | Python | argparse, pathlib | Directory path | paths.md file |
| `clipboard_collector.py` | Clipboard content management | Python | pyperclip, os | Command + optional file | Clipboard/file operations |
| `code_to_clipboard.py` | Convert code files to formatted Markdown | Python | pyperclip, argparse | Directory path | Clipboard (Markdown) |
| `load_paths.py` | Process paths.md to create content blocks | Python | pyperclip, argparse | paths.md file | Clipboard (Markdown) |
| `merge_paths.py` | Merge multiple files into Markdown | Python | pyperclip, argparse | File/directory paths | Clipboard (Markdown) |
| `path.ps1` | Path separator conversion | PowerShell | None | Clipboard content | Modified clipboard |

### 1.2 Shared Functionality Analysis

**Common Dependencies:**
- `pyperclip` (6 scripts)
- `argparse` (5 scripts) 
- `pathlib` (7 scripts)
- File I/O operations (all scripts)

**Shared Patterns:**
- Directory traversal and filtering
- Markdown generation
- Clipboard integration
- Path validation and processing
- Ignore pattern handling

## 2. CLI Command Structure Design

### 2.1 High-Level Architecture

```
content-tool
├── config
├── index
├── clipboard
├── scan
├── tree
└── path
```

### 2.2 Command Specification

```bash
# Configuration Management
content-tool config init [--global]          # Initialize configuration
content-tool config set <key> <value>       # Set configuration value
content-tool config get <key>               # Get configuration value
content-tool config list                    # List all configurations

# Indexing Operations
content-tool index generate <path>          # Generate directory indices
content-tool index update <path>            # Update existing indices
content-tool index validate <path>          # Validate index structure

# Clipboard Operations
content-tool clipboard push [<file>]        # Push content to clipboard store
content-tool clipboard pop                  # Pop content from clipboard store
content-tool clipboard reset                # Reset clipboard store
content-tool clipboard list                 # List clipboard history

# Scanning Operations
content-tool scan paths <directory>         # Scan and save file paths
content-tool scan content <directory>       # Scan and generate content blocks
content-tool scan code <directory>          # Scan code files to Markdown

# Tree Operations
content-tool tree generate <directory>      # Generate directory tree
content-tool tree copy <directory>          # Copy tree to clipboard

# Path Operations
content-tool path convert-separator         # Convert path separators
content-tool path normalize <path>          # Normalize path format
```

### 2.3 Namespace Hierarchy

```
content-tool/
    commands/
        config.py
        index.py
        clipboard.py
        scan.py
        tree.py
        path.py
    core/
        cli.py
        config_manager.py
        file_processor.py
        clipboard_manager.py
    utils/
        validators.py
        formatters.py
        filters.py
```

## 3. Configuration Management Strategy

### 3.1 Configuration Schema

```yaml
# ~/.content-tool/config.yaml
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
  clipboard_file: "C:/Atari-Monk-Art/app-data/clipboard.md"

index:
  output_name: "index.md"
  ignore_dirs:
    - "_layouts"
    - "assets"
    - "draft"
  ignore_files:
    - "_config.yml"
    - "README.md"

scan:
  max_depth: 10
  include_hidden: false
```

### 3.2 Configuration Implementation

```python
# core/config_manager.py
from pathlib import Path
import yaml
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path.home() / ".content-tool" / "config.yaml"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        return self._get_default_config()
```

## 4. Error Handling and Logging

### 4.1 Unified Error Hierarchy

```python
# core/exceptions.py
class ContentToolError(Exception):
    """Base exception for all content-tool errors"""

class ConfigError(ContentToolError):
    """Configuration-related errors"""

class FileSystemError(ContentToolError):
    """File system operation errors"""

class ClipboardError(ContentToolError):
    """Clipboard operation errors"""

class ValidationError(ContentToolError):
    """Input validation errors"""
```

### 4.2 Logging Strategy

```python
# core/logging.py
import logging
import sys

def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('content-tool.log')
        ]
    )
```

## 5. Cross-Platform Compatibility Plan

### 5.1 Platform Detection and Adaptation

```python
# utils/platform.py
import platform
import sys
from pathlib import Path

class PlatformManager:
    @property
    def is_windows(self) -> bool:
        return platform.system() == "Windows"
    
    @property
    def is_linux(self) -> bool:
        return platform.system() == "Linux"
    
    @property
    def is_macos(self) -> bool:
        return platform.system() == "Darwin"
    
    def get_clipboard_command(self) -> str:
        if self.is_windows:
            return "powershell"
        elif self.is_macos:
            return "pbcopy"
        else:
            return "xclip"
```

### 5.2 PowerShell Integration Strategy

```python
# commands/path.py
import subprocess
from core.platform import PlatformManager

class PathCommand:
    def __init__(self):
        self.platform = PlatformManager()
    
    def convert_separators(self):
        if self.platform.is_windows:
            # Execute PowerShell script
            ps_script = """
            $clipboardContent = Get-Clipboard
            if (-not [string]::IsNullOrEmpty($clipboardContent)) {
                $convertedPath = $clipboardContent -replace '\\\\', '/'
                Set-Clipboard -Value $convertedPath
            }
            """
            subprocess.run(["powershell", "-Command", ps_script], check=True)
        else:
            # Linux/macOS implementation
            pass
```

## 6. Dependency Matrix

### 6.1 Core Dependencies

| Dependency | Scripts Using | Purpose | Alternative |
|------------|---------------|---------|-------------|
| `pyperclip` | 6/8 | Clipboard operations | `xclip`/`pbcopy` fallbacks |
| `argparse` | 5/8 | Command-line parsing | `click` (recommended) |
| `pathlib` | 7/8 | Path manipulation | Built-in (no alternative needed) |

### 6.2 Recommended Unified Dependencies

```txt
# requirements.txt
click>=8.0.0
pyperclip>=1.8.0
pyyaml>=5.0.0
pathlib2>=2.3.0; python_version < '3.4'
```

## 7. Implementation Roadmap

### Phase 1: Core Infrastructure (Weeks 1-2)
- Implement CLI framework with Click
- Create configuration management system
- Build shared utility modules
- Implement error handling and logging

### Phase 2: Command Integration (Weeks 3-4)
- Migrate `clipboard` commands
- Implement `index` commands
- Add `scan` and `tree` functionality
- Create `path` operations

### Phase 3: Advanced Features (Weeks 5-6)
- Add batch processing capabilities
- Implement plugin system
- Create comprehensive testing suite
- Develop documentation and examples

## 8. Deliverables

### 8.1 Architecture Document (This Document)
- Complete technical analysis
- Command structure specification
- Configuration management plan
- Cross-platform compatibility strategy

### 8.2 Dependency Matrix
- Current dependency analysis
- Unified dependency recommendations
- Alternative implementation strategies

### 8.3 Command Structure Specification
```yaml
commands:
  config:
    description: "Manage tool configuration"
    subcommands:
      init: "Initialize configuration"
      set: "Set configuration value"
      get: "Get configuration value"
  
  index:
    description: "Directory indexing operations"
    subcommands:
      generate: "Generate directory indices"
      update: "Update existing indices"
  
  clipboard:
    description: "Clipboard content management"
    subcommands:
      push: "Push content to clipboard store"
      pop: "Pop content from clipboard store"
```

## 9. Conclusion

The analysis reveals significant opportunities for code reuse and standardization across the eight scripts. The proposed unified CLI tool architecture provides:

1. **Consistent User Experience**: Git-like command structure
2. **Code Reusability**: Shared functionality in core modules
3. **Maintainability**: Standardized error handling and logging
4. **Cross-Platform Support**: Unified approach for Windows/Linux/macOS
5. **Extensibility**: Plugin-friendly architecture for future enhancements

The implementation plan provides a clear roadmap for integrating the existing scripts into a cohesive, professional-grade CLI tool.