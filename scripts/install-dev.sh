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