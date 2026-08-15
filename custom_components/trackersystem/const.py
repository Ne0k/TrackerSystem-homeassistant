"""Constanten voor de TrackerSystem-integratie."""

DOMAIN = "trackersystem"

CONF_BASE_URL = "base_url"
CONF_API_KEY = "api_key"
CONF_DEVICES = "devices"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 300  # seconden

MANUFACTURER = "TrackerSystem"
API_LIST_PATH = "/api/ext/devices?full=1"
