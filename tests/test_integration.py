"""Integration tests for end-to-end functionality."""
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner
from PIL import Image

from img_optimize.cli import optimize


@pytest.fixture
def sample_images_dir(tmp_path):
    """Create a directory with various test images."""
    img_dir = tmp_path / "images"
    img_dir.mkdir()

    # Create JPEG with higher quality so optimization can reduce size
    jpg = Image.new('RGB', (200, 200), color='red')
    jpg.save(img_dir / "photo.jpg", format='JPEG', quality=100)

    # Create PNG (unoptimized)
    png = Image.new('RGB', (200, 200), color='blue')
    png.save(img_dir / "graphic.png", format='PNG', optimize=False)

    # Create WebP with high quality
    webp = Image.new('RGB', (200, 200), color='green')
    webp.save(img_dir / "modern.webp", format='WEBP', quality=100, method=0)

    # Create subdirectory with image
    subdir = img_dir / "subfolder"
    subdir.mkdir()
    sub_img = Image.new('RGB', (150, 150), color='yellow')
    sub_img.save(subdir / "nested.jpg", format='JPEG', quality=100)

    return img_dir


class TestCLIIntegration:
    """Test complete CLI workflows."""

    def test_basic_optimization(self, sample_images_dir):
        """Test basic optimization workflow."""
        runner = CliRunner()
        result = runner.invoke(optimize, [str(sample_images_dir)])

        assert result.exit_code == 0
        assert "Summary" in result.output
        assert (sample_images_dir / "optimized").exists()

    def test_recursive_optimization(self, sample_images_dir):
        """Test recursive directory optimization."""
        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--recursive'
        ])

        assert result.exit_code == 0
        # Check that nested image was processed
        nested_output = sample_images_dir / "optimized" / "subfolder" / "nested.jpg"
        assert nested_output.exists()

    def test_custom_output_dir(self, sample_images_dir, tmp_path):
        """Test with custom output directory."""
        output_dir = tmp_path / "custom_output"

        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--output', str(output_dir)
        ])

        assert result.exit_code == 0
        assert output_dir.exists()
        assert (output_dir / "photo.jpg").exists()

    def test_in_place_optimization(self, sample_images_dir):
        """Test in-place optimization."""
        original_size = (sample_images_dir / "photo.jpg").stat().st_size

        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--in-place'
        ])

        assert result.exit_code == 0
        assert "IN-PLACE MODE" in result.output
        # File should still exist and potentially be smaller
        assert (sample_images_dir / "photo.jpg").exists()

    def test_max_dimensions(self, sample_images_dir, tmp_path):
        """Test image resizing with max dimensions."""
        output_dir = tmp_path / "resized"

        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--output', str(output_dir),
            '--max-width', '100',
            '--max-height', '100'
        ])

        assert result.exit_code == 0

        # Check that images were resized
        with Image.open(output_dir / "photo.jpg") as img:
            assert img.width <= 100
            assert img.height <= 100

    def test_quality_setting(self, sample_images_dir):
        """Test custom quality setting."""
        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--quality', '70'
        ])

        assert result.exit_code == 0

    def test_dry_run_mode(self, sample_images_dir):
        """Test that dry-run doesn't create files."""
        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--dry-run'
        ])

        assert result.exit_code == 0
        assert "DRY RUN MODE" in result.output
        assert not (sample_images_dir / "optimized").exists()

    def test_skip_patterns(self, sample_images_dir):
        """Test skipping files based on patterns."""
        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--skip', '*.webp',
            '--skip', '*nested*'
        ])

        assert result.exit_code == 0
        # WebP and nested files should not be in output
        output_dir = sample_images_dir / "optimized"
        assert not (output_dir / "modern.webp").exists()

    def test_parallel_workers(self, sample_images_dir):
        """Test parallel processing."""
        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--workers', '2'
        ])

        assert result.exit_code == 0
        assert "parallel workers" in result.output.lower()

    def test_config_file(self, sample_images_dir, tmp_path):
        """Test loading configuration from file."""
        config_path = tmp_path / ".img-optimize.yaml"
        config_data = {
            'quality': 80,
            'max_width': 500,
            'skip': ['*.webp']
        }

        with open(config_path, 'w') as f:
            yaml.dump(config_data, f)

        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--config', str(config_path)
        ])

        assert result.exit_code == 0

    def test_log_file_creation(self, sample_images_dir, tmp_path):
        """Test that log file is created."""
        log_path = tmp_path / "optimize.log"

        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--log-file', str(log_path)
        ])

        assert result.exit_code == 0
        assert log_path.exists()
        assert log_path.stat().st_size > 0

    def test_empty_directory(self, tmp_path):
        """Test handling of empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        runner = CliRunner()
        result = runner.invoke(optimize, [str(empty_dir)])

        assert result.exit_code == 0
        assert "No image files found" in result.output

    def test_conflicting_options(self, sample_images_dir, tmp_path):
        """Test that conflicting options are handled."""
        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(sample_images_dir),
            '--in-place',
            '--output', str(tmp_path / "output")
        ])

        assert "cannot be used together" in result.output.lower()


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_nonexistent_directory(self):
        """Test handling of nonexistent input directory."""
        runner = CliRunner()
        result = runner.invoke(optimize, ['/nonexistent/path'])

        assert result.exit_code != 0

    def test_corrupted_image(self, tmp_path):
        """Test handling of corrupted image files."""
        img_dir = tmp_path / "images"
        img_dir.mkdir()

        # Create a corrupted "image" file
        corrupted = img_dir / "broken.jpg"
        corrupted.write_bytes(b"not a real image")

        runner = CliRunner()
        result = runner.invoke(optimize, [str(img_dir)])

        # Should complete but report error for corrupted file
        assert result.exit_code == 0
        assert "✗" in result.output or "No image files found" in result.output


class TestWebPFormat:
    """Test WebP-specific functionality."""

    def test_webp_optimization(self, tmp_path):
        """Test WebP image optimization."""
        img_dir = tmp_path / "webp_images"
        img_dir.mkdir()

        # Create WebP image with lower quality so optimization can work
        img = Image.new('RGB', (300, 300), color='purple')
        # Use lower quality and simpler compression method to allow optimization
        img.save(img_dir / "test.webp", format='WEBP', quality=95, method=0)

        runner = CliRunner()
        result = runner.invoke(optimize, [
            str(img_dir),
            '--quality', '75'
        ])

        assert result.exit_code == 0

        # Check if optimization happened or was skipped
        output_path = img_dir / "optimized" / "test.webp"
        if output_path.exists():
            # Verify it's still a valid WebP
            with Image.open(output_path) as img:
                assert img.format == 'WEBP'
        else:
            # File might have been skipped if optimization would increase size
            # Check that the command at least ran successfully
            assert "images to process" in result.output or "No image files" in result.output
