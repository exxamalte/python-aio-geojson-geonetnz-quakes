"""Test for the GeoNet NZ Quakes GeoJSON feed."""

import asyncio
import datetime
from http import HTTPStatus
from unittest import mock
from unittest.mock import ANY

from aio_geojson_client.consts import UPDATE_OK
from aio_geojson_client.exceptions import GeoJsonException
import aiohttp
import pytest
import pytz

from aio_geojson_geonetnz_quakes.consts import ATTRIBUTION
from aio_geojson_geonetnz_quakes.feed import GeonetnzQuakesFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_update_ok(mock_aioresponse):
    """Test updating feed is ok."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://api.geonet.org.nz/quake?MMI=5",
        status=HTTPStatus.OK,
        body=load_fixture("quakes-1.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = GeonetnzQuakesFeed(websession, home_coordinates, mmi=5)
        assert (
            repr(feed) == "<GeonetnzQuakesFeed(home=(-41.2, 174.7), "
            "url=https://api.geonet.org.nz/quake?MMI=5, "
            "radius=None, magnitude=None, time=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 3

        feed_entry = entries[0]
        assert feed_entry is not None
        assert feed_entry.title == "Locality 1"
        assert feed_entry.external_id == "2019p111111"
        assert feed_entry.coordinates[0] == pytest.approx(-38.07928467)
        assert feed_entry.coordinates[1] == pytest.approx(178.2567291)
        assert round(abs(feed_entry.distance_to_home - 461.6), 1) == 0
        assert repr(feed_entry) == "<GeonetnzQuakesFeedEntry(id=2019p111111)>"
        assert feed_entry.attribution == ATTRIBUTION
        assert feed_entry.depth == 5.920121193
        assert feed_entry.magnitude == 5.020958811
        assert feed_entry.mmi == 5
        assert feed_entry.locality == "Locality 1"
        assert feed_entry.quality == "best"
        assert feed_entry.time == datetime.datetime(
            2019, 7, 24, 18, 0, 0, tzinfo=pytz.utc
        )

        feed_entry = entries[1]
        assert feed_entry is not None
        assert feed_entry.title == "Locality 2"
        assert feed_entry.external_id == "2019p222222"
        assert feed_entry.depth == 0.0

        feed_entry = entries[2]
        assert feed_entry is not None
        assert feed_entry.time is None


@pytest.mark.asyncio
async def test_update_ok_with_minimum_magnitude_filter(mock_aioresponse):
    """Test updating feed is ok with minimum magnitude filter."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://api.geonet.org.nz/quake?MMI=5",
        status=HTTPStatus.OK,
        body=load_fixture("quakes-1.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = GeonetnzQuakesFeed(
            websession, home_coordinates, mmi=5, filter_minimum_magnitude=5.5
        )
        assert (
            repr(feed) == "<GeonetnzQuakesFeed(home=(-41.2, 174.7), "
            "url=https://api.geonet.org.nz/quake?MMI=5, "
            "radius=None, magnitude=5.5, time=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry is not None
        assert feed_entry.title == "Locality 2"
        assert feed_entry.external_id == "2019p222222"
        assert feed_entry.coordinates[0] == pytest.approx(-38.467079)
        assert feed_entry.coordinates[1] == pytest.approx(178.291257)
        assert round(abs(feed_entry.distance_to_home - 431.6), 1) == 0
        assert repr(feed_entry) == "<GeonetnzQuakesFeedEntry(id=2019p222222)>"

        feed_entry = entries[1]
        assert feed_entry is not None
        assert feed_entry.external_id == "2019p333333"


@pytest.mark.asyncio
async def test_update_ok_with_time_filter(mock_aioresponse):
    """Test updating feed is ok with time filter."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://api.geonet.org.nz/quake?MMI=5",
        status=HTTPStatus.OK,
        body=load_fixture("quakes-1.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        fixed_now = datetime.datetime(2019, 7, 24, 19, 30, 0, tzinfo=pytz.utc)

        feed = GeonetnzQuakesFeed(
            websession, home_coordinates, mmi=5, filter_time=datetime.timedelta(hours=1)
        )
        # Test if "now" is computed correctly, before patchinng it.
        before_now_call = datetime.datetime.now(pytz.utc)
        computed_now = feed._now()  # noqa: SLF001
        after_now_call = datetime.datetime.now(pytz.utc)
        assert before_now_call <= computed_now <= after_now_call

        with mock.patch(
            "aio_geojson_geonetnz_quakes.feed." "GeonetnzQuakesFeed._now"
        ) as mock_now:
            mock_now.return_value = fixed_now
            assert (
                repr(feed) == "<GeonetnzQuakesFeed(home=(-41.2, 174.7), "
                "url=https://api.geonet.org.nz/quake?"
                "MMI=5, radius=None, magnitude=None, "
                "time=1:00:00)>"
            )
            status, entries = await feed.update()
            assert status == UPDATE_OK
            assert entries is not None
            assert len(entries) == 1

            feed_entry = entries[0]
            assert feed_entry is not None
            assert feed_entry.external_id == "2019p222222"
            assert repr(feed_entry) == "<GeonetnzQuakesFeedEntry(" "id=2019p222222)>"


@pytest.mark.asyncio
async def test_empty_feed(mock_aioresponse):
    """Test updating feed is ok when feed does not contain any entries."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://api.geonet.org.nz/quake?MMI=5",
        status=HTTPStatus.OK,
        body=load_fixture("quakes-2.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = GeonetnzQuakesFeed(websession, home_coordinates, mmi=5)
        assert (
            repr(feed) == "<GeonetnzQuakesFeed(home=(-41.2, 174.7), "
            "url=https://api.geonet.org.nz/quake?MMI=5, "
            "radius=None, magnitude=None, time=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 0
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_invalid_mmi():
    """Test with invalid parameter."""
    with pytest.raises(GeoJsonException):
        GeonetnzQuakesFeed(ANY, ANY, mmi=10)
