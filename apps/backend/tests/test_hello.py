"""Hello unit test module."""

from src.main import hello


def test_hello():
    """Test the hello function."""
    assert hello() == "Hello ai"
