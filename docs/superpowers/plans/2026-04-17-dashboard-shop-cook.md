# Dashboard, Einkauf-Modus & Rezept-Kochen-Flow — Implementierungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Drei neue Features in `index.html`: Dashboard-Tab (ablaufende Items + Rezeptvorschläge + Shop-Button), Einkauf-Schnellmodus (Vollbild-Overlay, mehrere Items ohne Modal-Close), Rezept-Kochen-Flow (Zutaten als Teilentnahme aus Vorrat).

**Architecture:** Alle Änderungen in einer einzigen Datei `custom_components/vorratsmanager/www/index.html`. Neuer Home-Tab als erster Tab, Shop als Vollbild-Overlay (nicht Tab), Koch-Modal als Standard-Overlay. Kein Umbau der bestehenden Struktur.

**Tech Stack:** Vanilla JS, CSS Custom Properties, HA WebSocket via panel.js postMessage

---

## Datei-Übersicht

| Datei | Änderung |
|-------|----------|
| `custom_components/vorratsmanager/www/index.html` | Alle Änderungen: CSS, HTML, JS |

Alle Tasks beziehen sich auf diese eine Datei. Lokaler Pfad: `/tmp/vorratsmanager-ha/custom_components/vorratsmanager/www/index.html`

Deploy-Befehl (nach jedem Task der getestet werden soll):
```bash
echo '#!/bin/bash
echo 3001' > /tmp/askpass.sh && chmod +x /tmp/askpass.sh
cat /tmp/vorratsmanager-ha/custom_components/vorratsmanager/www/index.html | \
  DISPLAY=:0 SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force \
  ssh -o StrictHostKeyChecking=no ha@192.168.1.11 -p 22 \
  'sudo tee /homeassistant/www/vorratsmanager/index.html > /dev/null && echo OK'
```
Danach im Browser: **Ctrl+Shift+R** (Hard Reload).

---

## Task 1: i18n-Schlüssel für alle drei Features

**Files:**
- Modify: `index.html` — JS-Block, T-Objekt (de/en/ru/sq), ca. Zeile 1575

- [ ] **Schritt 1: Neue Keys ans Ende von `T.de` einfügen**

Suche die Zeile `expiringTitle: 'Läuft bald ab',` in `T.de` und füge DANACH ein:
```javascript
    homeDashboard: 'Home',
    homeExpiring: 'Läuft bald ab',
    homeCookToday: 'Heute kochen?',
    homeNoFavorites: 'Speichere KI-Rezepte als ⭐ Favoriten um hier Vorschläge zu sehen.',
    homeShopBtn: 'Einkaufen',
    shopTitle: 'Einkaufen',
    shopAdded: (n) => `${n} eingelagert`,
    shopDone: 'Fertig',
    shopAddBtn: '＋ Einlagern',
    shopRecent: 'Zuletzt eingelagert:',
    shopEmpty: 'Noch nichts eingelagert.',
    cookBtn: 'Kochen',
    cookTitle: 'Zutaten entnehmen',
    cookInStock: 'Im Vorrat vorhanden',
    cookMissing: 'Nicht im Vorrat',
    cookConfirm: (n) => `Entnehmen (${n})`,
    cookDone: (n) => `${n} Zutaten entnommen ✓`,
    cookAddShop: '+ Einkaufsliste',
```

- [ ] **Schritt 2: Neue Keys ans Ende von `T.en` einfügen**

Suche `expiringTitle:` in `T.en` und füge DANACH ein:
```javascript
    homeDashboard: 'Home',
    homeExpiring: 'Expiring soon',
    homeCookToday: 'Cook today?',
    homeNoFavorites: 'Save AI recipes as ⭐ favourites to see suggestions here.',
    homeShopBtn: 'Shopping',
    shopTitle: 'Shopping',
    shopAdded: (n) => `${n} added`,
    shopDone: 'Done',
    shopAddBtn: '＋ Add',
    shopRecent: 'Recently added:',
    shopEmpty: 'Nothing added yet.',
    cookBtn: 'Cook',
    cookTitle: 'Remove ingredients',
    cookInStock: 'In stock',
    cookMissing: 'Not in stock',
    cookConfirm: (n) => `Remove (${n})`,
    cookDone: (n) => `${n} ingredients removed ✓`,
    cookAddShop: '+ Shopping list',
```

- [ ] **Schritt 3: Neue Keys ans Ende von `T.ru` einfügen**

Suche `expiringTitle:` in `T.ru` und füge DANACH ein:
```javascript
    homeDashboard: 'Главная',
    homeExpiring: 'Скоро истекает',
    homeCookToday: 'Что приготовить?',
    homeNoFavorites: 'Сохраняйте рецепты ИИ как ⭐ избранные, чтобы видеть предложения здесь.',
    homeShopBtn: 'Покупки',
    shopTitle: 'Покупки',
    shopAdded: (n) => `${n} добавлено`,
    shopDone: 'Готово',
    shopAddBtn: '＋ Добавить',
    shopRecent: 'Недавно добавлено:',
    shopEmpty: 'Пока ничего не добавлено.',
    cookBtn: 'Готовить',
    cookTitle: 'Взять ингредиенты',
    cookInStock: 'В наличии',
    cookMissing: 'Нет в наличии',
    cookConfirm: (n) => `Взять (${n})`,
    cookDone: (n) => `${n} ингредиентов взято ✓`,
    cookAddShop: '+ Список покупок',
```

