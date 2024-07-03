"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, UnitOfPower
from homeassistant.core import CoreState, HomeAssistant

from .const import DOMAIN
from .coordinator import OSMConfigEntry
from .core import OSMCore
from .device import OSMDevice


async def async_setup_entry(
    hass: HomeAssistant, entry: OSMConfigEntry, async_add_entities
):
    """Add sensors for passed config_entry in HA."""
    coordinator = entry.runtime_data

    entities = [ConsumptionSensor(device) for device in coordinator.devices]

    entities.append(SurplusSensor(coordinator.core))

    async_add_entities(entities)


class ConsumptionSensor(SensorEntity):
    """Representation of a consumption sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, device: OSMDevice) -> None:
        """Initialize the sensor."""
        self._device = device
        self._attr_unique_id = f"{device.device_name}_consumption"
        self._attr_name = "Consumption"

    async def async_added_to_hass(self) -> None:
        """Handle when entity is added."""
        if self.hass.state is not CoreState.running:
            self.hass.bus.async_listen_once(
                EVENT_HOMEASSISTANT_STARTED, self.first_update
            )
        else:
            await self.first_update()

    async def first_update(self, _=None) -> None:
        """Run first update and write state."""
        await self.async_update()
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update the sensor."""
        await self._device.async_update()

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self._device.consumption

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_name)},
            "name": self._device.device_name,
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._device.consumption is not None


class SurplusSensor(SensorEntity):
    """Representation of a consumption sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, core: OSMCore) -> None:
        """Initialize the sensor."""
        self._core = core
        self._attr_unique_id = "surplus"
        self._attr_name = "Surplus"

    async def async_added_to_hass(self) -> None:
        """Handle when entity is added."""
        if self.hass.state is not CoreState.running:
            self.hass.bus.async_listen_once(
                EVENT_HOMEASSISTANT_STARTED, self.first_update
            )
        else:
            await self.first_update()

    async def first_update(self, _=None) -> None:
        """Run first update and write state."""
        await self.async_update()
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update the sensor."""
        await self._core.async_update()

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self._core.surplus

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, "core")},
            "name": "Core",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._core.surplus is not None
