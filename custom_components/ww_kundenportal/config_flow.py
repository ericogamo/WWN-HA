import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN
from .connector import WWPortalConnector


class WWPortalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Westfalen Weser."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            # Validate credentials
            connector = WWPortalConnector(username, password)
            success = await self.hass.async_add_executor_job(connector.login)

            if success:
                return self.async_create_entry(
                    title=f"Westfalen Weser ({username})", data=user_input
                )
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )
