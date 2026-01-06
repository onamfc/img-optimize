"""Tests for utility functions."""

import pytest

from img_optimize.utils import calculate_savings, format_size


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

    def test_complete_savings(self):
        """Test 100% savings (file reduced to 0)."""
        assert calculate_savings(1000, 0) == 100.0

    def test_fractional_savings(self):
        """Test savings with fractional percentages."""
        result = calculate_savings(1000, 750)
        assert result == 25.0

    def test_terabytes(self):
        """Test formatting terabytes."""
        assert "TB" in format_size(1099511627776)  # 1 TB

    def test_float_input(self):
        """Test that float inputs are handled correctly."""
        result = format_size(1536.5)
        assert "KB" in result
