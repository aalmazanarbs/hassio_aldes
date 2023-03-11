from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .aldes.api import AldesApi
from .const import DOMAIN, PRODUCT_COORDINATORS
from .entity import AldesProductDataUpdateCoordinator

PLATFORMS = [Platform.SELECT]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    aldesApi = AldesApi(async_get_clientsession(hass), entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])
    try:
        await aldesApi.authenticate()
        products = await aldesApi.get_products()
    except Exception as e:
        raise ConfigEntryNotReady from e

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        PRODUCT_COORDINATORS: []
    }

    for product in products:
        coordinator = AldesProductDataUpdateCoordinator(hass, product)
        await coordinator.async_config_entry_first_refresh()
        hass.data[DOMAIN][entry.entry_id][PRODUCT_COORDINATORS].append(coordinator)
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
