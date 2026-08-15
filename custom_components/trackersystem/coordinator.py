"""DataUpdateCoordinator: periodically fetches all objects from the portal."""
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_LIST_PATH, DOMAIN

_LOGGER = logging.getLogger(__name__)


class TrackerSystemCoordinator(DataUpdateCoordinator):
    """Poll the portal and keep per-IMEI object data."""

    def __init__(
        self,
        hass: HomeAssistant,
        base_url: str,
        api_key: str,
        scan_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, dict]:
        """Return {imei: device_payload}."""
        return await self.fetch(self._session, self._base_url, self._api_key)

    @staticmethod
    async def fetch(
        session: aiohttp.ClientSession, base_url: str, api_key: str
    ) -> dict[str, dict]:
        """Fetch the full object list; also used by the config flow."""
        url = base_url.rstrip("/") + API_LIST_PATH
        headers = {"X-Api-Key": api_key, "Accept": "application/json"}
        try:
            async with async_timeout.timeout(20):
                resp = await session.get(url, headers=headers)
                if resp.status == 401:
                    raise InvalidAuth
                if resp.status != 200:
                    raise UpdateFailed(f"HTTP {resp.status}")
                data = await resp.json()
        except InvalidAuth:
            raise
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Verbinding mislukt: {err}") from err

        devices = data.get("devices") if isinstance(data, dict) else None
        if not isinstance(devices, list):
            raise UpdateFailed("Onverwacht antwoord van het portaal")
        return {str(d.get("imei")): d for d in devices if d.get("imei")}


class InvalidAuth(Exception):
    """Invalid API key."""
