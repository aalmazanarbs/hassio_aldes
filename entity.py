import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .aldes.product import AldesProduct
from .const import DOMAIN, INTEGRATION, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class AldesProductDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, product: AldesProduct) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name = f'{DOMAIN}-{product.id}',
            update_interval = SCAN_INTERVAL,
            request_refresh_debouncer = Debouncer(
                hass, _LOGGER, cooldown = 5, immediate = False
            )
        )
        
        self.product = product

    async def _async_update_data(self) -> None:
        await self.product.update()

class AldesProductEntity(CoordinatorEntity[AldesProductDataUpdateCoordinator]):

    def __init__(self, coordinator: AldesProductDataUpdateCoordinator, entity_suffix: str) -> None:
        super().__init__(coordinator)
        
        product = coordinator.product
        self._attr_name = f'{product.get_display_name()} {entity_suffix}'
        self._attr_unique_id = f'{product.id}-{entity_suffix.lower().replace(" ", "-")}'
        self._attr_device_info = DeviceInfo(
            identifiers  = {(DOMAIN, product.id)},
            manufacturer = INTEGRATION,
            model        = product.get_display_name(),
            name         = product.name
        )
