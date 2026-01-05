"""Helper utilities for file operations and statistics."""

def format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def calculate_savings(original, optimized):
    """Calculate percentage saved."""
    if original == 0:
        return 0.0
    return ((original - optimized) / original) * 100
