# Image Optimizer

A powerful CLI tool for batch optimizing PNG, JPEG, and WebP images with advanced features like parallel processing, resizing, and config file support.

## Features

### Core Functionality
- **Multiple format support**: PNG, JPEG, and WebP optimization
- **Parallel processing**: Use multiple CPU cores for faster batch operations
- **Smart resizing**: Automatically resize images that exceed maximum dimensions
- **In-place optimization**: Overwrite originals or create copies in a separate directory
- **Recursive processing**: Handle nested directory structures with preserved hierarchy
- **Config file support**: Set project-specific defaults with `.img-optimize.yaml`

### Quality & Preservation
- Configurable quality levels (default: 85 for JPEG/WebP)
- Preserve original EXIF metadata
- Maintain file timestamps
- Skip files that would increase in size after optimization

### Developer Experience
- Dry-run mode to preview optimizations without saving
- Detailed logging with `--log-file` option
- Skip patterns to exclude specific files or directories
- Rich progress bars and colorized terminal output
- Comprehensive statistics and summary reports
- Type hints throughout for better IDE support

## Requirements

- Python 3.8 or higher
- pip package manager

## Installation

### Option 1: Install from source (recommended for development)

```bash
# Clone the repository
git clone https://github.com/onamfc/img-optimize.git
cd img-optimize

# Install in editable mode with dependencies
pip install -e .

# Or install with development dependencies for testing
pip install -e ".[dev]"
```

### Option 2: Install directly via pip

```bash
pip install git+https://github.com/onamfc/img-optimize.git
```

## Usage

After installation, you can use the `img-optimize` command from anywhere:

### Basic Usage

```bash
# Optimize all images in a directory
img-optimize /path/to/images

# Optimized images will be saved to /path/to/images/optimized/
```

### Advanced Options

```bash
# Specify custom output directory
img-optimize /path/to/images --output /path/to/output

# Set JPEG/WebP quality (1-100, default: 85)
img-optimize /path/to/images --quality 90

# Process subdirectories recursively
img-optimize /path/to/images --recursive

# Preview compression without saving files (dry-run)
img-optimize /path/to/images --dry-run

# Optimize in-place (overwrite originals)
img-optimize /path/to/images --in-place

# Resize large images during optimization
img-optimize /path/to/images --max-width 1920 --max-height 1080

# Use parallel processing for faster optimization
img-optimize /path/to/images --workers 4

# Skip specific files or patterns
img-optimize /path/to/images --skip "*.draft.*" --skip "*/temp/*"

# Save detailed logs to file
img-optimize /path/to/images --log-file optimize.log

# Use a config file for project defaults
img-optimize /path/to/images --config .img-optimize.yaml

# Combine multiple options
img-optimize ./photos -o ./compressed -q 80 -r -w 4 --max-width 2000
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `INPUT_DIR` | Directory containing images to optimize (required) |
| `-o, --output` | Output directory (default: INPUT_DIR/optimized) |
| `-q, --quality` | JPEG/WebP quality level 1-100 (default: 85) |
| `-r, --recursive` | Process subdirectories recursively |
| `-d, --dry-run` | Preview results without saving files |
| `-i, --in-place` | Optimize images in place (overwrite originals) |
| `--max-width` | Maximum width in pixels (resize if larger) |
| `--max-height` | Maximum height in pixels (resize if larger) |
| `-w, --workers` | Number of parallel workers (default: 1) |
| `--skip` | Skip files matching pattern (can be used multiple times) |
| `--log-file` | Save detailed logs to file |
| `--config` | Path to config file (.img-optimize.yaml) |
| `--help` | Show help message |

### Examples

```bash
# Optimize images with 90% quality, save to custom folder
img-optimize ./photos --output ./photos-optimized --quality 90

# Recursively optimize all images in subdirectories
img-optimize ./images --recursive

# Test optimization without modifying files
img-optimize ./test-images --dry-run

# Optimize in place with 4 parallel workers
img-optimize ./photos --in-place --workers 4

# Resize and optimize for web (max 1920px wide)
img-optimize ./raw-photos --max-width 1920 --quality 85

# Skip draft files and temporary folders
img-optimize ./project --skip "*.draft.*" --skip "*/temp/*" --recursive

# Use config file for consistent settings
img-optimize ./photos --config .img-optimize.yaml
```

### Configuration File

Create a `.img-optimize.yaml` file in your project directory for default settings:

```yaml
# .img-optimize.yaml
quality: 85
max_width: 2000
max_height: 2000
workers: 4
skip:
  - "*.draft.*"
  - "*/temp/*"
  - "*/backup/*"
```

Then simply run:
```bash
img-optimize ./images --recursive
```

## Supported Formats

- PNG (.png, .PNG)
- JPEG (.jpg, .jpeg, .JPG, .JPEG)
- WebP (.webp, .WEBP)

## Development

### Running Tests

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=img_optimize
```

### Project Structure

```
img-optimize/
├── src/
│   └── img_optimize/
│       ├── __init__.py
│       ├── cli.py          # Command-line interface
│       ├── optimizer.py    # Image optimization logic
│       └── utils.py        # Utility functions
├── tests/                  # Test suite
├── pyproject.toml          # Project configuration
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