- [ ] **Schritt 4: Neue Keys ans Ende von `T.sq` einfügen**

Suche `expiringTitle:` in `T.sq` und füge DANACH ein:
```javascript
    homeDashboard: 'Kreu',
    homeExpiring: 'Skadon së shpejti',
    homeCookToday: 'Çfarë të gatuajmë?',
    homeNoFavorites: 'Ruaj receta IA si ⭐ të preferuara për të parë sugjerime këtu.',
    homeShopBtn: 'Blerje',
    shopTitle: 'Blerje',
    shopAdded: (n) => `${n} shtuar`,
    shopDone: 'Gati',
    shopAddBtn: '＋ Shto',
    shopRecent: 'Shtuar së fundmi:',
    shopEmpty: 'Asgjë e shtuar ende.',
    cookBtn: 'Gatuaj',
    cookTitle: 'Hiq përbërësit',
    cookInStock: 'Në stok',
    cookMissing: 'Nuk është në stok',
    cookConfirm: (n) => `Hiq (${n})`,
    cookDone: (n) => `${n} përbërës hequr ✓`,
    cookAddShop: '+ Lista e blerjeve',
```

- [ ] **Schritt 5: Commit**
```bash
cd /tmp/vorratsmanager-ha && git add custom_components/vorratsmanager/www/index.html && git commit -m "feat: i18n keys für Dashboard, Einkauf-Modus, Kochen-Flow"
```

---

## Task 2: CSS für neue Komponenten

**Files:**
- Modify: `index.html` — CSS-Block, direkt vor `</style>` (ca. Zeile 1197)

- [ ] **Schritt 1: CSS vor `</style>` einfügen**

Suche die Zeile `</style>` und füge DAVOR ein:

```css
    /* ===== DASHBOARD TAB ===== */
    .dashboard-content {
      flex: 1;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    /* ===== SHOP OVERLAY ===== */
    #shop-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: var(--bg);
      z-index: 400;
      flex-direction: column;
      overflow: hidden;
    }
    #shop-overlay.open { display: flex; }
    .shop-header {
      height: var(--header-height);
      background: var(--card);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      flex-shrink: 0;
    }
    .shop-counter {
      font-size: 14px;
      font-weight: 700;
      color: var(--pantry);
    }
    .shop-form {
      padding: 16px;
      background: var(--card);
      border-bottom: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex-shrink: 0;
    }
    .shop-form-row {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    .shop-loc-btns {
      display: flex;
      gap: 6px;
    }
    .shop-loc-btn {
      flex: 1;
      padding: 10px 6px;
      border: 2px solid var(--border);
      border-radius: 10px;
      background: var(--bg);
      font-size: 20px;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s;
    }
    .shop-loc-btn.active[data-loc="freezer"] { border-color: var(--freezer); background: var(--freezer-bg); }
    .shop-loc-btn.active[data-loc="fridge"]  { border-color: var(--fridge);  background: var(--fridge-bg);  }
    .shop-loc-btn.active[data-loc="pantry"]  { border-color: var(--pantry);  background: var(--pantry-bg);  }
    .shop-add-btn {
      width: 100%;
      padding: 14px;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      transition: opacity 0.15s;
    }
    .shop-add-btn:active { opacity: 0.85; }
    .shop-recent {
      flex: 1;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
      padding: 12px 16px;
    }
    .shop-recent-title {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
    }
    .shop-recent-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 0;
      border-bottom: 1px solid var(--border);
      font-size: 14px;
    }
    .shop-recent-item:last-child { border-bottom: none; }

    /* ===== COOK MODAL ===== */
    .cook-section-title {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin: 12px 0 8px;
    }
    .cook-item-row {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 0;
      border-bottom: 1px solid var(--border);
    }
    .cook-item-row:last-child { border-bottom: none; }
    .cook-item-name { flex: 1; font-size: 14px; font-weight: 500; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .cook-item-meta { font-size: 11px; color: var(--text-muted); }
    .cook-stepper { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
    .cook-step-btn {
      width: 30px; height: 30px;
      border-radius: 8px;
      border: 1.5px solid var(--border);
      background: var(--bg);
      font-size: 18px;
      font-weight: 300;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text);
    }
    .cook-step-btn:active { background: var(--border); }
    .cook-qty-val { font-size: 15px; font-weight: 700; min-width: 36px; text-align: center; }
    .cook-missing-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid var(--border);
      font-size: 14px;
      color: var(--text-muted);
    }
    .cook-missing-item:last-child { border-bottom: none; }
    .cook-shop-btn {
      font-size: 12px;
      padding: 4px 8px;
      border-radius: 6px;
      border: 1.5px solid var(--border);
      background: var(--bg);
      color: var(--primary);
      cursor: pointer;
      white-space: nowrap;
      flex-shrink: 0;
    }

    body.dark .shop-loc-btn { background: var(--bg); border-color: var(--border); }
    body.dark .cook-step-btn { background: var(--bg); border-color: var(--border); }
```

