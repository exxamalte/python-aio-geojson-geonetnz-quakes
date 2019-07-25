"""GeoNet NZ Quakes constants."""

ATTR_DEPTH = "depth"
ATTR_LOCALITY = "locality"
ATTR_MAGNITUDE = "magnitude"
ATTR_MMI = "mmi"
ATTR_PUBLICID = "publicID"
ATTR_QUALITY = "quality"
ATTR_TIME = "time"

ATTRIBUTION = "GeoNet Geological hazard information for New Zealand"
URL_TEMPLATE = "https://api.geonet.org.nz/quake?MMI={}"
VALID_MMI = range(-1, 8)
