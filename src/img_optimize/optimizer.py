"""Core image optimization logic."""
from pathlib import Path
from PIL import Image
from rich.progress import track
from rich.console import Console
from .utils import format_size, calculate_savings
import io

console = Console()

class ImageOptimizer:
    def __init__(self, quality=85):
        self.quality = quality
    
    def optimize_image(self, input_path, output_path, dry_run=False):
        """Optimize a single image file."""
        try:
            with Image.open(input_path) as img:
                original_size = input_path.stat().st_size
                
                if img.format not in ['PNG', 'JPEG']:
                    return None
                
                buffer = io.BytesIO()
                
                if img.format == 'PNG':
                    img.save(buffer, format='PNG', optimize=True)
                else:
                    exif = img.info.get('exif', b'')
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    img.save(buffer, format='JPEG', quality=self.quality, 
                            optimize=True, exif=exif)
                
                optimized_size = buffer.tell()
                
                if optimized_size >= original_size:
                    console.print(f'[yellow]Skipped {input_path.name} (would increase size)[/yellow]')
                    return None
                
                if not dry_run:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    
                    stats = input_path.stat()
                    output_path.touch()
                    import os
                    os.utime(output_path, (stats.st_atime, stats.st_mtime))
                
                savings = calculate_savings(original_size, optimized_size)
                console.print(f'[green]✓[/green] {input_path.name}: '
                            f'{format_size(original_size)} → {format_size(optimized_size)} '
                            f'({savings:.1f}% saved)')
                
                return {
                    'path': input_path,
                    'original_size': original_size,
                    'optimized_size': optimized_size
                }
        
        except Exception as e:
            console.print(f'[red]✗[/red] {input_path.name}: {str(e)}')
            return None
    
    def process_batch(self, image_files, output_dir, dry_run=False):
        """Process multiple images with progress tracking."""
        results = []
        
        for img_path in track(image_files, description='Optimizing images...'):
            rel_path = img_path.name
            output_path = output_dir / rel_path
            
            result = self.optimize_image(img_path, output_path, dry_run)
            if result:
                results.append(result)
        
        return results
