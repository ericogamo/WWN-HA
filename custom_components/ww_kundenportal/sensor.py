import logging
from datetime import timedelta
import async_timeout

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.const import UnitOfEnergy

from .const import DOMAIN, SCAN_INTERVAL_MINUTES, SENSOR_TYPES, SENSOR_PURCHASE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    connector = hass.data[DOMAIN][config_entry.entry_id]

    async def async_update_data():
        """Fetch data from API endpoint."""
        async with async_timeout.timeout(30):
            data = await hass.async_add_executor_job(connector.fetch_data)
            if not data:
                raise UpdateFailed(f"Error communicating with API")
            return data

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="sensor",
        update_method=async_update_data,
        update_interval=timedelta(minutes=SCAN_INTERVAL_MINUTES),
    )

    # Fetch initial data so we have something when entities are added
    await coordinator.async_config_entry_first_refresh()

    entities = []

    # Check what data we have and add sensors accordingly
    if coordinator.data.get("reading_purchase_kwh") is not None:
        entities.append(WWSensor(coordinator, "purchase", config_entry))

    if coordinator.data.get("reading_feed_in_kwh") is not None:
        entities.append(WWSensor(coordinator, "feed_in", config_entry))

    async_add_entities(entities)


class WWSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, sensor_type, config_entry):
        self.coordinator = coordinator
        self._sensor_type = sensor_type
        self._config_entry = config_entry
        self._type_data = SENSOR_TYPES[sensor_type]

    @property
    def name(self):
        """Return the name of the sensor."""
        # Use the name from const.py
        return f"Westfalen Weser {self._type_data['name']}"

    @property
    def unique_id(self):
        """Return a unique ID."""
        # Uses meter ID if available, otherwise falls back to semantic ID
        meter_id = self.coordinator.data.get(f"meter_id_{self._sensor_type}")
        if meter_id:
            return f"ww_{meter_id}_{self._sensor_type}"
        return f"ww_{self._config_entry.entry_id}_{self._sensor_type}"

    @property
    def state(self):
        """Return the state of the sensor."""
        key = self._type_data["key"]
        return self.coordinator.data.get(key)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return UnitOfEnergy.KILO_WATT_HOUR

    @property
    def device_class(self):
        """Return the device class."""
        return SensorDeviceClass.ENERGY

    @property
    def state_class(self):
        """Return the state class."""
        return SensorStateClass.TOTAL_INCREASING

    @property
    def icon(self):
        """Return the icon."""
        return self._type_data["icon"]

    @property
    def should_poll(self):
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update the entity. Only used by the generic entity update service."""
        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        ts_key = f"timestamp_{self._sensor_type}"
        ts = self.coordinator.data.get(ts_key)
        if ts:
            attrs["last_reading_timestamp"] = ts

        mid_key = f"meter_id_{self._sensor_type}"
        mid = self.coordinator.data.get(mid_key)
        if mid:
            attrs["meter_id"] = mid

        return attrs
