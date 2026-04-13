"""VorratsManager – Home Assistant Integration."""
from __future__ import annotations

import json
import logging
import pathlib
import shutil

from homeassistant.components import frontend
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)
DOMAIN = "vorratsmanager"
PANEL_URL = "vorratsmanager"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Richtet VorratsManager ein."""

    src_dir = pathlib.Path(__file__).parent / "www"
    dst_dir = pathlib.Path(hass.config.path("www", "vorratsmanager"))
    data_file = dst_dir / "data.json"

    # --- Statische Dateien kopieren ---
    def _copy_www() -> None:
        dst_dir.mkdir(parents=True, exist_ok=True)
        for src_file in src_dir.iterdir():
            if src_file.is_file() and src_file.name != "data.json":
                shutil.copy2(src_file, dst_dir / src_file.name)
        if not data_file.exists():
            data_file.write_text(
                json.dumps({"items": [], "settings": {}, "updated": "", "version": 1},
                           ensure_ascii=False),
                encoding="utf-8",
            )
        _LOGGER.info("VorratsManager: Dateien unter %s bereitgestellt", dst_dir)

    await hass.async_add_executor_job(_copy_www)

    # --- Datenmigration von alter gefrierapp-Installation ---
    def _migrate() -> None:
        if data_file.stat().st_size > 100:
            return
        old = pathlib.Path(hass.config.path("www", "gefrierapp", "data.json"))
        if old.exists() and old.stat().st_size > 100:
            shutil.copy2(old, data_file)
            _LOGGER.info("VorratsManager: %d Bytes aus gefrierapp migriert", old.stat().st_size)

    await hass.async_add_executor_job(_migrate)

    # --- Panel in der Sidebar registrieren ---
    frontend.async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title="VorratsManager",
        sidebar_icon="mdi:fridge-outline",
        frontend_url_path=PANEL_URL,
        config={
            "_panel_custom": {
                "name": "vorrats-manager-panel",
                "module_url": "/local/vorratsmanager/panel.js",
                "trust_external": False,
                "embed_iframe": False,
            }
        },
        require_admin=False,
    )
    _LOGGER.info("VorratsManager: Panel registriert unter /%s", PANEL_URL)

    # --- Service vorratsmanager.vorrat_save ---
    async def _vorrat_save(call: ServiceCall) -> None:
        items = call.data.get("items", [])
        saved_recipes = call.data.get("savedRecipes", [])
        settings = call.data.get("settings", {})
        updated = call.data.get("updated", "")
        payload = json.dumps(
            {"items": items, "savedRecipes": saved_recipes, "settings": settings, "updated": updated, "version": 1},
            ensure_ascii=False,
        )
        try:
            await hass.async_add_executor_job(data_file.write_text, payload, "utf-8")
            hass.bus.async_fire(f"{DOMAIN}_updated", {"updated": updated})
            _LOGGER.debug("vorrat_save: %d Items", len(items))
        except OSError as err:
            _LOGGER.error("vorrat_save Fehler: %s", err)

    hass.services.async_register(DOMAIN, "vorrat_save", _vorrat_save)
    _LOGGER.info("VorratsManager v%s geladen", _get_version())
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entlädt die Integration (für Reload ohne Neustart)."""
    hass.services.async_remove(DOMAIN, "vorrat_save")
    # Panel entfernen
    try:
        hass.data["frontend_panels"].pop(PANEL_URL, None)
    except Exception:
        pass
    _LOGGER.info("VorratsManager entladen")
    return True


def _get_version() -> str:
    try:
        return json.loads(
            (pathlib.Path(__file__).parent / "manifest.json").read_text()
        ).get("version", "?")
    except Exception:
        return "?"
