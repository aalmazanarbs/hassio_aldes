from typing import Any, Dict, Optional

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_BASE
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.config_validation import string

from aiohttp import ClientConnectionError, ClientConnectorError

import voluptuous as vol

from .aldes.api import AldesApi, AuthenticationException
from .const import INTEGRATION, DOMAIN

class AldesConfigFlow(ConfigFlow, domain = DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        errors: Dict[str, str] = {}

        if user_input is not None:
            error = await self._process_step_user_input(user_input)
            if error is None:
                return await self._finish_step_user(user_input)
            else:
                errors[CONF_BASE] = error
        
        return self.async_show_form(
            step_id = "user",
            data_schema = vol.Schema({
                vol.Required(CONF_USERNAME) : string,
                vol.Required(CONF_PASSWORD) : string
            }),
            errors = errors
        )
    
    async def _process_step_user_input(self, user_input: Dict[str, Any]) -> str:
        error = None

        try:
            aldesApi = AldesApi(async_get_clientsession(self.hass), user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            await aldesApi.authenticate()
        except (ClientConnectorError, ClientConnectionError):
            error = "cannot_connect"
        except AuthenticationException:
            error = "invalid_auth"
        except Exception:
            error = "unknown"
        
        return error
    
    async def _finish_step_user(self, user_input: Dict[str, Any]) -> FlowResult:
        await self.async_set_unique_id(user_input[CONF_USERNAME])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title = f'{INTEGRATION} - {user_input[CONF_USERNAME]}',
            data  = user_input,
        )
