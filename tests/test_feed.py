"""Test for the geonet nz quakes geojson feed."""
import datetime
import re

import aiohttp
import pytest

from aio_geojson_client.consts import UPDATE_OK, UPDATE_ERROR
from aio_geojson_client.exceptions import GeoJsonException

from aio_geojson_geonetnz_quakes.consts import ATTRIBUTION
from aio_geojson_geonetnz_quakes.feed import GeonetnzQuakesFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_update_ok(aresponses, event_loop):
    """Test updating feed is ok."""
    home_coordinates = (-41.2, 174.7)
    aresponses.add(
        'api.geonet.org.nz',
        re.compile(r'/quake.*'),
        'get',
        aresponses.Response(text=load_fixture('quakes-1.json'),
                            status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = GeonetnzQuakesFeed(websession, home_coordinates, mmi=5)
        assert repr(feed) == "<GeonetnzQuakesFeed(home=(-41.2, 174.7), " \
                             "url=https://api.geonet.org.nz/quake?MMI=5, " \
                             "radius=None, magnitude=None)>"
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry is not None
        assert feed_entry.title == "Locality 1"
        assert feed_entry.external_id == "2019p111111"
        assert feed_entry.coordinates == (-38.07928467, 178.2567291)
        assert round(abs(feed_entry.distance_to_home - 461.6), 1) == 0
        assert repr(feed_entry) == "<GeonetnzQuakesFeedEntry(id=2019p111111)>"
        assert feed_entry.attribution == ATTRIBUTION
        assert feed_entry.depth == 5.920121193
        assert feed_entry.magnitude == 5.020958811
        assert feed_entry.mmi == 5
        assert feed_entry.locality == "Locality 1"
        assert feed_entry.quality == "best"
        assert feed_entry.time == datetime.datetime(2019, 7, 24, 18, 0, 0)

        feed_entry = entries[1]
        assert feed_entry is not None
        assert feed_entry.title == "Locality 2"
        assert feed_entry.external_id == "2019p222222"
        assert feed_entry.depth == 0.0


@pytest.mark.asyncio
async def test_update_ok_with_filter(aresponses, event_loop):
    """Test updating feed is ok with magnitude filter."""
    home_coordinates = (-41.2, 174.7)
    aresponses.add(
        "api.geonet.org.nz",
        re.compile(r"/quake.*"),
        "get",
        aresponses.Response(text=load_fixture('quakes-1.json'),
                            status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = GeonetnzQuakesFeed(websession, home_coordinates, mmi=5,
                                  filter_minimum_magnitude=5.5)
        assert repr(feed) == "<GeonetnzQuakesFeed(home=(-41.2, 174.7), " \
                             "url=https://api.geonet.org.nz/quake?MMI=5, " \
                             "radius=None, magnitude=5.5)>"
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry is not None
        assert feed_entry.title == "Locality 2"
        assert feed_entry.external_id == "2019p222222"
        assert feed_entry.coordinates == (-38.46707928, 178.2912567)
        assert round(abs(feed_entry.distance_to_home - 431.6), 1) == 0
        assert repr(feed_entry) == "<GeonetnzQuakesFeedEntry(id=2019p222222)>"


@pytest.mark.asyncio
async def test_empty_feed(aresponses, event_loop):
    """Test updating feed is ok when feed does not contain any entries."""
    home_coordinates = (-41.2, 174.7)
    aresponses.add(
        'api.geonet.org.nz',
        re.compile(r'/quake.*'),
        'get',
        aresponses.Response(text=load_fixture('quakes-2.json'),
                            status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = GeonetnzQuakesFeed(websession, home_coordinates, mmi=5)
        assert repr(feed) == "<GeonetnzQuakesFeed(home=(-41.2, 174.7), " \
                             "url=https://api.geonet.org.nz/quake?MMI=5, " \
                             "radius=None, magnitude=None)>"
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 0
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_invalid_mmi():
    """Test with invalid parameter."""
    with pytest.raises(GeoJsonException):
        GeonetnzQuakesFeed(None, None, mmi=10)
