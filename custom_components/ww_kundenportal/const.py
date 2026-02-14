DOMAIN = "ww_kundenportal"
DEFAULT_NAME = "Westfalen Weser"
SCAN_INTERVAL_MINUTES = 60

CONF_USERNAME = "username"
CONF_PASSWORD = "password"

PLATFORMS = ["sensor"]

# Sensor Types
SENSOR_PURCHASE = "purchase"
SENSOR_FEED_IN = "feed_in"

SENSOR_TYPES = {
    SENSOR_PURCHASE: {
        "name": "Strombezug",
        "icon": "mdi:transmission-tower",
        "key": "reading_purchase_kwh",
    },
    SENSOR_FEED_IN: {
        "name": "Stromeinspeisung",
        "icon": "mdi:solar-power",
        "key": "reading_feed_in_kwh",
    },
}
