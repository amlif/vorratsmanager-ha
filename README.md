# VorratsManager für Home Assistant

Verwalte **Gefriertruhe, Kühlschrank und Vorratsraum** direkt in Home Assistant – mit KI-Rezeptvorschlägen, Favoriten, Bring!-Integration und Echtzeit-Sync zwischen allen Geräten im Haushalt.

[![HACS](https://img.shields.io/badge/HACS-Custom-orange)](https://hacs.xyz)
![HA](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue?logo=homeassistant)
![Lizenz](https://img.shields.io/badge/Lizenz-MIT-green)

---

## Features

| | |
|---|---|
| ❄️ Gefriertruhe · 🥬 Kühlschrank · 🏺 Vorratsraum | 3 Lagerorte mit eigenen Kategorien |
| ⚠️ MHD-Tracking | Ablaufwarnungen (konfigurierbar) + Telegram-Benachrichtigungen |
| 🤖 KI-Rezepte | Thermomix · Airfryer · Grill · Backofen · Herd |
| 🍳 Gerätewahl | Nur Rezepte für deine vorhandenen Geräte |
| 🥗 Diät-Filter | Vegetarisch · Vegan · Glutenfrei |
| 👥 Portionsauswahl | Rezeptmenge für 1–10 Personen |
| ⭐ Favoriten | KI-Rezepte speichern – sync auf allen Geräten |
| 🖨️ Rezept drucken | Druckfreundliche Ansicht |
| 🛒 Bring!-Integration | Erledigte Einkäufe direkt in den Vorrat importieren |
| 📷 Barcode-Scanner | Produkt scannen → automatisch befüllen (Open Food Facts) |
| ⚠️ Mindestbestand | Pro Artikel konfigurierbar – bei Unterschreitung automatisch zu Bring! |
| 🚫 Non-Food Filter | Nicht-Lebensmittel aus der Rezepte-Zutatenliste ausblenden |
| 📊 Statistiken | Übersicht über Lagermengen und Ablaufdaten |
| 🔄 Echtzeit-Sync | Alle Geräte im Haushalt synchron (WebSocket) |
| 🌐 4 Sprachen | Deutsch · English · Русский · Shqip |
| 🌙 Dark Mode | |
| 🔍 Cookidoo-Suche | Smarte Zutatenauswahl (MHD-priorisiert) |
| 📤 Export / Import | Datensicherung als JSON |

---

## Installation via HACS (empfohlen)

1. **HACS** → **Integrationen** → **⋮** → **Benutzerdefinierte Repositories**
2. URL: `https://github.com/amlif/vorratsmanager-ha` · Kategorie: **Integration**
3. **VorratsManager** suchen → **Installieren**
4. **Home Assistant neu starten**
5. ✅ **VorratsManager** erscheint automatisch in der Seitenleiste

> Keine Änderung an `configuration.yaml` nötig.

---

## Manuelle Installation

1. Ordner `custom_components/vorratsmanager/` in dein HA-Konfigurationsverzeichnis kopieren
2. Home Assistant neu starten

---

## Einrichtung

Nach der Installation und dem Neustart erscheint VorratsManager automatisch in der Seitenleiste. Es ist **keine weitere Konfiguration nötig** – die App läuft vollständig innerhalb von Home Assistant und benötigt keinen API-Token oder externe URL.

### Optionale Einstellungen (⚙️ in der App)

| Einstellung | Beschreibung |
|---|---|
| **Einkaufsliste (Entity ID)** | HA Todo-Entity für Bring! Sync (Standard: `todo.einkauf`) |
| **MHD-Warnung** | Wie viele Tage vor Ablauf gewarnt werden soll |
| **Küchengeräte** | KI schlägt nur Rezepte für gewählte Geräte vor |
| **Diät-Filter** | KI berücksichtigt Ernährungspräferenzen |
| **KI-Keys (optional)** | Groq- oder OpenRouter-Key für eigene KI-Modelle |
| **Sprache** | DE · EN · RU · SQ |
| **Dark Mode** | Dunkles Design |

---

## KI-Rezepte

Die App nutzt eine automatische Fallback-Kette – **kein API-Key nötig** wenn du die App als HA-Panel verwendest:

| Backend | Kosten | Einrichtung |
|---------|--------|-------------|
| **HA ai_task** (Standard) | Kostenlos | Automatisch – nichts nötig |
| **Groq** | Kostenlos | Key unter [console.groq.com](https://console.groq.com) → ⚙️ Einstellungen |
| **OpenRouter** | Kostenlos (freie Modelle) | Key unter [openrouter.ai](https://openrouter.ai) → ⚙️ Einstellungen |

**Wie es funktioniert:**
- Zutaten auswählen (oder automatisch die 5 bald ablaufenden Produkte)
- Portionsanzahl wählen (1–10 Personen)
- „KI-Rezepte generieren" tippen
- Die KI erstellt passende Rezepte für deine gewählten Küchengeräte
- Rezepte können als Favoriten gespeichert, gedruckt oder auf Cookidoo gesucht werden

---

## Bring!-Integration

Die Integration nutzt die **HA Todo-Integration** – keine externe API nötig.

**Voraussetzung:** Eine HA-Einkaufsliste muss als Todo-Entity eingerichtet sein (z.B. `todo.einkauf`).

**Vorgehen:**
1. Einkaufen gehen, Artikel in der Einkaufsliste als erledigt markieren
2. Im VorratsManager → **Vorratsraum** → **🛒 Bring! Sync** tippen
3. Lagerort für jeden Artikel wählen (Gefriertruhe / Kühlschrank / Vorratsraum)
4. **Hinzufügen** → Artikel landen direkt im Vorrat

Falls deine Einkaufsliste eine andere Entity ID hat (z.B. `todo.shopping`):
⚙️ Einstellungen → **Einkaufsliste (Entity ID)** anpassen.

---

## Datenspeicherung

- Vorratsdaten: `config/www/vorratsmanager/data.json`
- Echtzeit-Sync via HA WebSocket (Event `vorratsmanager_updated`)
- Kein Datenbankzugriff, kein Cloud-Dienst, kein Token nötig
- Export/Import als JSON jederzeit möglich (⚙️ → Daten)

---

## Technisches

- **Service:** `vorratsmanager.vorrat_save`
- **Event:** `vorratsmanager_updated`
- **Kommunikation:** panel.js ↔ iframe über `postMessage` (kein direkter API-Zugriff aus dem iframe)
- **Anforderungen:** Home Assistant 2024.1+

---

## Changelog

### v1.6.0
- **Neu:** Mindestbestand pro Artikel – wird Bestand auf/unter den Mindestbestand gesenkt, wird der Artikel automatisch zu Bring! hinzugefügt (⚠️ Mindestbestand → 🛒 Bring! ✓)
- **Neu:** „Kein Lebensmittel"-Checkbox pro Artikel – Non-Food Artikel (Zahnpasta, Waschmittel etc.) werden aus der Rezepte-Zutatenliste ausgeblendet
- **Neu:** Toggle-Button im Rezepte-Tab: `🚫 +N anzeigen` zeigt ausgeblendete Non-Food Artikel bei Bedarf an
- **Neu:** KI-Rezept-Generierung schließt Non-Food Artikel automatisch aus

### v1.5.0
- **Neu:** Dashboard-Tab (🏠 Home) – zeigt ablaufende Items und alle gespeicherten Favoriten aufklappbar
- **Neu:** Einkauf-Schnellmodus – Vollbild-Overlay zum schnellen Einlagern mehrerer Items ohne Modal-Schließen
- **Neu:** Rezept-Kochen-Flow – 🍳-Button öffnet Zutaten-Entnehmen-Modal mit Stepper (Teilentnahme)
- **Neu:** Barcode-Scanner funktioniert jetzt in der HA Mobile App (html5-qrcode Fallback für iOS/WebView)
- **Fix:** Barcode-Scanner schreibt korrekt ins Feld (Shop-Modus oder Add-Modal)

### v1.4.6
- **Entfernt:** HA URL + Long-Lived Token aus den Einstellungen – nicht mehr nötig, da alle Service-Calls über panel.js laufen
- **Neu:** Einkaufsliste (Entity ID) in Einstellungen konfigurierbar (Standard: `todo.einkauf`)
- **Neu:** panel.js leitet alle HA Service-Calls durch (`vorrat-service` Message-Typ)
- **Bugfix:** `renderExpiringForRecipes` – kaputtes Karten-Layout im Rezepte-Tab behoben
- **Bugfix:** Bring!-Import Modal: Abbrechen-Button jetzt mehrsprachig
- **Bugfix:** Statistik-Modal: „Abgelaufen"-Text jetzt in allen 4 Sprachen korrekt
- **Bugfix:** „Alle Daten löschen" löscht jetzt auch gespeicherte Rezepte
- **Bugfix:** Server-Sync von `0`/`false`/leerem Array korrekt übernommen
- **Bugfix:** Entnommen-Modal: Min-Menge bei + / − Buttons konsistent (0.1)
- **Bugfix:** Header-Icon wechselt jetzt beim Tab-Wechsel (❄️ / 🥬 / 🏺 / 👨‍🍳)

### v1.4.5
- Barcode-Scanner: Kamera-Bridge über panel.js für HA Companion App (iOS/Android)

### v1.4.4
- Barcode-Scanner: `allow="camera"` im iframe, ZXing-Fallback für iOS

### v1.4.3
- Bugfix: Barcode-Scanner in HA Companion App

### v1.4.2
- Barcode-Scanner Verbesserungen

### v1.4.1
- Bugfix: Weißer Bildschirm nach v1.4.0 Update

### v1.4.0
- Bring!-Integration, Diät-Filter, Lagerort-Auswahl beim Import

---

## Lizenz

MIT – freie Nutzung, Weitergabe und Anpassung erlaubt.