- [ ] **Schritt 2: Commit**
```bash
cd /tmp/vorratsmanager-ha && git add custom_components/vorratsmanager/www/index.html && git commit -m "feat: CSS für Dashboard, Shop-Overlay, Koch-Modal"
```

---

## Task 3: HTML — Dashboard-Tab, Shop-Overlay, Koch-Modal

**Files:**
- Modify: `index.html` — HTML body

- [ ] **Schritt 1: Dashboard-Tab-Content einfügen**

Suche `<!-- FREEZER TAB -->` und füge DAVOR ein:

```html
<!-- DASHBOARD TAB -->
<div class="tab-content active" id="tab-home" data-tab="home">
  <div class="dashboard-content" id="dashboard-content"></div>
</div>
```

- [ ] **Schritt 2: `active` von Freezer-Tab entfernen**

Ändere:
```html
<div class="tab-content active" id="tab-freezer" data-tab="freezer">
```
zu:
```html
<div class="tab-content" id="tab-freezer" data-tab="freezer">
```

- [ ] **Schritt 3: Home-Button als ersten Tab einfügen**

Suche in der `.tab-bar`:
```html
  <button class="tab-btn active" data-tab="freezer" onclick="switchTab('freezer')">
```
und ändere es zu (Home DAVOR, active von freezer entfernen):
```html
  <button class="tab-btn active" data-tab="home" onclick="switchTab('home')">
    <span class="tab-icon">🏠</span>
    <span class="tab-label" data-key="homeDashboard">Home</span>
  </button>
  <button class="tab-btn" data-tab="freezer" onclick="switchTab('freezer')">
```

- [ ] **Schritt 4: Shop-Overlay HTML einfügen**

Suche `<!-- BARCODE SCANNER OVERLAY -->` und füge DAVOR ein:

```html
<!-- SHOP OVERLAY -->
<div id="shop-overlay">
  <div class="shop-header">
    <div style="font-size:18px;font-weight:700">🛒 <span data-key="shopTitle">Einkaufen</span></div>
    <div style="display:flex;align-items:center;gap:12px">
      <span class="shop-counter" id="shop-counter">0 eingelagert</span>
      <button onclick="closeShopMode()" style="background:var(--primary);color:#fff;border:none;border-radius:10px;padding:8px 16px;font-size:14px;font-weight:700;cursor:pointer" id="shop-done-btn">✓ Fertig</button>
    </div>
  </div>
  <div class="shop-form">
    <div style="display:flex;gap:8px">
      <input class="form-input" id="shop-name" type="text" placeholder="Name…" style="flex:1">
      <button type="button" onclick="startBarcodeScanner()" style="background:var(--bg);border:1.5px solid var(--border);border-radius:10px;padding:0 12px;font-size:18px;cursor:pointer;flex-shrink:0">📷</button>
    </div>
    <div class="shop-form-row">
      <input class="form-input" id="shop-qty" type="number" min="0.1" step="0.1" value="1" style="width:80px;flex-shrink:0">
      <select class="form-select" id="shop-unit" style="flex:1"></select>
      <input class="form-input" id="shop-expiry" type="date" style="flex:1" placeholder="MHD">
    </div>
    <div class="shop-loc-btns">
      <button class="shop-loc-btn active" data-loc="freezer" onclick="setShopLocation('freezer')">🧊</button>
      <button class="shop-loc-btn" data-loc="fridge"  onclick="setShopLocation('fridge')">🥬</button>
      <button class="shop-loc-btn" data-loc="pantry"  onclick="setShopLocation('pantry')">🏺</button>
    </div>
    <button class="shop-add-btn" onclick="shopAddItem()" id="shop-add-btn">＋ Einlagern</button>
  </div>
  <div class="shop-recent">
    <div class="shop-recent-title" data-key="shopRecent">Zuletzt eingelagert:</div>
    <div id="shop-recent-list"></div>
  </div>
</div>
```

- [ ] **Schritt 5: Koch-Modal HTML einfügen**

Suche `<!-- BRING IMPORT MODAL -->` und füge DANACH ein:

```html
<!-- COOK MODAL -->
<div class="overlay" id="cook-overlay" onclick="closeModal(event)">
  <div class="modal" id="modal-cook">
    <div class="modal-handle"></div>
    <div class="modal-header">
      <div>
        <div class="modal-title" id="cook-modal-title">🍳 Zutaten entnehmen</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:2px" id="cook-recipe-name"></div>
      </div>
      <button class="icon-btn" onclick="closeAllModals()">✕</button>
    </div>
    <div class="modal-body" id="cook-modal-body" style="max-height:65vh;overflow-y:auto"></div>
    <div class="modal-footer">
      <button class="btn btn-outline" onclick="closeAllModals()" id="cook-cancel-btn">Abbrechen</button>
      <button class="btn btn-primary" onclick="confirmCook()" id="cook-confirm-btn">Entnehmen</button>
    </div>
  </div>
</div>
```

