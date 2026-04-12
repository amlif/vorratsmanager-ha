class VorratsManagerPanel extends HTMLElement {
  set hass(hass) {
    const firstSet = !this._hass;
    this._hass = hass;

    if (firstSet) {
      hass.connection.subscribeEvents((event) => {
        this._iframe?.contentWindow?.postMessage(
          { type: 'vorrat-updated', updated: event.data?.updated }, '*'
        );
      }, 'vorratsmanager_updated').then(unsub => { this._unsub = unsub; });
    }

    if (this._iframeLoaded) {
      this._iframe?.contentWindow?.postMessage({ type: 'ha-ready', url: window.location.origin }, '*');
    }
  }

  connectedCallback() {
    const shadow = this.attachShadow({ mode: "open" });
    const style = document.createElement("style");
    style.textContent = ":host{display:block;width:100%;height:100%;overflow:hidden;}iframe{display:block;width:100%;height:100%;border:none;}";
    shadow.appendChild(style);

    const iframe = document.createElement("iframe");
    iframe.src = "/local/vorratsmanager/index.html";
    this._iframe = iframe;
    this._iframeLoaded = false;

    iframe.addEventListener('load', () => {
      this._iframeLoaded = true;
      if (this._hass) {
        iframe.contentWindow?.postMessage({ type: 'ha-ready', url: window.location.origin }, '*');
      }
    });

    shadow.appendChild(iframe);

    this._msgHandler = async (e) => {
      if (!this._hass) return;

      if (e.data?.type === 'vorrat-save') {
        try {
          await this._hass.callService('vorratsmanager', 'vorrat_save', {
            items: e.data.items,
            settings: e.data.settings || {},
            updated: e.data.updated
          });
        } catch(err) { console.warn('vorrat-save failed', err); }
      }

      else if (e.data?.type === 'vorrat-ai') {
        const reqId = e.data.reqId;
        try {
          const result = await this._hass.connection.sendMessagePromise({
            type: 'call_service',
            domain: 'ai_task',
            service: 'generate_data',
            service_data: { task_name: 'VorratsManager Rezept', instructions: e.data.prompt },
            return_response: true
          });
          this._iframe?.contentWindow?.postMessage({ type: 'vorrat-ai-result', reqId, result }, '*');
        } catch(err) {
          this._iframe?.contentWindow?.postMessage({ type: 'vorrat-ai-result', reqId, error: String(err) }, '*');
        }
      }
    };
    window.addEventListener('message', this._msgHandler);

    const setH = () => { const h = this.clientHeight; if (h > 50) iframe.style.height = h + "px"; };
    setH();
    try { new ResizeObserver(setH).observe(this); } catch(e) {}
    let p = this.parentElement;
    while (p && p.tagName !== "BODY") { if (!p.style.height) p.style.height = "100%"; p = p.parentElement; }
  }

  disconnectedCallback() {
    if (this._msgHandler) window.removeEventListener('message', this._msgHandler);
    if (this._unsub) this._unsub();
  }
}
customElements.define("vorrats-manager-panel", VorratsManagerPanel);
