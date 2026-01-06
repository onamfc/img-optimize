# img-optimize

A simple CLI tool for batch optimizing PNG and JPEG images while preserving quality

## Features

- Batch process all PNG and JPEG files in a specified directory
- Compress images with configurable quality levels (default: 85 for JPEG, optimize for PNG)
- Preserve original EXIF metadata and file timestamps
- Display compression statistics: original size, optimized size, and percentage saved
- Create optimized files in output directory (preserving original files)
- Show progress bar for batch operations using rich library
- Support recursive directory processing with --recursive flag
- Dry-run mode to preview compression results without saving files
- Summary report showing total space saved across all processed images
- Skip already optimized files that would increase in size
- Colorized terminal output for better readability

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

# Set JPEG quality (1-100, default: 85)
img-optimize /path/to/images --quality 90

# Process subdirectories recursively
img-optimize /path/to/images --recursive

# Preview compression without saving files (dry-run)
img-optimize /path/to/images --dry-run

# Combine options
img-optimize /path/to/images -o ./compressed -q 80 -r
```

### Command-Line Options

- `INPUT_DIR` - Directory containing images to optimize (required)
- `-o, --output` - Output directory (default: INPUT_DIR/optimized)
- `-q, --quality` - JPEG quality level from 1-100 (default: 85)
- `-r, --recursive` - Process subdirectories recursively
- `-d, --dry-run` - Preview results without saving files
- `--help` - Show help message

### Examples

```bash
# Optimize images with 90% quality, save to custom folder
img-optimize ./photos --output ./photos-optimized --quality 90

# Recursively optimize all images in subdirectories
img-optimize ./images --recursive

# Test optimization without modifying files
img-optimize ./test-images --dry-run
```

## Supported Formats

- PNG (.png, .PNG)
- JPEG (.jpg, .jpeg, .JPG, .JPEG)

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
