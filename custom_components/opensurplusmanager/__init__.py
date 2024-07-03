"""The Open Surplus Manager integration."""

from __future__ import annotations

import asyncio

from pyosmanager import OSMClient

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, SEMAPHORE
from .coordinator import OSMConfigEntry, OSMCoordinator
from .core import OSMCore
from .device import OSMDevice

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.NUMBER]


async def async_setup_entry(hass: HomeAssistant, entry: OSMConfigEntry) -> bool:
    """Set up Open Surplus Manager from a config entry."""
    if SEMAPHORE not in hass.data.setdefault(DOMAIN, {}):
        hass.data.setdefault(DOMAIN, {})[SEMAPHORE] = asyncio.Semaphore(1)
    client = OSMClient(entry.data["host"])

    result = await client.is_healthy()
    if not result:
        return False

    devices = await client.get_devices()
    devices = [OSMDevice(client, device.name) for device in devices]
    core = OSMCore(client)
    coordinator = OSMCoordinator(client, core, devices)

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: OSMConfigEntry) -> bool:
    """Unload a config entry."""
    await entry.runtime_data.client.close()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
