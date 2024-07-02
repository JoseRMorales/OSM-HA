"""Support for Open Surplus Manager binary sensors."""

from pyosmanager import OSMClient

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import CoreState

from .const import DOMAIN
from .device import OSMDevice


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    client: OSMClient
    devices = await client.get_devices()
    entities = [
        PoweredBinarySensor(OSMDevice(client, device.name)) for device in devices
    ]
    entities += [
        EnabledBinarySensor(OSMDevice(client, device.name)) for device in devices
    ]

    async_add_entities(entities)


class PoweredBinarySensor(BinarySensorEntity):
    """Representation of a consumption sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_device_class = BinarySensorDeviceClass.POWER

    def __init__(self, device: OSMDevice) -> None:
        """Initialize the sensor."""
        self._device = device
        self._attr_unique_id = f"{device.device_name}_powered"
        self._attr_name = "Power State"

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
    def is_on(self) -> bool | None:
        """Return the state of the sensor."""
        return self._device.powered

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_name)},
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._device.powered is not None


class EnabledBinarySensor(BinarySensorEntity):
    """Representation of a consumption sensor."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device: OSMDevice) -> None:
        """Initialize the sensor."""
        self._device = device
        self._attr_unique_id = f"{device.device_name}_enabled"
        self._attr_name = "Enabled"

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
    def is_on(self) -> bool | None:
        """Return the state of the sensor."""
        return self._device.enabled

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_name)},
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._device.enabled is not None
