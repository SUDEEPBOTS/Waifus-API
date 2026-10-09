/**
 * Official JavaScript / Node.js SDK for Waifu Database API (https://wafus.vercel.app)
 */

class WaifuClient {
  constructor(apiKey = null, baseUrl = 'https://wafus.vercel.app') {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
  }

  async _request(path, options = {}) {
    const url = `${this.baseUrl}${path}`;
    const headers = {
      'Accept': 'application/json',
      ...(options.headers || {})
    };

    if (this.apiKey) {
      headers['x-api-key'] = this.apiKey;
    }

    if (options.body && typeof options.body === 'object') {
      headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(options.body);
    }

    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Waifu API Error [${res.status}]: ${errText}`);
    }
    return res.json();
  }

  /** Generate or retrieve API Key */
  async getApiKey() {
    const res = await this._request('/');
    if (res.api_key) {
      this.apiKey = res.api_key;
    }
    return res;
  }

  /** Health check ping */
  async ping() {
    return this._request('/Ping');
  }

  /** Database stats and total count */
  async stats() {
    return this._request('/Stats');
  }

  /** Roll a random waifu */
  async random() {
    return this._request('/Random');
  }

  /** Search waifu by name */
  async findByName(name) {
    return this._request(`/Find?name=${encodeURIComponent(name)}`);
  }

  /** Search waifu by ID */
  async findById(waifuId) {
    return this._request(`/FindById/${encodeURIComponent(waifuId)}`);
  }

  /** List waifus with pagination */
  async list(skip = 0, limit = 20) {
    return this._request(`/List?skip=${skip}&limit=${limit}`);
  }

  /** Add waifu (Requires API Key) */
  async addWaifu(data) {
    return this._request('/Waifuadd', {
      method: 'POST',
      body: data
    });
  }

  /** Update waifu (Requires API Key) */
  async updateWaifu(name, data) {
    return this._request(`/Update?name=${encodeURIComponent(name)}`, {
      method: 'PUT',
      body: data
    });
  }

  /** Remove waifu by name (Requires API Key) */
  async removeWaifu(name) {
    return this._request(`/Rmwafus?name=${encodeURIComponent(name)}`, {
      method: 'DELETE'
    });
  }

  /** Remove waifu by ID (Requires API Key) */
  async removeById(waifuId) {
    return this._request(`/RmById/${encodeURIComponent(waifuId)}`, {
      method: 'DELETE'
    });
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = WaifuClient;
}
