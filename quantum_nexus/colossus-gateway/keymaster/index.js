/**
 * KEYMASTER - Unified Key Management Service
 * 
 * Responsibilities:
 * - Store/retrieve all API keys from Supabase vault
 * - Single unified auth token for all services
 * - Key rotation and upgrade management
 * - Health checks for all connected services
 * - Proxy API calls through unified interface
 */

const { createClient } = require('@supabase/supabase-js');

class Keymaster {
  constructor() {
    this.supabase = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_SERVICE_ROLE
    );
    this.cache = new Map();
    this.cacheTTL = 5 * 60 * 1000; // 5 min cache
  }

  // Get a key by service name
  async getKey(service) {
    const cached = this.cache.get(service);
    if (cached && Date.now() - cached.ts < this.cacheTTL) {
      return cached.value;
    }

    const { data, error } = await this.supabase
      .from('secrets_vault')
      .select('key_value')
      .eq('service', service)
      .single();

    if (error || !data) {
      // Fallback to env vars
      return process.env[service] || null;
    }

    this.cache.set(service, { value: data.key_value, ts: Date.now() });
    return data.key_value;
  }

  // Set/update a key
  async setKey(service, keyName, keyValue, category = 'general') {
    const { error } = await this.supabase
      .from('secrets_vault')
      .upsert({
        service,
        key_name: keyName,
        key_value: keyValue,
        category,
        updated_at: new Date().toISOString()
      }, { onConflict: 'service' });

    if (!error) {
      this.cache.delete(service);
    }
    return !error;
  }

  // Get all keys (masked)
  async getAllKeys() {
    const { data, error } = await this.supabase
      .from('secrets_vault')
      .select('service, key_name, category, updated_at');

    if (error) return [];

    return data.map(k => ({
      ...k,
      key_value: '••••••••' + k.key_name.slice(-4)
    }));
  }

  // Get all keys for a category
  async getKeysByCategory(category) {
    const { data, error } = await this.supabase
      .from('secrets_vault')
      .select('service, key_name, key_value, category')
      .eq('category', category);

    if (error) return [];
    return data;
  }

  // Check health of a service
  async checkHealth(service) {
    const key = await this.getKey(service);
    if (!key) return { service, status: 'no_key', healthy: false };

    try {
      const checkers = {
        github: async (k) => {
          const res = await fetch('https://api.github.com/user', {
            headers: { Authorization: 'token ' + k }
          });
          return res.ok;
        },
        groq: async (k) => {
          const res = await fetch('https://api.groq.com/openai/v1/models', {
            headers: { Authorization: 'Bearer ' + k }
          });
          return res.ok;
        },
        mem0: async (k) => {
          const res = await fetch('https://api.mem0.ai/v1/memories/', {
            headers: { Authorization: 'Token ' + k }
          });
          return res.ok;
        },
        supabase: async (k) => {
          const res = await fetch(process.env.SUPABASE_URL + '/rest/v1/', {
            headers: { apikey: k }
          });
          return res.ok;
        }
      };

      const checker = checkers[service];
      if (!checker) return { service, status: 'no_checker', healthy: true };

      const healthy = await checker(key);
      return { service, status: healthy ? 'healthy' : 'unhealthy', healthy };
    } catch (e) {
      return { service, status: 'error', healthy: false, error: e.message };
    }
  }

  // Check all services
  async checkAllHealth() {
    const services = ['github', 'groq', 'mem0', 'supabase'];
    const results = await Promise.all(
      services.map(s => this.checkHealth(s))
    );
    return results.reduce((acc, r) => {
      acc[r.service] = r;
      return acc;
    }, {});
  }

  // Rotate a key
  async rotateKey(service, newKey) {
    const existing = await this.getKey(service);
    if (!existing) return { success: false, error: 'Key not found' };

    // Store old key as backup
    await this.setKey(service + '_backup', 'backup', existing, 'backup');
    // Set new key
    await this.setKey(service, service, newKey, 'rotated');

    return { success: true, message: `Key rotated for ${service}` };
  }

  // Get unified auth token
  async getUnifiedToken() {
    const { data, error } = await this.supabase
      .from('secrets_vault')
      .select('service, key_value')
      .in('service', ['github', 'groq', 'mem0', 'supabase']);

    if (error) return null;

    const payload = {
      sub: 'colossus-gateway',
      services: data.map(d => d.service),
      iat: Math.floor(Date.now() / 1000),
      exp: Math.floor(Date.now() / 1000) + 3600
    };

    return Buffer.from(JSON.stringify(payload)).toString('base64');
  }
}

module.exports = Keymaster;