- [ ] **Schritt 6: Commit**
```bash
cd /tmp/vorratsmanager-ha && git add custom_components/vorratsmanager/www/index.html && git commit -m "feat: HTML für Dashboard-Tab, Shop-Overlay, Koch-Modal"
```

---

## Task 4: JS — renderDashboard() + switchTab + renderAll

**Files:**
- Modify: `index.html` — JS-Block

- [ ] **Schritt 1: `switchTab()` updaten**

Suche die bestehende `function switchTab(tab)` und ersetze sie komplett:

```javascript
function switchTab(tab) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(`tab-${tab}`)?.classList.add('active');
  document.querySelector(`.tab-btn[data-tab="${tab}"]`)?.classList.add('active');

  const fab = document.getElementById('fab-btn');
  fab.style.display = (tab === 'recipes' || tab === 'home') ? 'none' : 'flex';

  const headerIcons = { home: '🏠', freezer: '❄️', fridge: '🥬', pantry: '🏺', recipes: '👨‍🍳' };
  document.getElementById('header-icon').textContent = headerIcons[tab] || '🏠';

  if (tab === 'home')    renderDashboard();
  if (tab === 'pantry')  renderList('pantry');
  if (tab === 'recipes') renderRecipes();
}
```

- [ ] **Schritt 2: `renderAll()` updaten**

Suche die bestehende `function renderAll()` und ersetze sie komplett:

```javascript
function renderAll() {
  renderDashboard();
  renderFilters('freezer');
  renderFilters('fridge');
  renderFilters('pantry');
  renderList('freezer');
  renderList('fridge');
  renderList('pantry');
  renderStats('freezer');
  renderStats('fridge');
  renderStats('pantry');
  renderRecipes();
  updateTabBadges();
  updateI18n();
}
```

- [ ] **Schritt 3: `_matchIngredient()` Hilfsfunktion einfügen**

Füge direkt VOR `function renderRecipes()` ein:

```javascript
function _matchIngredient(ingredientStr, itemName) {
  const ing = String(ingredientStr).toLowerCase();
  const name = itemName.toLowerCase();
  // Match wenn Vorrats-Name in Zutat enthalten oder erste Wort der Zutat im Vorrats-Name
  return ing.includes(name) || name.includes(ing.split(/[\s,]+/)[0]);
}
```

- [ ] **Schritt 4: `renderDashboard()` Funktion einfügen**

Füge direkt VOR `function renderAll()` ein:

```javascript
function renderDashboard() {
  const el = document.getElementById('dashboard-content');
  if (!el) return;
  const lang = db.settings.lang;
  const notifyDays = Number(db.settings.notifyDays) || 2;

  // Ablaufende Items (alle Lagerorte, ≤7 Tage)
  const expiring = db.items
    .filter(i => { const d = daysUntilExpiry(i.expiry); return d !== null && d <= 7; })
    .sort((a, b) => daysUntilExpiry(a.expiry) - daysUntilExpiry(b.expiry));

  // Rezept-Scoring: wieviele ablaufende Items matchen Zutaten?
  const scoredRecipes = db.savedRecipes.map((r, idx) => {
    const ingredients = Array.isArray(r.ingredients) ? r.ingredients : [];
    const score = expiring.filter(item =>
      ingredients.some(ing => _matchIngredient(String(ing), item.name))
    ).length;
    return { r, idx, score };
  }).sort((a, b) => b.score - a.score).slice(0, 3);

  let html = '';

  // Block 1: Ablaufende Items
  if (expiring.length > 0) {
    html += `<div class="recipe-info-card">
      <div class="recipe-info-title">🔴 ${t('homeExpiring')}</div>
      <div style="display:flex;flex-direction:column;gap:8px;margin-top:8px">
        ${expiring.map(item => {
          const cat = getCatInfo(item.location, item.category);
          const days = daysUntilExpiry(item.expiry);
          const badge = expiryBadge(days, lang);
          return `<div class="item-card expiry-${expiryClass(days)}" style="cursor:pointer" onclick="openEditModal('${item.id}')">
            <div class="item-card-main" style="min-height:52px">
              <div class="item-emoji" style="width:40px;height:40px;font-size:22px">${cat.emoji}</div>
              <div class="item-body">
                <div class="item-name">${escHtml(item.name)}</div>
                <div class="item-meta"><span>${locLabel(item.location)}</span><span>·</span><span>${item.qty} ${escHtml(item.unit)}</span></div>
              </div>
              <div class="item-right">
                <span class="expiry-badge ${badge.cls}">${badge.text}</span>
              </div>
            </div>
          </div>`;
        }).join('')}
      </div>
    </div>`;
  }

  // Block 2: Rezeptvorschläge
  html += `<div class="recipe-info-card">
    <div class="recipe-info-title">👨‍🍳 ${t('homeCookToday')}</div>`;
  if (scoredRecipes.length === 0) {
    html += `<p class="recipe-tip" style="margin-top:8px">${t('homeNoFavorites')}</p>`;
  } else {
    html += `<div style="display:flex;flex-direction:column;gap:0;margin-top:10px">
      ${scoredRecipes.map(({ r, idx }) => {
        const appliance = r.appliance || 'Herd';
        const meta = APPLIANCE_META[appliance] || APPLIANCE_META['Herd'];
        return `<div style="display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--border)">
          <span style="font-size:24px">${meta.icon}</span>
          <div style="flex:1;min-width:0">
            <div style="font-weight:600;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${escHtml(r.name || '')}</div>
            <div style="font-size:12px;color:var(--text-muted);margin-top:1px">${appliance}${r.time ? ' · ⏱ ' + escHtml(r.time) : ''}</div>
          </div>
          <button onclick="openCookModal(db.savedRecipes[${idx}])" style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;border:none;border-radius:10px;padding:8px 14px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap;flex-shrink:0">🍳 ${t('cookBtn')}</button>
        </div>`;
      }).join('')}
    </div>`;
  }
  html += `</div>`;

  // Block 3: Einkaufen-Button
  html += `<button onclick="openShopMode()" style="width:100%;padding:18px;background:linear-gradient(135deg,#F59E0B,#D97706);color:#fff;border:none;border-radius:var(--radius);font-size:17px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 4px 12px rgba(245,158,11,0.35)">
    🛒 ${t('homeShopBtn')}
  </button>`;

  el.innerHTML = html;
}
```

