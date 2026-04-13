"""Config Flow für VorratsManager – richtet sich mit einem Klick ein."""
from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

DOMAIN = "vorratsmanager"


class VorratsManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Einmaliger Setup-Dialog – keine Eingaben nötig."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Wird aufgerufen wenn der Nutzer die Integration hinzufügt."""
        # Nur eine Instanz erlauben
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        # Sofort fertig – kein Formular nötig
        return self.async_create_entry(title="VorratsManager", data={})
