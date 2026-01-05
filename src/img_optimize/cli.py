"""CLI interface for img-optimize."""
import click
from pathlib import Path
from rich.console import Console
from .optimizer import ImageOptimizer
from .utils import format_size, calculate_savings

console = Console()

@click.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.option('--output', '-o', type=click.Path(), help='Output directory (default: input_dir/optimized)')
@click.option('--quality', '-q', default=85, type=click.IntRange(1, 100), help='JPEG quality (1-100, default: 85)')
@click.option('--recursive', '-r', is_flag=True, help='Process subdirectories recursively')
@click.option('--dry-run', '-d', is_flag=True, help='Preview without saving files')
def optimize(input_dir, output, quality, recursive, dry_run):
    """Optimize PNG and JPEG images in INPUT_DIR."""
    input_path = Path(input_dir)
    output_path = Path(output) if output else input_path / 'optimized'
    
    if not dry_run:
        output_path.mkdir(parents=True, exist_ok=True)
    
    optimizer = ImageOptimizer(quality=quality)
    pattern = '**/*' if recursive else '*'
    
    image_files = []
    for ext in ['*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG']:
        image_files.extend(input_path.glob(pattern.replace('*', ext)))
    
    if not image_files:
        console.print('[yellow]No image files found.[/yellow]')
        return
    
    console.print(f'[cyan]Found {len(image_files)} images to process[/cyan]')
    if dry_run:
        console.print('[yellow]DRY RUN MODE - No files will be saved[/yellow]\n')
    
    results = optimizer.process_batch(image_files, output_path, dry_run)
    
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
