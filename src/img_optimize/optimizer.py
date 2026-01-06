"""Core image optimization logic."""
import io
import logging
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Union

from PIL import Image
from rich.console import Console
from rich.progress import track

from .utils import calculate_savings, format_size

console = Console()
logger = logging.getLogger(__name__)

# Supported image formats (PIL reports these format names)
SUPPORTED_FORMATS = ['PNG', 'JPEG', 'WEBP', 'MPO']  # MPO is multi-picture JPEG


class ImageOptimizer:
    """Image optimization engine with support for multiple formats and options.

    Attributes:
        quality: JPEG/WebP quality (1-100)
        max_width: Maximum width for resizing (None = no resize)
        max_height: Maximum height for resizing (None = no resize)
        workers: Number of parallel workers (1 = sequential)
    """

    def __init__(
        self,
        quality: int = 85,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        workers: int = 1
    ) -> None:
        """Initialize the image optimizer.

        Args:
            quality: Quality setting for lossy compression (1-100, default: 85)
            max_width: Maximum width in pixels, images will be resized if larger
            max_height: Maximum height in pixels, images will be resized if larger
            workers: Number of parallel workers for batch processing
        """
        self.quality = quality
        self.max_width = max_width
        self.max_height = max_height
        self.workers = workers
    
    def _resize_if_needed(self, img: Image.Image) -> Image.Image:
        """Resize image if it exceeds max dimensions.

        Args:
            img: PIL Image object

        Returns:
            Resized image or original if no resize needed
        """
        if not self.max_width and not self.max_height:
            return img

        width, height = img.size
        needs_resize = False

        if self.max_width and width > self.max_width:
            needs_resize = True
            ratio = self.max_width / width
            width = self.max_width
            height = int(height * ratio)

        if self.max_height and height > self.max_height:
            needs_resize = True
            ratio = self.max_height / height
            height = self.max_height
            width = int(width * ratio)

        if needs_resize:
            return img.resize((width, height), Image.Resampling.LANCZOS)
        return img

    def optimize_image(
        self,
        input_path: Path,
        output_path: Path,
        dry_run: bool = False
    ) -> Optional[Dict[str, Union[Path, int]]]:
        """Optimize a single image file.

        Args:
            input_path: Path to input image
            output_path: Path where optimized image will be saved
            dry_run: If True, don't save the file

        Returns:
            Dictionary with optimization results or None if failed/skipped

        Raises:
            No exceptions raised; errors are logged and None is returned
        """
        try:
            with Image.open(input_path) as img:
                original_size = input_path.stat().st_size

                # Determine format from file extension if PIL doesn't detect it
                img_format = img.format
                if not img_format:
                    ext = input_path.suffix.lower()
                    if ext in [".webp"]:
                        img_format = "WEBP"
                    elif ext in [".png"]:
                        img_format = "PNG"
                    elif ext in [".jpg", ".jpeg"]:
                        img_format = "JPEG"

                if img_format not in SUPPORTED_FORMATS:
                    logger.warning(
                        f"Unsupported format: {img_format} for {input_path.name}"
                    )
                    return None

                # Resize if needed
                img = self._resize_if_needed(img)

                buffer = io.BytesIO()

                if img_format == "PNG":
                    img.save(buffer, format="PNG", optimize=True)
                elif img_format == "WEBP":
                    img.save(buffer, format="WEBP", quality=self.quality, method=6)
                else:  # JPEG or MPO
                    exif = img.info.get("exif", b"")
                    if img.mode in ("RGBA", "LA", "P"):
                        img = img.convert("RGB")
                    img.save(
                        buffer,
                        format="JPEG",
                        quality=self.quality,
                        optimize=True,
                        exif=exif,
                    )

                optimized_size = buffer.tell()

                if optimized_size >= original_size:
                    console.print(
                        f"[yellow]Skipped {input_path.name} (would increase size)[/yellow]"
                    )
                    return None

                if not dry_run:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(buffer.getvalue())

                    stats = input_path.stat()
                    output_path.touch()
                    os.utime(output_path, (stats.st_atime, stats.st_mtime))

                savings = calculate_savings(original_size, optimized_size)
                console.print(
                    f"[green]✓[/green] {input_path.name}: "
                    f"{format_size(original_size)} → {format_size(optimized_size)} "
                    f"({savings:.1f}% saved)"
                )

                return {
                    "path": input_path,
                    "original_size": original_size,
                    "optimized_size": optimized_size,
                }

        except Exception as e:
            console.print(f"[red]✗[/red] {input_path.name}: {str(e)}")
            logger.error(f"Error optimizing {input_path}: {e}", exc_info=True)
            return None
    
    def process_batch(
        self,
        image_files: List[Path],
        output_dir: Path,
        input_dir: Path,
        dry_run: bool = False
    ) -> List[Dict[str, Union[Path, int]]]:
        """Process multiple images with progress tracking.

        Args:
            image_files: List of image file paths to process
            output_dir: Directory where optimized images will be saved
            input_dir: Base input directory (for calculating relative paths)
            dry_run: If True, don't save files

        Returns:
            List of optimization results for successfully processed images
        """
        results = []

        if self.workers > 1:
            # Parallel processing
            with ProcessPoolExecutor(max_workers=self.workers) as executor:
                futures = {}
                for img_path in image_files:
                    rel_path = img_path.relative_to(input_dir)
                    output_path = output_dir / rel_path
                    future = executor.submit(
                        self.optimize_image, img_path, output_path, dry_run
                    )
                    futures[future] = img_path

                for future in track(
                    as_completed(futures),
                    total=len(futures),
                    description="Optimizing images...",
                ):
                    result = future.result()
                    if result:
                        results.append(result)
        else:
            # Sequential processing
            for img_path in track(image_files, description="Optimizing images..."):
                rel_path = img_path.relative_to(input_dir)
                output_path = output_dir / rel_path

                result = self.optimize_image(img_path, output_path, dry_run)
                if result:
                    results.append(result)

        return results
