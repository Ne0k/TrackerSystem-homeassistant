"""Shared base entity: links every entity to a vehicle device."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import TrackerSystemCoordinator


class TrackerSystemEntity(CoordinatorEntity[TrackerSystemCoordinator]):
    """Base for all TrackerSystem entities (one device per IMEI)."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: TrackerSystemCoordinator, imei: str) -> None:
        super().__init__(coordinator)
        self._imei = imei

    @property
    def _data(self) -> dict:
        return (self.coordinator.data or {}).get(self._imei) or {}

    @property
    def available(self) -> bool:
        return super().available and self._imei in (self.coordinator.data or {})

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._imei)},
            name=self._data.get("name") or self._imei,
            manufacturer=MANUFACTURER,
            model="GPS-tracker",
        )
