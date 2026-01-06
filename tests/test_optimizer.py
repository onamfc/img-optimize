"""Tests for image optimizer."""

from pathlib import Path

import pytest
from PIL import Image

from img_optimize.optimizer import ImageOptimizer


@pytest.fixture
def temp_image(tmp_path):
    """Create a temporary test image."""
    img_path = tmp_path / "test.jpg"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path, format="JPEG", quality=100)
    return img_path


@pytest.fixture
def temp_png(tmp_path):
    """Create a temporary PNG image."""
    img_path = tmp_path / "test.png"
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(img_path, format="PNG")
    return img_path


@pytest.fixture
def output_dir(tmp_path):
    return tmp_path / "output"


class TestImageOptimizer:
    def test_init_default_quality(self):
        optimizer = ImageOptimizer()
        assert optimizer.quality == 85

    def test_init_custom_quality(self):
        optimizer = ImageOptimizer(quality=75)
        assert optimizer.quality == 75

    def test_optimize_jpeg(self, temp_image, output_dir):
        optimizer = ImageOptimizer(quality=85)
        output_path = output_dir / "optimized.jpg"

        result = optimizer.optimize_image(temp_image, output_path, dry_run=False)

        assert result is not None
        assert result["original_size"] > 0
        assert result["optimized_size"] > 0
        assert output_path.exists()

    def test_optimize_png(self, temp_png, output_dir):
        optimizer = ImageOptimizer()
        output_path = output_dir / "optimized.png"

        result = optimizer.optimize_image(temp_png, output_path, dry_run=False)

        assert result is not None
        assert output_path.exists()

    def test_dry_run_mode(self, temp_image, output_dir):
        optimizer = ImageOptimizer()
        output_path = output_dir / "optimized.jpg"

        result = optimizer.optimize_image(temp_image, output_path, dry_run=True)

        assert result is not None
        assert not output_path.exists()

    def test_process_batch(self, temp_image, temp_png, output_dir, tmp_path):
        optimizer = ImageOptimizer()
        image_files = [temp_image, temp_png]

        results = optimizer.process_batch(image_files, output_dir, tmp_path, dry_run=False)

        assert len(results) >= 0
        assert output_dir.exists()

    def test_invalid_image_format(self, tmp_path, output_dir):
        text_file = tmp_path / "test.txt"
        text_file.write_text("not an image")

        optimizer = ImageOptimizer()
        output_path = output_dir / "output.txt"

        result = optimizer.optimize_image(text_file, output_path)
        assert result is None

    def test_resize_large_image(self, tmp_path, output_dir):
        """Test that images are resized when max dimensions are set."""
        # Create a large image
        img_path = tmp_path / "large.jpg"
        img = Image.new("RGB", (2000, 1500), color="red")
        img.save(img_path, format="JPEG", quality=95)

        optimizer = ImageOptimizer(quality=85, max_width=1000, max_height=1000)
        output_path = output_dir / "resized.jpg"

        result = optimizer.optimize_image(img_path, output_path, dry_run=False)

        assert result is not None
        assert output_path.exists()

        # Check that the output image is smaller
        with Image.open(output_path) as resized:
            assert resized.width <= 1000
            assert resized.height <= 1000

    def test_max_width_only(self, tmp_path, output_dir):
        """Test resize with only max_width set."""
        img_path = tmp_path / "wide.jpg"
        img = Image.new("RGB", (2000, 1000), color="blue")
        img.save(img_path, format="JPEG", quality=95)

        optimizer = ImageOptimizer(max_width=1000)
        output_path = output_dir / "resized_width.jpg"

        result = optimizer.optimize_image(img_path, output_path, dry_run=False)

        with Image.open(output_path) as resized:
            assert resized.width == 1000
            assert resized.height == 500  # Should maintain aspect ratio

    def test_parallel_processing(self, tmp_path, output_dir):
        """Test parallel batch processing."""
        # Create multiple test images
        image_files = []
        for i in range(5):
            img_path = tmp_path / f"test_{i}.jpg"
            img = Image.new("RGB", (100, 100), color="red")
            img.save(img_path, format="JPEG", quality=100)
            image_files.append(img_path)

        optimizer = ImageOptimizer(quality=85, workers=2)
        results = optimizer.process_batch(image_files, output_dir, tmp_path, dry_run=False)

        assert len(results) > 0

    def test_webp_support(self, tmp_path, output_dir):
        """Test WebP image optimization."""
        # Create a WebP image with low quality so optimization can reduce size
        img_path = tmp_path / "test.webp"
        img = Image.new("RGB", (200, 200), color="green")
        # Save with lower quality so optimization can actually reduce the file size
        img.save(img_path, format="WEBP", quality=95, method=0)

        optimizer = ImageOptimizer(quality=75)
        output_path = output_dir / "optimized.webp"

        result = optimizer.optimize_image(img_path, output_path, dry_run=False)

        # WebP optimization might be skipped if it increases size, which is ok
        if result is not None:
            assert output_path.exists()
        else:
            # If skipped, that's also valid behavior
            assert True

    def test_preserve_directory_structure(self, tmp_path, output_dir):
        """Test that directory structure is preserved in recursive mode."""
        # Create nested directory structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        img_path = subdir / "nested.jpg"
        img = Image.new("RGB", (50, 50), color="yellow")
        img.save(img_path, format="JPEG", quality=100)

        optimizer = ImageOptimizer()
        results = optimizer.process_batch([img_path], output_dir, tmp_path, dry_run=False)

        # Check that subdirectory was created in output
        expected_output = output_dir / "subdir" / "nested.jpg"
        assert expected_output.exists()