- [ ] **Schritt 5: Deploy + manuell testen**

```bash
echo '#!/bin/bash
echo 3001' > /tmp/askpass.sh && chmod +x /tmp/askpass.sh
cat /tmp/vorratsmanager-ha/custom_components/vorratsmanager/www/index.html | \
  DISPLAY=:0 SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force \
  ssh -o StrictHostKeyChecking=no ha@192.168.1.11 -p 22 \
  'sudo tee /homeassistant/www/vorratsmanager/index.html > /dev/null && echo OK'
```

Prüfen:
- [ ] App öffnet auf Home-Tab (🏠)
- [ ] Ablaufende Items erscheinen in Block 1 (falls vorhanden)
- [ ] Gespeicherte Rezepte erscheinen in Block 2 mit 🍳-Button
- [ ] Gelber Einkaufen-Button sichtbar
- [ ] Tab-Wechsel zu Gefriertruhe/Kühlschrank/Vorratsraum/Rezepte funktioniert
- [ ] FAB (＋) auf Home-Tab versteckt, auf Lagerort-Tabs sichtbar

- [ ] **Schritt 6: Commit**
```bash
cd /tmp/vorratsmanager-ha && git add custom_components/vorratsmanager/www/index.html && git commit -m "feat: Dashboard-Tab mit ablaufenden Items und Rezeptvorschlägen"
```

---

## Task 5: JS — Einkauf-Modus

**Files:**
- Modify: `index.html` — JS-Block

- [ ] **Schritt 1: State-Variable einfügen**

Suche `let recentRecipeNames = [];` und füge DANACH ein:

```javascript
let _shopLocation = 'freezer';
let _shopAddedCount = 0;
let _shopRecentItems = []; // letzte 5 Item-IDs dieser Session
```

- [ ] **Schritt 2: Shop-Funktionen einfügen**

Füge direkt VOR `// ============================================================` (vor der `init()` Funktion) ein:

