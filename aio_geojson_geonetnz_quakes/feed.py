"""GeoNet NZ Quakes feed."""

from __future__ import annotations

from datetime import datetime
import logging

from aio_geojson_client.exceptions import GeoJsonException
from aio_geojson_client.feed import GeoJsonFeed
from aiohttp import ClientSession
from geojson import FeatureCollection
import pytz

from aio_geojson_geonetnz_quakes.consts import URL_TEMPLATE, VALID_MMI

from .feed_entry import GeonetnzQuakesFeedEntry

_LOGGER = logging.getLogger(__name__)


class GeonetnzQuakesFeed(GeoJsonFeed):
    """GeoNet NZ Quakes feed."""

    def __init__(
        self,
        websession: ClientSession,
        home_coordinates: tuple[float, float],
        mmi: int = -1,
        filter_radius: float | None = None,
        filter_minimum_magnitude: float | None = None,
        filter_time: datetime | None = None,
    ):
        """Initialise this service."""
        if mmi in VALID_MMI:
            url = URL_TEMPLATE.format(mmi)
            super().__init__(
                websession, home_coordinates, url, filter_radius=filter_radius
            )
            self._filter_minimum_magnitude = filter_minimum_magnitude
            self._filter_time = filter_time
        else:
            _LOGGER.error("Invalid MMI provided %s", mmi)
            raise GeoJsonException(f"Minimum MMI must be one of {VALID_MMI}")

    def __repr__(self):
        """Return string representation of this feed."""
        return f"<{self.__class__.__name__}(home={self._home_coordinates}, url={self._url}, radius={self._filter_radius}, magnitude={self._filter_minimum_magnitude}, time={self._filter_time})>"

    def _new_entry(self, home_coordinates, feature, global_data):
        """Generate a new entry."""
        return GeonetnzQuakesFeedEntry(home_coordinates, feature)

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        filtered_entries = super()._filter_entries(entries)
        if self._filter_minimum_magnitude:
            # Return only entries that have an actual magnitude value, and
            # the value is equal or above the defined threshold.
            filtered_entries = list(
                filter(
                    lambda entry: entry.magnitude
                    and entry.magnitude >= self._filter_minimum_magnitude,
                    filtered_entries,
                )
            )
        if self._filter_time:
            # Return only entries that have a time value, and that value is
            # between now and now-time interval.
            now = self._now()
            filtered_entries = list(
                filter(
                    lambda entry: entry.time
                    and (now - self._filter_time <= entry.time <= now),
                    filtered_entries,
                )
            )
        return filtered_entries

    def _now(self) -> datetime:
        """Return now with timezone."""
        return datetime.now(pytz.utc)

    def _extract_last_timestamp(
        self, feed_entries: list[GeonetnzQuakesFeedEntry]
    ) -> datetime | None:
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates = sorted(
                filter(None, [entry.time for entry in feed_entries]), reverse=True
            )
            return dates[0]
        return None

    def _extract_from_feed(self, feed: FeatureCollection) -> dict | None:
        """Extract global metadata from feed."""
        return None
