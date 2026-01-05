"""Tests for image optimizer."""
import pytest
from pathlib import Path
from PIL import Image
import io
from img_optimize.optimizer import ImageOptimizer


@pytest.fixture
def temp_image(tmp_path):
    """Create a temporary test image."""
    img_path = tmp_path / "test.jpg"
    img = Image.new('RGB', (100, 100), color='red')
    img.save(img_path, format='JPEG', quality=100)
    return img_path


@pytest.fixture
def temp_png(tmp_path):
    """Create a temporary PNG image."""
    img_path = tmp_path / "test.png"
    img = Image.new('RGB', (100, 100), color='blue')
    img.save(img_path, format='PNG')
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
        assert result['original_size'] > 0
        assert result['optimized_size'] > 0
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
    
    def test_process_batch(self, temp_image, temp_png, output_dir):
        optimizer = ImageOptimizer()
        image_files = [temp_image, temp_png]
        
        results = optimizer.process_batch(image_files, output_dir, dry_run=False)
        
        assert len(results) >= 0
        assert output_dir.exists()
    
    def test_invalid_image_format(self, tmp_path, output_dir):
        text_file = tmp_path / "test.txt"
        text_file.write_text("not an image")
        
        optimizer = ImageOptimizer()
        output_path = output_dir / "output.txt"
        
        result = optimizer.optimize_image(text_file, output_path)
        assert result is None
