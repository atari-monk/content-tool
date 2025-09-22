# src/content_tool/cli.py
"""Main CLI entry point for content-tool."""

import click

from content_tool.core.config_manager import ConfigManager
from content_tool.core.logging import setup_logging


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--config", type=click.Path(), help="Path to configuration file")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, config: str):
    """Content Tool - Unified file and content management CLI"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    from pathlib import Path
    ctx.obj["config"] = ConfigManager(config_path=Path(config) if config else None)

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


if __name__ == "__main__":
    main()
