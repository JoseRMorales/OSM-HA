"""Coordinator for OpenSurplusManager."""

from pyosmanager import OSMClient

from homeassistant.config_entries import ConfigEntry

from .core import OSMCore
from .device import OSMDevice

type OSMConfigEntry = ConfigEntry[OSMCoordinator]


class OSMCoordinator:
    """Representation of a OpenSurplusManager Coordinator in order to get share the core and device object between platforms."""

    def __init__(self, client: OSMClient, core: OSMCore, devices: list[OSMDevice]):
        """Initialize the coordinator."""
        self.client = client
        self.core = core
        self.devices = devices
