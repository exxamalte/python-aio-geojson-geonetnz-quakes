"""Test for the GeoNet NZ Quakes GeoJSON general setup."""

from aio_geojson_geonetnz_quakes import __version__


def test_version():
    """Test for version tag."""
    assert __version__ is not None
