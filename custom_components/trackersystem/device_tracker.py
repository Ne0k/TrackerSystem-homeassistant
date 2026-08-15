"""Device tracker: shows the vehicle on the HA map."""
from __future__ import annotations

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_DEVICES, DOMAIN
from .entity import TrackerSystemEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    imeis = entry.data.get(CONF_DEVICES) or list(coordinator.data or {})
    async_add_entities(TrackerSystemTracker(coordinator, imei) for imei in imeis)


class TrackerSystemTracker(TrackerSystemEntity, TrackerEntity):
    """GPS position of a vehicle."""

    _attr_name = None  # use the device name
    _attr_icon = "mdi:car"

    def __init__(self, coordinator, imei: str) -> None:
        super().__init__(coordinator, imei)
        self._attr_unique_id = f"{imei}_tracker"

    @property
    def source_type(self) -> SourceType:
        return SourceType.GPS

    @property
    def latitude(self) -> float | None:
        return self._data.get("lat")

    @property
    def longitude(self) -> float | None:
        return self._data.get("lng")

    @property
    def extra_state_attributes(self) -> dict:
        d = self._data
        return {
            "speed_kmh": d.get("speed_kmh"),
            "course": d.get("course"),
            "altitude_m": d.get("altitude_m"),
            "last_seen": d.get("last_seen"),
            "imei": self._imei,
        }
