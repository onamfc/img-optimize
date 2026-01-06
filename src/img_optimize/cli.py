"""CLI interface for img-optimize."""
import fnmatch
import logging
import os
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console

try:
    import yaml
except ImportError:
    yaml = None

from .optimizer import ImageOptimizer
from .utils import calculate_savings, format_size

console = Console()


def load_config(config_file: Optional[Path] = None) -> dict:
    """Load configuration from YAML file.

    Args:
        config_file: Path to config file, or None to search for default

    Returns:
        Dictionary with configuration values
    """
    if yaml is None:
        return {}

    if config_file is None:
        # Search for .img-optimize.yaml in current directory
        config_file = Path.cwd() / '.img-optimize.yaml'

    if config_file and config_file.exists():
        with open(config_file) as f:
            return yaml.safe_load(f) or {}
    return {}


def should_skip(file_path: Path, skip_patterns: List[str]) -> bool:
    """Check if file should be skipped based on patterns.

    Args:
        file_path: Path to check
        skip_patterns: List of glob patterns to skip

    Returns:
        True if file should be skipped
    """
    for pattern in skip_patterns:
        if fnmatch.fnmatch(str(file_path), pattern) or fnmatch.fnmatch(file_path.name, pattern):
            return True
    return False


@click.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.option(
    '--output', '-o', type=click.Path(), help='Output directory (default: input_dir/optimized)'
)
@click.option(
    '--quality',
    '-q',
    default=85,
    type=click.IntRange(1, 100),
    help='JPEG/WebP quality (1-100, default: 85)',
)
@click.option('--recursive', '-r', is_flag=True, help='Process subdirectories recursively')
@click.option('--dry-run', '-d', is_flag=True, help='Preview without saving files')
@click.option(
    '--in-place', '-i', is_flag=True, help='Optimize images in place (overwrite originals)'
)
@click.option('--max-width', type=int, help='Maximum width in pixels (resize if larger)')
@click.option('--max-height', type=int, help='Maximum height in pixels (resize if larger)')
@click.option(
    '--workers', '-w', default=1, type=int, help='Number of parallel workers (default: 1)'
)
@click.option('--log-file', type=click.Path(), help='Save detailed logs to file')
@click.option(
    '--skip', multiple=True, help='Skip files matching pattern (can be used multiple times)'
)
@click.option(
    '--config', type=click.Path(exists=True), help='Path to config file (.img-optimize.yaml)'
)
def optimize(
    input_dir,
    output,
    quality,
    recursive,
    dry_run,
    in_place,
    max_width,
    max_height,
    workers,
    log_file,
    skip,
    config,
):
    """Optimize PNG, JPEG, and WebP images in INPUT_DIR."""
    # Load config file
    cfg = load_config(Path(config) if config else None)

    # Merge CLI options with config (CLI takes precedence)
    quality = quality if quality != 85 else cfg.get('quality', 85)
    max_width = max_width or cfg.get('max_width')
    max_height = max_height or cfg.get('max_height')
    workers = workers if workers != 1 else cfg.get('workers', 1)
    skip_patterns = list(skip) if skip else cfg.get('skip', [])

    # Setup logging
    if log_file:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=logging.WARNING)

    input_path = Path(input_dir)

    # Handle in-place optimization
    if in_place:
        if output:
            console.print('[red]Error: --in-place and --output cannot be used together[/red]')
            return
        output_path = input_path
    else:
        output_path = Path(output) if output else input_path / 'optimized'

    if not dry_run and not in_place:
        output_path.mkdir(parents=True, exist_ok=True)

    optimizer = ImageOptimizer(
        quality=quality,
        max_width=max_width,
        max_height=max_height,
        workers=workers
    )
    pattern = '**/*' if recursive else '*'

    image_files = []
    extensions = [
        '*.png',
        '*.PNG',
        '*.jpg',
        '*.JPG',
        '*.jpeg',
        '*.JPEG',
        '*.webp',
        '*.WEBP',
    ]
    for ext in extensions:
        found = input_path.glob(pattern.replace('*', ext))
        # Filter out skipped files
        image_files.extend([f for f in found if not should_skip(f, skip_patterns)])

    if not image_files:
        console.print('[yellow]No image files found.[/yellow]')
        return

    console.print(f'[cyan]Found {len(image_files)} images to process[/cyan]')
    if dry_run:
        console.print('[yellow]DRY RUN MODE - No files will be saved[/yellow]\n')
    if in_place:
        console.print('[yellow]IN-PLACE MODE - Original files will be overwritten[/yellow]\n')
    if workers > 1:
        console.print(f'[cyan]Using {workers} parallel workers[/cyan]\n')

    results = optimizer.process_batch(image_files, output_path, input_path, dry_run)
    
    total_original = sum(r['original_size'] for r in results)
    total_optimized = sum(r['optimized_size'] for r in results)
    total_saved = total_original - total_optimized
    
    console.print(f'\n[bold green]Summary:[/bold green]')
    console.print(f'Processed: {len(results)} images')
    console.print(f'Total original size: {format_size(total_original)}')
    console.print(f'Total optimized size: {format_size(total_optimized)}')
    console.print(f'Total saved: {format_size(total_saved)} ({calculate_savings(total_original, total_optimized):.1f}%)')

if __name__ == '__main__':
    optimize()
