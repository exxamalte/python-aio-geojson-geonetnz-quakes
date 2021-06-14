"""GeoNet NZ Quakes feed entry."""
import logging
from datetime import datetime
from typing import Optional, Tuple

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

    def __init__(self, home_coordinates: Tuple[float, float], feature: Feature):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return ATTRIBUTION

    @property
    def external_id(self) -> Optional[str]:
        """Return the external id of this entry."""
        return self._search_in_properties(ATTR_PUBLICID)

    @property
    def title(self) -> Optional[str]:
        """Return the title of this entry."""
        return self.locality

    @property
    def depth(self) -> Optional[float]:
        """Return the depth of this entry."""
        return self._search_in_properties(ATTR_DEPTH)

    @property
    def magnitude(self) -> Optional[float]:
        """Return the magnitude of this entry."""
        return self._search_in_properties(ATTR_MAGNITUDE)

    @property
    def mmi(self) -> Optional[int]:
        """Return the MMI of this entry."""
        return self._search_in_properties(ATTR_MMI)

    @property
    def locality(self) -> Optional[str]:
        """Return the locality of this entry."""
        return self._search_in_properties(ATTR_LOCALITY)

    @property
    def quality(self) -> Optional[str]:
        """Return the quality of this entry."""
        return self._search_in_properties(ATTR_QUALITY)

    @property
    def time(self) -> Optional[datetime]:
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
