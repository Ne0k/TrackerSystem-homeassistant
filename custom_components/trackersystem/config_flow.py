"""Config- en options-flow voor TrackerSystem."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_API_KEY,
    CONF_BASE_URL,
    CONF_DEVICES,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .coordinator import InvalidAuth, TrackerSystemCoordinator


class TrackerSystemConfigFlow(ConfigFlow, domain=DOMAIN):
    """Verbind met het portaal en kies de objecten."""

    VERSION = 1

    def __init__(self) -> None:
        self._base_url: str = ""
        self._api_key: str = ""
        self._devices: dict[str, str] = {}  # imei -> naam

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> Any:
        errors: dict[str, str] = {}
        if user_input is not None:
            self._base_url = user_input[CONF_BASE_URL].rstrip("/")
            self._api_key = user_input[CONF_API_KEY]
            session = async_get_clientsession(self.hass)
            try:
                data = await TrackerSystemCoordinator.fetch(
                    session, self._base_url, self._api_key
                )
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # noqa: BLE001
                errors["base"] = "cannot_connect"
            else:
                self._devices = {
                    imei: (d.get("name") or imei) for imei, d in data.items()
                }
                await self.async_set_unique_id(self._base_url)
                self._abort_if_unique_id_configured()
                return await self.async_step_select()

        schema = vol.Schema(
            {
                vol.Required(CONF_BASE_URL, default="https://portal.trackersystem.nl"): str,
                vol.Required(CONF_API_KEY): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_select(
        self, user_input: dict[str, Any] | None = None
    ) -> Any:
        if user_input is not None:
            return self.async_create_entry(
                title="TrackerSystem",
                data={
                    CONF_BASE_URL: self._base_url,
                    CONF_API_KEY: self._api_key,
                    CONF_DEVICES: user_input[CONF_DEVICES],
                },
            )

        options = [
            {"value": imei, "label": name} for imei, name in sorted(
                self._devices.items(), key=lambda kv: kv[1].lower()
            )
        ]
        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICES, default=list(self._devices)): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        multiple=True,
                        mode=SelectSelectorMode.LIST,
                    )
                )
            }
        )
        return self.async_show_form(step_id="select", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(entry: ConfigEntry) -> OptionsFlow:
        return TrackerSystemOptionsFlow(entry)


class TrackerSystemOptionsFlow(OptionsFlow):
    """Pas het polling-interval aan."""

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> Any:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self._entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        schema = vol.Schema(
            {
                vol.Required(CONF_SCAN_INTERVAL, default=current): vol.All(
                    vol.Coerce(int), vol.Range(min=30, max=3600)
                )
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
