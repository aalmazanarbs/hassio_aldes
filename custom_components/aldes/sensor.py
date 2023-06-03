from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, PRODUCT_COORDINATORS
from .entity import AldesProductEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id][PRODUCT_COORDINATORS]
    async_add_entities(AldesProductEntitySensor(coordinator) for coordinator in coordinators)

class AldesProductEntitySensor(AldesProductEntity, SensorEntity):

    _attr_icon = "mdi:temperature-celsius"
    _attr_unit_of_measurement = None
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: AldesProductDataUpdateCoordinator) -> None:
        super().__init__(coordinator, 'Temperature')

        self._attr_options = coordinator.product.get_display_modes()
        self._attr_device_class = "temperature"
        self._attr_native_unit_of_measurement = TEMP_CELSIUS

    @property
    def native_value(self) -> str:
        return self.coordinator.product.get_sensor_value()

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.product.maybe_set_mode_from_display(option)
        await self.coordinator.async_request_refresh()
