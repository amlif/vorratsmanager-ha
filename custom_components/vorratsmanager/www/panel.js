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
    iframe.src = "/local/vorratsmanager/index.html?v=1.4.4";
    iframe.allow = "camera; microphone";
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
            savedRecipes: e.data.savedRecipes || [],
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

      else if (e.data?.type === 'vorrat-barcode-start') {
        this._startCameraBridge();
      }

      else if (e.data?.type === 'vorrat-barcode-stop') {
        this._stopCameraBridge();
      }

      else if (e.data?.type === 'vorrat-ha-call') {
        const reqId = e.data.reqId;
        try {
          let result;
          if (e.data.returnResponse) {
            result = await this._hass.connection.sendMessagePromise({
              type: 'call_service',
              domain: e.data.domain,
              service: e.data.service,
              service_data: e.data.data || {},
              return_response: true
            });
          } else {
            await this._hass.callService(e.data.domain, e.data.service, e.data.data || {});
            result = { ok: true };
          }
          this._iframe?.contentWindow?.postMessage({ type: 'vorrat-ha-result', reqId, result }, '*');
        } catch(err) {
          this._iframe?.contentWindow?.postMessage({ type: 'vorrat-ha-result', reqId, error: String(err) }, '*');
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

  async _startCameraBridge() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' } } });
      this._camStream = stream;

      // Video muss im Shadow DOM sein damit der WebView es tatsächlich abspielt
      const video = document.createElement('video');
      video.srcObject = stream;
      video.autoplay = true;
      video.playsInline = true;
      video.muted = true;
      video.setAttribute('playsinline', '');
      video.style.cssText = 'position:absolute;width:1px;height:1px;opacity:0.01;pointer-events:none;';
      this.shadowRoot.appendChild(video);
      this._camVideo = video;

      await new Promise(r => {
        if (video.readyState >= 1) { r(); return; }
        video.addEventListener('loadedmetadata', r, { once: true });
      });
      video.play().catch(() => {});

      // Canvas für Frame-Capture (robuster als createImageBitmap auf video)
      const cap = document.createElement('canvas');
      this._camInterval = setInterval(() => {
        if (!this._camStream || video.readyState < 2 || !video.videoWidth) return;
        cap.width = video.videoWidth;
        cap.height = video.videoHeight;
        cap.getContext('2d').drawImage(video, 0, 0);
        createImageBitmap(cap).then(bitmap => {
          this._iframe?.contentWindow?.postMessage({ type: 'vorrat-camera-frame', bitmap }, '*', [bitmap]);
        }).catch(() => {});
      }, 250);
    } catch(e) {
      this._iframe?.contentWindow?.postMessage({ type: 'vorrat-camera-error' }, '*');
    }
  }

  _stopCameraBridge() {
    clearInterval(this._camInterval);
    this._camInterval = null;
    if (this._camVideo) { this._camVideo.remove(); this._camVideo = null; }
    if (this._camStream) { this._camStream.getTracks().forEach(t => t.stop()); this._camStream = null; }
  }

  disconnectedCallback() {
    if (this._msgHandler) window.removeEventListener('message', this._msgHandler);
    if (this._unsub) this._unsub();
    this._stopCameraBridge();
  }
}
customElements.define("vorrats-manager-panel", VorratsManagerPanel);
