"""Sensor-entiteiten: accu, tank, spanning, snelheid, kilometerstand."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricPotential,
    UnitOfLength,
    UnitOfSpeed,
    UnitOfVolume,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_DEVICES, DOMAIN
from .entity import TrackerSystemEntity


@dataclass(frozen=True, kw_only=True)
class TSSensor(SensorEntityDescription):
    """Sensor description; always=True → always create, otherwise only when data is present."""

    always: bool = False


SENSORS: tuple[TSSensor, ...] = (
    TSSensor(
        key="battery_pct",
        translation_key="battery",
        name="Battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    TSSensor(
        key="fuel_pct",
        name="Fuel level",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:fuel",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    TSSensor(
        key="fuel_l",
        name="Fuel",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        icon="mdi:fuel",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    TSSensor(
        key="ext_voltage_v",
        name="Supply voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        always=True,
    ),
    TSSensor(
        key="speed_kmh",
        name="Speed",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        always=True,
    ),
    TSSensor(
        key="odometer_km",
        name="Odometer",
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
        always=True,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    imeis = entry.data.get(CONF_DEVICES) or list(coordinator.data or {})
    entities: list[SensorEntity] = []
    for imei in imeis:
        data = (coordinator.data or {}).get(imei) or {}
        for desc in SENSORS:
            if desc.always or data.get(desc.key) is not None:
                entities.append(TrackerSystemSensor(coordinator, imei, desc))
    async_add_entities(entities)


class TrackerSystemSensor(TrackerSystemEntity, SensorEntity):
    """A single sensor value of a vehicle."""

    entity_description: TSSensor

    def __init__(self, coordinator, imei: str, description: TSSensor) -> None:
        super().__init__(coordinator, imei)
        self.entity_description = description
        self._attr_unique_id = f"{imei}_{description.key}"

    @property
    def native_value(self):
        return self._data.get(self.entity_description.key)
