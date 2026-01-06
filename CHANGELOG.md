# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-06

### Added
- **WebP format support** - Optimize WebP images alongside PNG and JPEG
- **Parallel processing** - Use `--workers` flag to process images concurrently for faster optimization
- **Image resizing** - New `--max-width` and `--max-height` options to resize large images during optimization
- **In-place optimization** - Use `--in-place` flag to overwrite original files instead of creating copies
- **Config file support** - Create `.img-optimize.yaml` to set default options per project
- **Logging to file** - Use `--log-file` to save detailed logs for debugging
- **Skip patterns** - Use `--skip` to exclude specific files or patterns from processing
- **Comprehensive type hints** - Full type annotations throughout the codebase for better IDE support
- **Enhanced docstrings** - Detailed documentation for all functions and classes
- **Better error handling** - More descriptive error messages and proper logging

### Fixed
- **Critical bug**: Recursive processing now correctly maintains directory structure in output
- Files that would increase in size are now properly skipped with warnings

### Changed
- Improved CLI help text and option descriptions
- Refactored optimizer to support multiple formats more easily
- Better progress reporting with rich library
- Code quality improvements with constants extracted and better organization

### Documentation
- Updated README with comprehensive usage examples
- Added requirements.txt for easier dependency installation
- Updated pyproject.toml with new dependencies and dev tools

## [1.0.0] - 2026-01-04

### Added
- Initial release
- Basic PNG and JPEG optimization
- Recursive directory processing
- Dry-run mode for previewing optimizations
- Progress bar and summary statistics
- EXIF metadata preservation
- File timestamp preservation
- Configurable JPEG quality settings

[2.0.0]: https://github.com/onamfc/img-optimize/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/onamfc/img-optimize/releases/tag/v1.0.0
