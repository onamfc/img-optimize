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

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/img-optimize.git
cd img-optimize

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python using click

## Dependencies

- `click`
- `Pillow`
- `rich`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
