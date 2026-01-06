"""Tests for CLI interface."""

from pathlib import Path

import pytest
from click.testing import CliRunner
from PIL import Image

from img_optimize.cli import optimize


@pytest.fixture
def test_images_dir(tmp_path):
    """Create directory with test images."""
    img_dir = tmp_path / "images"
    img_dir.mkdir()

    img1 = Image.new("RGB", (50, 50), color="red")
    img1.save(img_dir / "test1.jpg", format="JPEG", quality=100)

    img2 = Image.new("RGB", (50, 50), color="blue")
    img2.save(img_dir / "test2.png", format="PNG")

    return img_dir


class TestCLI:
    def test_basic_optimization(self, test_images_dir):
        runner = CliRunner()
        result = runner.invoke(optimize, [str(test_images_dir)])

        assert result.exit_code == 0
        assert "Summary" in result.output

    def test_custom_output_dir(self, test_images_dir, tmp_path):
        runner = CliRunner()
        output_dir = tmp_path / "custom_output"

        result = runner.invoke(
            optimize, [str(test_images_dir), "--output", str(output_dir)]
        )

        assert result.exit_code == 0
        assert output_dir.exists()

    def test_quality_option(self, test_images_dir):
        runner = CliRunner()
        result = runner.invoke(optimize, [str(test_images_dir), "--quality", "75"])

        assert result.exit_code == 0

    def test_dry_run_mode(self, test_images_dir):
        runner = CliRunner()
        result = runner.invoke(optimize, [str(test_images_dir), "--dry-run"])

        assert result.exit_code == 0
        assert "DRY RUN MODE" in result.output

    def test_no_images_found(self, tmp_path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        runner = CliRunner()
        result = runner.invoke(optimize, [str(empty_dir)])

        assert result.exit_code == 0
        assert "No image files found" in result.output

    def test_recursive_flag(self, tmp_path):
        img_dir = tmp_path / "images"
        sub_dir = img_dir / "subdir"
        sub_dir.mkdir(parents=True)

        img = Image.new("RGB", (50, 50), color="green")
        img.save(sub_dir / "nested.jpg", format="JPEG")

        runner = CliRunner()
        result = runner.invoke(optimize, [str(img_dir), "--recursive"])

        assert result.exit_code == 0
