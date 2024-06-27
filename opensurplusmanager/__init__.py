"""The Open Surplus Manager integration."""

from __future__ import annotations

from pyosmanager import OSMClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SENSOR]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
type OSMConfigEntry = ConfigEntry[OSMClient]  # noqa: F821


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: OSMConfigEntry) -> bool:
    """Set up Open Surplus Manager from a config entry."""

    # TODO 1. Create API instance
    client = OSMClient(entry.data["host"])

    # TODO 2. Validate the API connection (and authentication)
    result = await client.is_healthy()
    if not result:
        return False
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)
    entry.runtime_data = client
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: OSMConfigEntry) -> bool:
    """Unload a config entry."""
    await entry.runtime_data.close()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
