"""Helper utilities for file operations and statistics."""

from typing import List, Union

# Constants
BYTES_PER_KB: int = 1024
SIZE_UNITS: List[str] = ["B", "KB", "MB", "GB", "TB"]


def format_size(bytes_size: Union[int, float]) -> str:
    """Format bytes to human-readable size.

    Args:
        bytes_size: Size in bytes to format

    Returns:
        Formatted string with size and unit (e.g., "1.23 MB")

    Examples:
        >>> format_size(1024)
        '1.00 KB'
        >>> format_size(1536)
        '1.50 KB'
    """
    size = float(bytes_size)
    for unit in SIZE_UNITS[:-1]:
        if size < BYTES_PER_KB:
            return f"{size:.2f} {unit}"
        size /= BYTES_PER_KB
    return f"{size:.2f} {SIZE_UNITS[-1]}"


def calculate_savings(original: Union[int, float], optimized: Union[int, float]) -> float:
    """Calculate percentage saved from optimization.

    Args:
        original: Original file size in bytes
        optimized: Optimized file size in bytes

    Returns:
        Percentage of space saved (0-100)

    Examples:
        >>> calculate_savings(1000, 750)
        25.0
        >>> calculate_savings(100, 0)
        100.0
    """
    if original == 0:
        return 0.0
    return ((original - optimized) / original) * 100
