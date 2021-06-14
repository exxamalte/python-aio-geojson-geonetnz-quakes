"""Test for the GeoNet NZ Quakes GeoJSON feed manager."""
import datetime

import aiohttp
import pytest
import pytz

from aio_geojson_geonetnz_quakes.feed_manager import GeonetnzQuakesFeedManager
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_feed_manager(aresponses, event_loop):
    """Test the feed manager."""
    home_coordinates = (-41.2, 174.7)
    aresponses.add(
        "api.geonet.org.nz",
        "/quake?MMI=5",
        "get",
        aresponses.Response(text=load_fixture("quakes-1.json"), status=200),
        match_querystring=True,
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        async def _generate_entity(external_id):
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        async def _update_entity(external_id):
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        async def _remove_entity(external_id):
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        feed_manager = GeonetnzQuakesFeedManager(
            websession,
            _generate_entity,
            _update_entity,
            _remove_entity,
            home_coordinates,
            mmi=5,
        )
        assert (
            repr(feed_manager) == "<GeonetnzQuakesFeedManager("
            "feed=<GeonetnzQuakesFeed("
            "home=(-41.2, 174.7), url=https://"
            "api.geonet.org.nz/quake?MMI=5, "
            "radius=None, magnitude=None, "
            "time=None)>)>"
        )
        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 3
        assert feed_manager.last_timestamp == datetime.datetime(
            2019, 7, 24, 19, 0, 0, tzinfo=pytz.utc
        )
        assert len(generated_entity_external_ids) == 3
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0
