# VorratsManager — Feature Design: Dashboard, Einkauf-Modus, Rezept-Kochen-Flow

**Datum:** 2026-04-17  
**Scope:** 3 neue Features in `custom_components/vorratsmanager/www/index.html`  
**Ansatz:** Option A — Erweiterung der bestehenden Single-File-App, kein Umbau

---

## 1. Dashboard-Tab (🏠 Home)

### Position
Neuer 5. Tab, eingefügt als **erster Tab** in der Tab-Leiste (vor Gefriertruhe).  
Tab-Icon: 🏠, Label: „Home" / „Home" / „Главная" / „Kreu" (i18n)

### Layout (von oben nach unten)

**Block 1 — Läuft bald ab**
- Alle Items aller 3 Lagerorte mit `daysUntilExpiry <= notifyDays` oder `<= 7`
- Sortiert: kritischste zuerst
- Gleiche `item-card`-Komponente wie in den Lagerort-Tabs
- Klick → öffnet Edit-Modal
- Nur sichtbar wenn mindestens 1 ablaufendes Item vorhanden; sonst Block ausgeblendet

**Block 2 — Heute kochen?**
- Zeigt bis zu 3 gespeicherte Favoriten-Rezepte (`db.savedRecipes`)
- Priorisierung: Rezept mit den meisten Zutaten-Matches auf ablaufende Items zuerst
- Jede Karte zeigt: Rezept-Name, Gerät-Badge, Zeit-Badge, neuer „🍳 Kochen"-Button
- Wenn keine Favoriten gespeichert: Hinweistext „Speichere KI-Rezepte als ⭐ Favoriten"

**Block 3 — Einkaufen-Button**
- Großer, prominenter Button `🛒 Einkaufen` am Ende des Dashboards
- Öffnet den Einkauf-Modus (Vollbild-Overlay)

### Datenabhängigkeiten
- Liest `db.items`, `db.savedRecipes`, `db.settings.notifyDays`
- Kein eigener State — rendert bei `renderAll()` mit

---

## 2. Einkauf-Modus

### Trigger
- Dashboard-Button `🛒 Einkaufen`
- Bestehender FAB `＋` öffnet weiterhin das normale Add-Modal (unverändert)

### UI — Vollbild-Overlay
```
┌─────────────────────────────────────┐
│ 🛒 Einkaufen      [3 eingelagert] ✓ Fertig │
├─────────────────────────────────────┤
│ [Name + 📷 Barcode]                 │
│ [Menge] [Einheit▼]  [MHD optional]  │
│ [❄️ Gefriert.] [🥬 Kühlschr.] [🏺 Vorrat] │
│         [ ＋ Einlagern ]            │
├─────────────────────────────────────┤
│ Zuletzt eingelagert:                │
│ • Hähnchenbrust  ❄️  ×1            │
│ • Milch          🥬  ×2            │
│ • Nudeln         🏺  ×1            │
└─────────────────────────────────────┘
```

### Verhalten
- Öffnen: Felder leeren, Lagerort = `freezer` als Default, Zähler = 0
- **„＋ Einlagern"**: 
  - Pflichtfeld: Name (nicht leer)
  - Item wird zu `db.items` hinzugefügt (Kategorie = `other` des gewählten Lagerorts)
  - Formular wird geleert, Lagerort bleibt, Zähler +1
  - Liste der letzten 5 eingelagerten Items aktualisiert sich
  - Kein Server-Save bei jedem Klick — Items werden lokal gepuffert
- **„✓ Fertig"**: Schließt Overlay, triggert einmalig `saveDb()` → Server-Sync

### State
```javascript
let _shopMode = {
  active: false,
  addedItems: [],  // Array der in dieser Session hinzugefügten Item-IDs
};
```

### i18n
| Key | DE | EN | RU | SQ |
|-----|----|----|-----|-----|
| `shopTitle` | Einkaufen | Shopping | Покупки | Blerje |
| `shopAdded` | `(n) => \`${n} eingelagert\`` | `(n) => \`${n} added\`` | `(n) => \`${n} добавлено\`` | `(n) => \`${n} shtuar\`` |
| `shopDone` | Fertig | Done | Готово | Gati |
| `shopAddBtn` | ＋ Einlagern | ＋ Add | ＋ Добавить | ＋ Shto |
| `shopRecent` | Zuletzt eingelagert | Recently added | Недавно добавлено | Shtuar së fundmi |

