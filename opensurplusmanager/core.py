"""Core module for OpenSurplusManager integration."""

from pyosmanager import APIError, OSMClient


class OSMCore:
    """Base representation of a OpenSurplusManager Core."""

    def __init__(self, client: OSMClient):
        """Initialize the surplus."""
        self.client = client
        self.surplus: float | None = None
        self.grid_margin: float | None = None
        self.surplus_margin: float | None = None
        self.idle_power: float | None = None

    async def async_update(self):
        """Update the surplus."""
        if self.surplus is None:
            try:
                state = await self.client.get_core_state()
                self.surplus = state.surplus
                self.grid_margin = state.grid_margin
                self.surplus_margin = state.surplus_margin
                self.idle_power = state.idle_power
            except APIError:
                self.surplus = None
                self.grid_margin = None
                self.surplus_margin = None
                self.idle_power = None

    async def async_set_grid_margin(self, value: float):
        """Update the grid margin."""
        await self.client.set_grid_margin(value)

    async def async_set_surplus_margin(self, value: float):
        """Update the surplus margin."""
        await self.client.set_surplus_margin(value)

    async def async_set_idle_power(self, value: float):
        """Update the idle power."""
        await self.client.set_idle_power(value)
