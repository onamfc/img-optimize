"""Tests for utility functions."""
import pytest
from img_optimize.utils import format_size, calculate_savings


class TestFormatSize:
    def test_bytes(self):
        assert format_size(500) == "500.00 B"
    
    def test_kilobytes(self):
        assert format_size(2048) == "2.00 KB"
    
    def test_megabytes(self):
        assert format_size(5242880) == "5.00 MB"
    
    def test_gigabytes(self):
        assert format_size(1073741824) == "1.00 GB"
    
    def test_zero(self):
        assert format_size(0) == "0.00 B"


class TestCalculateSavings:
    def test_fifty_percent_savings(self):
        assert calculate_savings(1000, 500) == 50.0
    
    def test_no_savings(self):
        assert calculate_savings(1000, 1000) == 0.0
    
    def test_zero_original(self):
        assert calculate_savings(0, 0) == 0.0
    
    def test_high_savings(self):
        result = calculate_savings(1000, 100)
        assert result == 90.0