```javascript
// ============================================================
// EINKAUF-MODUS
// ============================================================
function openShopMode() {
  _shopLocation = 'freezer';
  _shopAddedCount = 0;
  _shopRecentItems = [];

  // Felder leeren
  document.getElementById('shop-name').value = '';
  document.getElementById('shop-qty').value = '1';
  document.getElementById('shop-expiry').value = '';

  // Unit-Select befüllen
  const unitEl = document.getElementById('shop-unit');
  const lang = db.settings.lang;
  const units = UNITS[lang] || UNITS['de'];
  unitEl.innerHTML = units.map(u => `<option value="${u}">${u}</option>`).join('');

  // Lagerort-Buttons updaten
  setShopLocation('freezer');

  // Counter + Done-Button Labels
  _updateShopCounter();
  document.getElementById('shop-done-btn').textContent = '✓ ' + t('shopDone');
  document.getElementById('shop-add-btn').textContent = t('shopAddBtn');

  renderShopRecent();
  document.getElementById('shop-overlay').classList.add('open');
  setTimeout(() => document.getElementById('shop-name').focus(), 200);
}

function setShopLocation(loc) {
  _shopLocation = loc;
  document.querySelectorAll('.shop-loc-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.loc === loc);
  });
}

function shopAddItem() {
  const name = document.getElementById('shop-name').value.trim();
  if (!name) {
    document.getElementById('shop-name').focus();
    return;
  }
  const lang = db.settings.lang;
  const cats = CATEGORIES[_shopLocation];
  const item = {
    id: generateId(),
    name,
    location: _shopLocation,
    category: cats[cats.length - 1].id,
    qty: parseFloat(document.getElementById('shop-qty').value) || 1,
    unit: document.getElementById('shop-unit').value,
    added: today(),
    expiry: document.getElementById('shop-expiry').value || null,
    notes: '',
  };

  db.items.unshift(item);
  _shopAddedCount++;
  _shopRecentItems.unshift(item.id);
  if (_shopRecentItems.length > 5) _shopRecentItems.pop();

  // localStorage sichern, KEIN Server-Sync (erst bei Fertig)
  saveDb(false);

  // Formular leeren (Lagerort + Unit beibehalten)
  document.getElementById('shop-name').value = '';
  document.getElementById('shop-qty').value = '1';
  document.getElementById('shop-expiry').value = '';
  document.getElementById('shop-name').focus();

  _updateShopCounter();
  renderShopRecent();
}

function _updateShopCounter() {
  document.getElementById('shop-counter').textContent = t('shopAdded', _shopAddedCount);
}

function renderShopRecent() {
  const el = document.getElementById('shop-recent-list');
  if (_shopRecentItems.length === 0) {
    el.innerHTML = `<div style="font-size:13px;color:var(--text-light);padding:8px 0">${t('shopEmpty')}</div>`;
    return;
  }
  const locIcons = { freezer: '🧊', fridge: '🥬', pantry: '🏺' };
  el.innerHTML = _shopRecentItems.map(id => {
    const item = db.items.find(i => i.id === id);
    if (!item) return '';
    return `<div class="shop-recent-item">
      <span style="font-size:20px">${locIcons[item.location] || '📦'}</span>
      <span style="flex:1;font-weight:500">${escHtml(item.name)}</span>
      <span style="color:var(--text-muted);font-size:13px">${item.qty} ${escHtml(item.unit)}</span>
    </div>`;
  }).join('');
}

function closeShopMode() {
  document.getElementById('shop-overlay').classList.remove('open');
  if (_shopAddedCount > 0) {
    saveDb(); // jetzt erst Server-Sync
    renderAll();
    showToast(t('shopAdded', _shopAddedCount));
  }
}
```

- [ ] **Schritt 3: Deploy + manuell testen**

```bash
cat /tmp/vorratsmanager-ha/custom_components/vorratsmanager/www/index.html | \
  DISPLAY=:0 SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force \
  ssh -o StrictHostKeyChecking=no ha@192.168.1.11 -p 22 \
  'sudo tee /homeassistant/www/vorratsmanager/index.html > /dev/null && echo OK'
```

Prüfen:
- [ ] Gelber Button öffnet Shop-Overlay
- [ ] Lagerort-Buttons ❄️ 🥬 🏺 wechseln korrekt (aktiver Button hervorgehoben)
- [ ] Item eingeben + „＋ Einlagern" → Formular leert sich, Zähler steigt
- [ ] Zuletzt-eingelagert-Liste zeigt letzte 5 Items
- [ ] „✓ Fertig" schließt Overlay + Toast „X eingelagert" erscheint
- [ ] Items erscheinen im richtigen Lagerort-Tab
- [ ] Barcode-Button öffnet Scanner (falls Chrome)

- [ ] **Schritt 4: Commit**
```bash
cd /tmp/vorratsmanager-ha && git add custom_components/vorratsmanager/www/index.html && git commit -m "feat: Einkauf-Schnellmodus als Vollbild-Overlay"
```

---

## Task 6: JS — Rezept-Kochen-Flow

**Files:**
- Modify: `index.html` — JS-Block

- [ ] **Schritt 1: State-Variable einfügen**

Suche `let _shopLocation = 'freezer';` und füge DANACH ein:

```javascript
let _cookRecipe = null;
let _cookTakeAmounts = {}; // { itemId: amount }
let _cookChecked = {};     // { itemId: boolean }
```

- [ ] **Schritt 2: Kochen-Funktionen einfügen**

Füge direkt nach den Shop-Funktionen (nach `closeShopMode()`) ein:

