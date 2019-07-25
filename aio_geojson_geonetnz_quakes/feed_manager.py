"""Feed Manager for GeoNet NZ Quakes feed."""
from aio_geojson_client.feed_manager import FeedManagerBase
from aiohttp import ClientSession

from .feed import GeonetnzQuakesFeed


class GeonetnzQuakesFeedManager(FeedManagerBase):
    """Feed Manager for GeoNet NZ Quakes feed."""

    def __init__(self, websession: ClientSession, generate_callback,
                 update_callback, remove_callback,
                 coordinates, mmi=-1, filter_radius=None,
                 filter_minimum_magnitude=None):
        """Initialize the Qld Bushfire Alert Feed Manager."""
        feed = GeonetnzQuakesFeed(
            websession,
            coordinates,
            mmi=mmi,
            filter_radius=filter_radius,
            filter_minimum_magnitude=filter_minimum_magnitude)
        super().__init__(feed, generate_callback, update_callback,
                         remove_callback)
