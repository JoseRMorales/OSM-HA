"""Platform for sensor integration."""

from __future__ import annotations

import logging

from pyosmanager import APIError, OSMClient

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, UnitOfPower
from homeassistant.core import CoreState

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    client: OSMClient
    devices = await client.get_devices()
    entities = [ConsumptionSensor(OSMDevice(client, device.name)) for device in devices]

    surplus = OSMSurplus(client)
    entities.append(SurplusSensor(surplus))

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
        self._attr_name = f"{device.device_name} Consumption"

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


class OSMDevice:
    """Base representation of a OpenSurplusManager Device."""

    def __init__(self, client: OSMClient, device_name: str):
        """Initialize the device."""
        self.client = client
        self.device_name = device_name
        self.consumption: float | None = None

    async def async_update(self):
        """Update the device."""
        try:
            self.consumption = await self.client.get_device_consumption(
                self.device_name
            )
        except APIError:
            self.consumption = None


class SurplusSensor(SensorEntity):
    """Representation of a consumption sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, surplus: OSMSurplus) -> None:
        """Initialize the sensor."""
        self._surplus = surplus
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
        await self._surplus.async_update()

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self._surplus.surplus

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, "surplus")},
            "name": "Surplus",
        }


class OSMSurplus:
    """Base representation of a OpenSurplusManager Surplus."""

    def __init__(self, client: OSMClient):
        """Initialize the surplus."""
        self.client = client
        self.surplus: float | None = None

    async def async_update(self):
        """Update the surplus."""
        try:
            self.surplus = await self.client.get_surplus()
        except APIError:
            self.surplus = None
