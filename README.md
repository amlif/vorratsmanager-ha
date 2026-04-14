# VorratsManager für Home Assistant

Verwalte **Gefriertruhe, Kühlschrank und Vorratsraum** direkt in Home Assistant – mit KI-Rezeptvorschlägen, Favoriten, Bring!-Integration und Echtzeit-Sync zwischen allen Geräten.

[![HACS](https://img.shields.io/badge/HACS-Custom-orange)](https://hacs.xyz)
![HA](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue?logo=homeassistant)
![Lizenz](https://img.shields.io/badge/Lizenz-MIT-green)

---

## Features

| | |
|---|---|
| ❄️ Gefriertruhe · 🥬 Kühlschrank · 🏺 Vorratsraum | 3 Lagerorte mit eigenen Kategorien |
| ⚠️ MHD-Tracking | Ablaufwarnungen (konfigurierbar) |
| 🤖 KI-Rezepte | Thermomix · Airfryer · Grill · Backofen · Herd |
| 🍳 Gerätewahl | Nur Rezepte für deine vorhandenen Geräte |
| ⭐ Favoriten | KI-Rezepte speichern – sync auf allen Geräten |
| 🛒 Bring!-Integration | Erledigte Einkäufe direkt in den Vorrat |
| 🔄 Echtzeit-Sync | Alle Geräte im Haushalt synchron |
| 🌐 4 Sprachen | Deutsch · English · Русский · Shqip |
| 🌙 Dark Mode | |
| 🔍 Cookidoo-Suche | Smarte Zutatenauswahl (MHD-priorisiert) |
| 📤 Export / Import | JSON |

---

## Installation via HACS (empfohlen)

1. **HACS** → **Integrationen** → **⋮** (oben rechts) → **Benutzerdefinierte Repositories**
2. URL: `https://github.com/amlif/vorratsmanager-ha` · Kategorie: **Integration**
3. **VorratsManager** suchen → **Installieren**
4. **Home Assistant neu starten**
5. ✅ Fertig – **VorratsManager** erscheint automatisch in der Seitenleiste

> Keine Änderung an `configuration.yaml` nötig.

---

## Manuelle Installation

1. Den Ordner `custom_components/vorratsmanager/` in dein HA-Konfigurationsverzeichnis kopieren
2. Home Assistant neu starten

---

## KI-Rezepte

Die App nutzt eine Fallback-Kette – du brauchst **keinen** API-Key wenn du HA verwendest:

| Backend | Kosten | Einrichtung |
|---------|--------|-------------|
| **HA ai_task** | Kostenlos | Automatisch im HA-Panel – nichts nötig |
| **Groq** | Kostenlos | Key auf [console.groq.com](https://console.groq.com) → ⚙️ Einstellungen |
| **OpenRouter** | Kostenlos (freie Modelle) | Key auf [openrouter.ai](https://openrouter.ai) → ⚙️ Einstellungen |

In ⚙️ Einstellungen kannst du außerdem festlegen, welche Küchengeräte du besitzt – die KI schlägt dann nur passende Rezepte vor (Thermomix, Airfryer, Grill, Backofen, Herd). Bereits angezeigte Rezepte werden automatisch ausgeschlossen, damit die Vorschläge abwechslungsreich bleiben.

---

## Bring!-Integration

1. Bring! App → Profil → API-Token kopieren
2. ⚙️ Einstellungen → Bring! Token + Liste eintragen
3. Erledigte Artikel werden auf Knopfdruck in den Vorrat importiert

---

## Datenspeicherung

- Vorratsdaten: `config/www/vorratsmanager/data.json`
- Echtzeit-Sync via HA WebSocket (`vorratsmanager_updated` Event)
- Kein Datenbankzugriff, kein Cloud-Dienst

---

## Technisches

- **Service:** `vorratsmanager.vorrat_save`
- **Event:** `vorratsmanager_updated`
- **Panel-URL:** `/local/vorratsmanager/panel.js`
- **Anforderungen:** Home Assistant 2024.1+, HACS (für automatische Updates)

---

## Migration von der manuellen Installation

Falls du bisher `pyscript` + `panel_custom` manuell konfiguriert hattest:

1. HACS-Version installieren, HA neu starten
2. Aus `configuration.yaml` entfernen:
   ```yaml
   # Das kann weg:
   panel_custom:
     - name: vorrats-manager-panel
       ...
   ```
3. `pyscript/vorratsmanager.py` kann gelöscht werden
4. Deine Daten bleiben erhalten (data.json wird nicht überschrieben)

---

## Changelog

### v1.4.1
- Bugfix: Weißer Bildschirm / App komplett nicht benutzbar nach v1.4.0 Update (fehlende Anführungszeichen in `syncBring()` verursachten JavaScript-Syntaxfehler)

### v1.4.0
- Bring!-Integration: Erledigte Artikel direkt in Vorrat importieren
- Lagerort-Auswahl beim Bring!-Import
- Diät-Filter für KI-Rezepte

---

## Lizenz

MIT – freie Nutzung, Weitergabe und Anpassung erlaubt.
