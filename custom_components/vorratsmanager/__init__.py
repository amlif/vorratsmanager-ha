"""VorratsManager – Home Assistant Integration.

Richtet sich automatisch ein:
- Panel erscheint sofort in der HA-Sidebar (mdi:fridge-outline)
- Dateien werden unter /local/vorratsmanager/ bereitgestellt
- Service vorratsmanager.vorrat_save zum Speichern
- Event vorratsmanager_updated für Echtzeit-Sync zwischen Geräten
"""
from __future__ import annotations

import json
import logging
import pathlib
import shutil

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)
DOMAIN = "vorratsmanager"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Wird beim Start von HA aufgerufen – keine Aktion nötig."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Richtet VorratsManager ein (wird nach dem Config-Flow aufgerufen)."""

    src_dir = pathlib.Path(__file__).parent / "www"
    dst_dir = pathlib.Path(hass.config.path("www", "vorratsmanager"))
    data_file = dst_dir / "data.json"

    # --- Statische Dateien kopieren ---
    def _copy_www() -> None:
        dst_dir.mkdir(parents=True, exist_ok=True)
        for src_file in src_dir.iterdir():
            if src_file.is_file() and src_file.name != "data.json":
                shutil.copy2(src_file, dst_dir / src_file.name)
        # data.json nur anlegen wenn noch nicht vorhanden (bestehende Daten bleiben!)
        if not data_file.exists():
            data_file.write_text(
                json.dumps(
                    {"items": [], "settings": {}, "updated": "", "version": 1},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        _LOGGER.info("VorratsManager: Dateien bereitgestellt unter %s", dst_dir)

    await hass.async_add_executor_job(_copy_www)

    # --- Panel in der Sidebar registrieren ---
    try:
        from homeassistant.components.panel_custom import async_register_panel

        await async_register_panel(
            hass,
            webcomponent_name="vorrats-manager-panel",
            frontend_url_path="vorratsmanager",
            sidebar_title="VorratsManager",
            sidebar_icon="mdi:fridge-outline",
            module_url="/local/vorratsmanager/panel.js",
            require_admin=False,
            config=None,
            embed_iframe=False,
            trust_external_url=False,
        )
        _LOGGER.info("VorratsManager: Panel registriert")
    except Exception as err:
        _LOGGER.error("VorratsManager: Panel-Registrierung fehlgeschlagen: %s", err)

    # --- Service vorratsmanager.vorrat_save ---
    async def _vorrat_save(call: ServiceCall) -> None:
        items = call.data.get("items", [])
        settings = call.data.get("settings", {})
        updated = call.data.get("updated", "")

        payload = json.dumps(
            {"items": items, "settings": settings, "updated": updated, "version": 1},
            ensure_ascii=False,
        )
        try:
            await hass.async_add_executor_job(data_file.write_text, payload, "utf-8")
            hass.bus.async_fire(f"{DOMAIN}_updated", {"updated": updated})
            _LOGGER.debug("vorrat_save: %d Items gespeichert", len(items))
        except OSError as err:
            _LOGGER.error("vorrat_save Schreibfehler: %s", err)

    hass.services.async_register(DOMAIN, "vorrat_save", _vorrat_save)

    version = _get_version()
    _LOGGER.info("VorratsManager v%s geladen", version)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Wird aufgerufen wenn die Integration entfernt wird."""
    hass.services.async_remove(DOMAIN, "vorrat_save")
    _LOGGER.info("VorratsManager entladen")
    return True


def _get_version() -> str:
    try:
        manifest = json.loads(
            (pathlib.Path(__file__).parent / "manifest.json").read_text()
        )
        return manifest.get("version", "?")
    except Exception:
        return "?"
