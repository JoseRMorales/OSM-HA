"""Support for Open Surplus Manager number entities."""

from pyosmanager import OSMClient

from homeassistant.components.number import NumberDeviceClass, NumberEntity
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, UnitOfPower, UnitOfTime
from homeassistant.core import CoreState

from .const import DOMAIN
from .core import OSMCore
from .device import OSMDevice


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    client: OSMClient

    core = OSMCore(client)

    entities = [
        GridMarginNumber(core),
        SurplusMarginNumber(core),
        IdlePowerNumber(core),
    ]

    devices = await client.get_devices()
    for device in devices:
        entities.append(DeviceMaxConsumptionNumber(OSMDevice(client, device.name)))
        entities.append(DeviceExpectedConsumptionNumber(OSMDevice(client, device.name)))
        entities.append(DeviceCooldownNumber(OSMDevice(client, device.name)))

    async_add_entities(entities)


class GridMarginNumber(NumberEntity):
    """Representation of a grid margin sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = NumberDeviceClass.POWER
    _attr_native_max_value = 10000

    def __init__(self, core: OSMCore) -> None:
        """Initialize the sensor."""
        self._core = core
        self._attr_unique_id = "grid_margin"
        self._attr_name = "Grid Margin"

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

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self._core.client.set_grid_margin(value)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._core.grid_margin is not None

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self._core.grid_margin

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, "core")},
        }


class SurplusMarginNumber(NumberEntity):
    """Representation of a surplus margin sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = NumberDeviceClass.POWER
    _attr_native_max_value = 10000

    def __init__(self, core: OSMCore) -> None:
        """Initialize the sensor."""
        self._core = core
        self._attr_unique_id = "surplus_margin"
        self._attr_name = "Surplus Margin"

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

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self._core.client.set_surplus_margin(value)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._core.surplus_margin is not None

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self._core.surplus_margin

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, "core")},
        }


class IdlePowerNumber(NumberEntity):
    """Representation of a idle power sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = NumberDeviceClass.POWER
    _attr_native_max_value = 10000

    def __init__(self, core: OSMCore) -> None:
        """Initialize the sensor."""
        self._core = core
        self._attr_unique_id = "idle_power"
        self._attr_name = "Idle Power"

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

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self._core.client.set_idle_power(value)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._core.idle_power is not None

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self._core.idle_power

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, "core")},
        }


class DeviceMaxConsumptionNumber(NumberEntity):
    """Representation of a device max consumption sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = NumberDeviceClass.POWER
    _attr_native_max_value = 10000

    def __init__(self, device: OSMDevice) -> None:
        """Initialize the sensor."""
        self._device = device
        self._attr_unique_id = f"{device.device_name}_max_consumption"
        self._attr_name = "Max Consumption"

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

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self._device.async_set_max_consumption(value)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._device.max_consumption is not None

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self._device.max_consumption

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_name)},
        }


class DeviceExpectedConsumptionNumber(NumberEntity):
    """Representation of a device expected consumption sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = NumberDeviceClass.POWER
    _attr_native_max_value = 10000

    def __init__(self, device: OSMDevice) -> None:
        """Initialize the sensor."""
        self._device = device
        self._attr_unique_id = f"{device.device_name}_expected_consumption"
        self._attr_name = "Expected Consumption"

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

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self._device.async_set_expected_consumption(value)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._device.expected_consumption is not None

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self._device.expected_consumption

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_name)},
        }


class DeviceCooldownNumber(NumberEntity):
    """Representation of a device cooldown sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_unit_of_measurement = UnitOfTime.SECONDS
    _attr_device_class = NumberDeviceClass.DURATION
    _attr_native_max_value = 10000

    def __init__(self, device: OSMDevice) -> None:
        """Initialize the sensor."""
        self._device = device
        self._attr_unique_id = f"{device.device_name}_cooldown"
        self._attr_name = "Cooldown"

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

    async def async_set_native_value(self, value: int) -> None:
        """Update the current value."""
        await self._device.async_set_cooldown(value)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._device.cooldown is not None

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self._device.cooldown

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_name)},
        }