```javascript
// ============================================================
// REZEPT-KOCHEN-FLOW
// ============================================================
function openCookModal(recipe) {
  if (!recipe) return;
  _cookRecipe = recipe;
  _cookTakeAmounts = {};
  _cookChecked = {};

  const lang = db.settings.lang;
  const ingredients = Array.isArray(recipe.ingredients) ? recipe.ingredients : [];

  // Matching: welche Vorrats-Items passen zu Zutaten?
  const matched = [];
  const unmatched = [];

  ingredients.forEach(ing => {
    const ingStr = typeof ing === 'string' ? ing : (ing.name || String(ing));
    const found = db.items.filter(item => _matchIngredient(ingStr, item.name));
    if (found.length > 0) {
      found.forEach(item => {
        if (!matched.find(m => m.item.id === item.id)) {
          matched.push({ item, ingStr });
        }
      });
    } else {
      unmatched.push(ingStr);
    }
  });

  // Defaults: alle gecheckt, volle Menge
  matched.forEach(({ item }) => {
    _cookChecked[item.id] = true;
    _cookTakeAmounts[item.id] = item.qty;
  });

  // Titel
  document.getElementById('cook-modal-title').textContent = '🍳 ' + t('cookTitle');
  document.getElementById('cook-recipe-name').textContent = recipe.name || '';
  document.getElementById('cook-cancel-btn').textContent = t('btnCancel');

  _renderCookModal(matched, unmatched);
  document.getElementById('cook-overlay').classList.add('open');
}

function _renderCookModal(matched, unmatched) {
  const lang = db.settings.lang;
  const checkedCount = matched.filter(({ item }) => _cookChecked[item.id]).length;
  document.getElementById('cook-confirm-btn').textContent = t('cookConfirm', checkedCount);

  let html = '';

  if (matched.length > 0) {
    html += `<div class="cook-section-title">✅ ${t('cookInStock')}</div>`;
    html += matched.map(({ item }) => {
      const checked = _cookChecked[item.id];
      const amount = _cookTakeAmounts[item.id];
      const step = item.qty <= 5 ? 0.5 : 1;
      const locIcons = { freezer: '🧊', fridge: '🥬', pantry: '🏺' };
      return `<div class="cook-item-row" id="crow-${item.id}" style="opacity:${checked ? 1 : 0.45}">
        <input type="checkbox" style="width:18px;height:18px;accent-color:var(--primary);flex-shrink:0;cursor:pointer"
          ${checked ? 'checked' : ''} onchange="toggleCookItem('${item.id}',this.checked)">
        <div style="flex:1;min-width:0">
          <div class="cook-item-name">${escHtml(item.name)}</div>
          <div class="cook-item-meta">${locIcons[item.location] || ''} ${item.qty} ${escHtml(item.unit)}</div>
        </div>
        <div class="cook-stepper">
          <button class="cook-step-btn" onclick="adjustCookItem('${item.id}',-${step},${item.qty})">−</button>
          <span class="cook-qty-val" id="cqty-${item.id}">${amount}</span>
          <button class="cook-step-btn" onclick="adjustCookItem('${item.id}',${step},${item.qty})">+</button>
          <span style="font-size:11px;color:var(--text-muted);min-width:24px">${escHtml(item.unit)}</span>
        </div>
      </div>`;
    }).join('');
  }

  if (unmatched.length > 0) {
    html += `<div class="cook-section-title" style="margin-top:${matched.length>0?'16':'0'}px">❌ ${t('cookMissing')}</div>`;
    html += unmatched.map(ing => `<div class="cook-missing-item">
      <span>${escHtml(String(ing))}</span>
      ${_inHaPanel ? `<button class="cook-shop-btn" onclick="addIngredientToShop('${escAttr(String(ing))}')">${t('cookAddShop')}</button>` : ''}
    </div>`).join('');
  }

  if (matched.length === 0 && unmatched.length === 0) {
    html = `<p style="color:var(--text-muted);text-align:center;padding:24px;font-size:14px">Keine Zutaten gefunden.</p>`;
  }

  document.getElementById('cook-modal-body').innerHTML = html;
}

function toggleCookItem(itemId, checked) {
  _cookChecked[itemId] = checked;
  const row = document.getElementById(`crow-${itemId}`);
  if (row) row.style.opacity = checked ? '1' : '0.45';
  const checkedCount = Object.values(_cookChecked).filter(Boolean).length;
  document.getElementById('cook-confirm-btn').textContent = t('cookConfirm', checkedCount);
}

function adjustCookItem(itemId, delta, maxQty) {
  const item = db.items.find(i => i.id === itemId);
  if (!item) return;
  const step = maxQty <= 5 ? 0.5 : 1;
  const current = _cookTakeAmounts[itemId] || item.qty;
  const newVal = Math.max(0.1, Math.min(maxQty, Math.round((current + delta) * 10) / 10));
  _cookTakeAmounts[itemId] = newVal;
  const el = document.getElementById(`cqty-${itemId}`);
  if (el) el.textContent = newVal;
}

async function addIngredientToShop(name) {
  if (!_inHaPanel) return;
  try {
    await callServiceViaPanel('todo', 'add_item', { entity_id: db.settings.todoEntity || 'todo.einkauf', item: name });
    showToast('🛒 ' + name + ' → Einkaufsliste ✓');
  } catch(e) { showToast('🛒 Fehler'); }
}

function confirmCook() {
  let removed = 0;
  Object.entries(_cookChecked).forEach(([itemId, checked]) => {
    if (!checked) return;
    const item = db.items.find(i => i.id === itemId);
    if (!item) return;
    const take = _cookTakeAmounts[itemId] || item.qty;
    item.qty = Math.max(0, Math.round((item.qty - take) * 10) / 10);
    if (item.qty <= 0) db.items = db.items.filter(i => i.id !== itemId);
    removed++;
  });
  saveDb();
  closeAllModals();
  renderAll();
  showToast(t('cookDone', removed));
}
```

- [ ] **Schritt 3: „🍳 Kochen"-Button in `renderSavedRecipes()` einfügen**

