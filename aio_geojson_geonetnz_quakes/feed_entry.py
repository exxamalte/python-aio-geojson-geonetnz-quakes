"""GeoNet NZ Quakes feed entry."""
from __future__ import annotations

import logging
from datetime import datetime

import pytz
from aio_geojson_client.feed_entry import FeedEntry
from geojson import Feature

from .consts import (
    ATTR_DEPTH,
    ATTR_LOCALITY,
    ATTR_MAGNITUDE,
    ATTR_MMI,
    ATTR_PUBLICID,
    ATTR_QUALITY,
    ATTR_TIME,
    ATTRIBUTION,
)

_LOGGER = logging.getLogger(__name__)


class GeonetnzQuakesFeedEntry(FeedEntry):
    """GeoNet NZ Quakes feed entry."""

    def __init__(self, home_coordinates: tuple[float, float], feature: Feature):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return ATTRIBUTION

    @property
    def external_id(self) -> str | None:
        """Return the external id of this entry."""
        return self._search_in_properties(ATTR_PUBLICID)

    @property
    def title(self) -> str | None:
        """Return the title of this entry."""
        return self.locality

    @property
    def depth(self) -> float | None:
        """Return the depth of this entry."""
        return self._search_in_properties(ATTR_DEPTH)

    @property
    def magnitude(self) -> float | None:
        """Return the magnitude of this entry."""
        return self._search_in_properties(ATTR_MAGNITUDE)

    @property
    def mmi(self) -> int | None:
        """Return the MMI of this entry."""
        return self._search_in_properties(ATTR_MMI)

    @property
    def locality(self) -> str | None:
        """Return the locality of this entry."""
        return self._search_in_properties(ATTR_LOCALITY)

    @property
    def quality(self) -> str | None:
        """Return the quality of this entry."""
        return self._search_in_properties(ATTR_QUALITY)

    @property
    def time(self) -> datetime | None:
        """Return the time of this entry."""
        time_str = self._search_in_properties(ATTR_TIME)
        if time_str:
            # 'Z' means UTC timezone.
            time = pytz.utc.localize(
                datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            )
            _LOGGER.debug("Time parsed: %s", time)
            return time
        return None
