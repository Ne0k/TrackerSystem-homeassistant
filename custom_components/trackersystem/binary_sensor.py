"""Binary sensors: ignition (on/off) and online status."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_DEVICES, DOMAIN
from .entity import TrackerSystemEntity

BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="ignition",
        name="Ignition",
        device_class=BinarySensorDeviceClass.RUNNING,
        icon="mdi:key-variant",
    ),
    BinarySensorEntityDescription(
        key="online",
        name="Online",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    imeis = entry.data.get(CONF_DEVICES) or list(coordinator.data or {})
    entities = [
        TrackerSystemBinarySensor(coordinator, imei, desc)
        for imei in imeis
        for desc in BINARY_SENSORS
    ]
    async_add_entities(entities)


class TrackerSystemBinarySensor(TrackerSystemEntity, BinarySensorEntity):
    """On/off state of a vehicle."""

    def __init__(self, coordinator, imei: str, description) -> None:
        super().__init__(coordinator, imei)
        self.entity_description = description
        self._attr_unique_id = f"{imei}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        val = self._data.get(self.entity_description.key)
        return None if val is None else bool(val)