Suche in `renderSavedRecipes()` diese Zeile:
```javascript
          <button class="btn-save-recipe saved" title="${t('removeSaved')}" onclick="event.stopPropagation();removeSavedRecipe(${i})">⭐</button>
```
und ersetze sie durch:
```javascript
          <button class="btn-save-recipe saved" title="${t('removeSaved')}" onclick="event.stopPropagation();removeSavedRecipe(${i})">⭐</button>
          <button style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;border:none;border-radius:8px;padding:4px 10px;font-size:13px;font-weight:600;cursor:pointer;flex-shrink:0" title="${t('cookBtn')}" onclick="event.stopPropagation();openCookModal(db.savedRecipes[${i}])">🍳</button>
```

- [ ] **Schritt 4: „🍳 Kochen"-Button in `renderAIRecipeCard()` einfügen**

Suche in `renderAIRecipeCard()` diese Zeile:
```javascript
        <button class="btn-save-recipe${db.savedRecipes.some(s => s.name === r.name) ? ' saved' : ''}" title="${t('saveRecipe')}" onclick="event.stopPropagation();saveAIRecipe(${i})">${t('saveRecipe')}</button>
```
und ersetze sie durch:
```javascript
        <button class="btn-save-recipe${db.savedRecipes.some(s => s.name === r.name) ? ' saved' : ''}" title="${t('saveRecipe')}" onclick="event.stopPropagation();saveAIRecipe(${i})">${t('saveRecipe')}</button>
        <button style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;border:none;border-radius:8px;padding:4px 10px;font-size:13px;font-weight:600;cursor:pointer;flex-shrink:0" title="${t('cookBtn')}" onclick="event.stopPropagation();openCookModal(aiRecipes[${i}])">🍳</button>
```

- [ ] **Schritt 5: Deploy + manuell testen**

```bash
cat /tmp/vorratsmanager-ha/custom_components/vorratsmanager/www/index.html | \
  DISPLAY=:0 SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force \
  ssh -o StrictHostKeyChecking=no ha@192.168.1.11 -p 22 \
  'sudo tee /homeassistant/www/vorratsmanager/index.html > /dev/null && echo OK'
```

Prüfen:
- [ ] 🍳-Button erscheint in gespeicherten Favoriten-Karten
- [ ] 🍳-Button erscheint in KI-Rezept-Karten
- [ ] 🍳-Button auf Dashboard-Tab funktioniert
- [ ] Koch-Modal öffnet sich mit Rezept-Name im Titel
- [ ] Gematchte Items mit Checkbox + Menge-Stepper sichtbar
- [ ] Stepper erhöht/verringert Menge korrekt (min 0.1, max item.qty)
- [ ] Checkbox deaktiviert → Row ausgegraut, Zähler im Button sinkt
- [ ] „Entnehmen (N)"-Button: Items werden korrekt reduziert/entfernt
- [ ] Toast „N Zutaten entnommen ✓" erscheint
- [ ] Nicht gematchte Zutaten in ❌-Sektion mit „+ Einkaufsliste"-Button (wenn in HA)

- [ ] **Schritt 6: Commit**
```bash
cd /tmp/vorratsmanager-ha && git add custom_components/vorratsmanager/www/index.html && git commit -m "feat: Rezept-Kochen-Flow mit Teilentnahme aus Vorrat"
```

---

## Task 7: Finaler Deploy + Abnahme

- [ ] **Schritt 1: Vollständigen Deploy durchführen**
```bash
cat /tmp/vorratsmanager-ha/custom_components/vorratsmanager/www/index.html | \
  DISPLAY=:0 SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force \
  ssh -o StrictHostKeyChecking=no ha@192.168.1.11 -p 22 \
  'sudo tee /homeassistant/www/vorratsmanager/index.html > /dev/null && echo OK'
```

- [ ] **Schritt 2: Gesamttest PC-Browser**
  - [ ] App lädt auf Home-Tab, alle 3 Blöcke sichtbar
  - [ ] Alle 5 Tabs navigierbar, aktiver Tab korrekt hervorgehoben
  - [ ] Einkauf-Modus: mehrere Items ohne Schließen einlagern
  - [ ] Koch-Flow: Rezept wählen, Mengen anpassen, bestätigen, Vorrat korrekt reduziert
  - [ ] Dark Mode funktioniert auf allen neuen Komponenten
  - [ ] Sprach-Wechsel (EN/RU) zeigt neue Keys korrekt übersetzt

- [ ] **Schritt 3: Gesamttest HA Mobile App**
  - [ ] Home-Tab lädt korrekt (kein weißer Fleck, kein Overflow)
  - [ ] Einkauf-Overlay auf Vollbild korrekt
  - [ ] Koch-Modal Stepper touch-bedienbar (min 44px Touch-Target durch cook-step-btn 30px — prüfen ob ausreichend, ggf. auf 40px erhöhen)
  - [ ] Shop-Barcode-Button öffnet Scanner oder zeigt „nicht unterstützt"-Toast

- [ ] **Schritt 4: Final Commit**
```bash
cd /tmp/vorratsmanager-ha && git add -A && git status
# Sicherstellen dass nur index.html geändert, dann:
git commit -m "feat: Dashboard, Einkauf-Modus, Rezept-Kochen-Flow – vollständig"
```

> **GitHub push:** NICHT automatisch — erst nach Freigabe durch den User.
