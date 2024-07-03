"""Representation of a OpenSurplusManager Device."""

import asyncio

from pyosmanager import APIError, OSMClient


class OSMDevice:
    """Base representation of a OpenSurplusManager Device."""

    def __init__(self, client: OSMClient, device_name: str):
        """Initialize the device."""
        self.client = client
        self.device_name = device_name
        self.consumption: float | None = None
        self.powered: bool | None = None
        self.enabled: bool | None = None
        self.max_consumption: float | None = None
        self.expected_consumption: float | None = None
        self.cooldown: int | None = None
        self._initialized = False

    async def wait_for_initialization(self):
        """Wait until the core is initialized."""
        while not self._initialized:
            await asyncio.sleep(1)

    async def async_update(self):
        """Update the device."""
        try:
            device = await self.client.get_device(self.device_name)
            self.consumption = device.consumption
            self.powered = device.powered
            self.enabled = device.enabled
            self.max_consumption = device.max_consumption
            self.expected_consumption = device.expected_consumption
            self.cooldown = device.cooldown
            self._initialized = True
        except APIError:
            self.consumption = None
            self.powered = None
            self.enabled = None
            self.max_consumption = None
            self.expected_consumption = None
            self.cooldown = None

    async def async_set_max_consumption(self, value: float):
        """Update the max consumption."""
        await self.client.set_device_max_consumption(self.device_name, value)

    async def async_set_expected_consumption(self, value: float):
        """Update the expected consumption."""
        await self.client.set_device_expected_consumption(self.device_name, value)

    async def async_set_cooldown(self, value: int):
        """Update the cooldown."""
        await self.client.set_device_cooldown(self.device_name, value)