---

## 3. Rezept-Kochen-Flow

### Trigger
- Neuer Button **„🍳 Kochen"** in:
  - Gespeicherte Favoriten-Karten (im Rezepte-Tab)
  - KI-Rezept-Karten (im Rezepte-Tab)
  - Dashboard Block 2 (Heute kochen?)

### Modal — „Zutaten entnehmen"

**Struktur:**
```
┌─────────────────────────────────────┐
│ 🍳 Zutaten entnehmen         ✕     │
│ Rezept: [Name]                      │
├─────────────────────────────────────┤
│ ✅ Im Vorrat vorhanden:             │
│ ☑ Hähnchenbrust  1.2kg  ❄️         │
│ ☑ Zwiebel        3 Stück 🏺        │
│                                     │
│ ❌ Nicht im Vorrat:                 │
│ • Sahne 200ml        [+Einkauf]     │
│ • Knoblauch          [+Einkauf]     │
├─────────────────────────────────────┤
│ [Abbrechen]    [✓ Entnehmen (2)]    │
└─────────────────────────────────────┘
```

### Matching-Logik
```javascript
function matchIngredientToItems(ingredientStr, items) {
  const ing = ingredientStr.toLowerCase();
  return items.filter(item => {
    const name = item.name.toLowerCase();
    return ing.includes(name) || name.includes(ing.split(' ')[0]);
  });
}
```
- Case-insensitive Substring-Match in beide Richtungen
- Vorrats-Name gegen ersten Wortbaustein der Rezept-Zutat (ignoriert Mengenangaben)
- Kein KI-Match nötig

### Entnehmen-Aktion
- Alle angehakten Items: `qty = 0` → Item wird aus `db.items` entfernt
- „+ Einkaufsliste"-Button: ruft `callServiceViaPanel('todo', 'add_item', ...)` auf (nur im HA-Panel)
- Nach Bestätigung: `saveDb()`, Modal schließen, `renderAll()`, Toast

### i18n
| Key | DE | EN | RU | SQ |
|-----|----|----|-----|-----|
| `cookTitle` | Zutaten entnehmen | Remove ingredients | Убрать ингредиенты | Hiq përbërësit |
| `cookInStock` | Im Vorrat vorhanden | In stock | В наличии | Në stok |
| `cookMissing` | Nicht im Vorrat | Not in stock | Не в наличии | Nuk është në stok |
| `cookConfirm` | `(n) => \`Entnehmen (${n})\`` | `(n) => \`Remove (${n})\`` | `(n) => \`Убрать (${n})\`` | `(n) => \`Hiq (${n})\`` |
| `cookDone` | `(n) => \`${n} Zutaten entnommen ✓\`` | `(n) => \`${n} ingredients removed ✓\`` | `(n) => \`${n} ингредиентов убрано ✓\`` | `(n) => \`${n} përbërës hequr ✓\`` |
| `cookAddShop` | + Einkaufsliste | + Shopping list | + Список покупок | + Lista blerjes |

---

## Technische Umsetzung

### Änderungen an bestehenden Strukturen

**HTML:**
- Neuer `#tab-home` Tab-Content vor `#tab-freezer`
- Neuer `data-tab="home"` Button in `.tab-bar` (Position: ganz links)
- Neues `#shop-overlay` Vollbild-Overlay
- Neues `#cook-overlay` Modal

**JavaScript:**
- `switchTab()` erweitern: case `'home'` → `renderDashboard()`
- `renderAll()` erweitern: ruft `renderDashboard()` mit auf
- 4 neue Rendering-Funktionen: `renderDashboard()`, `openShopMode()`, `shopAddItem()`, `openCookModal(recipe)`
- `saveDb()` im Einkauf-Modus: nur beim „Fertig"-Button, nicht bei jedem Item

**CSS:**
- Minimale Ergänzungen: `.shop-overlay`, `.shop-form`, `.shop-recent-list`, `.cook-section`
- Dark Mode Regeln für neue Elemente

### Keine Änderungen an
- `panel.js` — unverändert
- `__init__.py` — unverändert
- Datenstruktur `data.json` — unverändert
- Bestehende Tabs/Modals — unverändert

---

## Nicht im Scope

- Mindestbestand-Feature (separates Feature, spätere Version)
- Wochenplanung
- Einkauf-Modus als eigener Tab (Option B, abgelehnt)
- KI-basiertes Ingredient-Matching
