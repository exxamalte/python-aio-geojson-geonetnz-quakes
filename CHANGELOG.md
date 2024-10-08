# Changes

## 0.17 (07/10/2024)
* Bump aio_geojson_client to 0.21.
* Removed Python 3.8 support.
* Code quality improvements.

## 0.16 (26/01/2024)
* Bumped version of upstream aio_geojson_client library to 0.20.
* Improved JSON parsing error handling, especially when not using Python's built-in JSON parsing library.
* Code quality improvements.
* Added Python 3.12 support.
* Removed Python 3.7 support.
* Bumped library versions: black, flake8, isort.
* Migrated to pytest.

## 0.15 (24/01/2023)
* Added Python 3.11 support.
* Removed deprecated asynctest dependency.
* Bumped version of upstream aio_geojson_client library to 0.18.

## 0.14 (17/02/2022)
* No functional changes.
* Added Python 3.10 support.
* Removed Python 3.6 support.
* Bumped version of upstream aio_geojson_client library to 0.16.
* Bumped library versions: black, flake8, isort.

## 0.13 (15/06/2021)
* Set aiohttp to a release 3.7.4 or later (thanks @fabaff).
* Add license tag (thanks @fabaff).
* Added Python 3.9 support.
* Bump aio_geojson_client to v0.14.
* Migrated to github actions.
* General code improvements.

## 0.12 (17/02/2020)
* Bumped version of upstream GeoJSON library.
* Internal code improvements.

## 0.11 (06/11/2019)
* Python 3.8 compatibility.

## 0.10 (24/09/2019)
* Bumped version of upstream GeoJSON library.

## 0.9 (14/08/2019)
* Bumped version of upstream GeoJSON library.

## 0.8 (13/08/2019)
* Bumped version of upstream GeoJSON library.
* Reset last timestamp when update fails.
* Add request timeout of 10 seconds.

## 0.7 (12/08/2019)
* Bumped version of upstream GeoJSON library.
* Added total number of managed entries to status callback info.

## 0.6 (10/08/2019)
* Bumped version of upstream GeoJSON library.
* Added ability for status update callback.

## 0.5 (06/08/2019)
* Fixed computation of "now" for filtering.
* Removed debug statements.

## 0.4 (30/07/2019)
* Parsing feed entry time as timezone aware.
* Support for filtering entries by time.

## 0.3 (29/07/2019)
* Bumped version of upstream GeoJSON library.

## 0.2 (26/07/2019)
* Bumped version of upstream GeoJSON library.

## 0.1 (25/07/2019)
* Initial release with support for GeoNet NZ Quakes feed.
