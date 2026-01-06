"""img-optimize: A CLI tool for batch optimizing PNG, JPEG, and WebP images."""

__version__ = "2.0.0"
__author__ = "img-optimize"
__all__ = ["ImageOptimizer", "optimize"]

from .optimizer import ImageOptimizer
from .cli import optimize
