/**
 * CaseBrain Connector Hub
 * Manages connections to all external services
 */

const connectors = {
  github: {
    name: 'GitHub',
    token: process.env.GITHUB_TOKEN,
    baseURL: 'https://api.github.com',
    async test() {
      const res = await fetch(this.baseURL + '/user', {
        headers: { Authorization: 'token ' + this.token }
      });
      return res.ok;
    }
  },
  mem0: {
    name: 'Mem0',
    apiKey: process.env.MEM0_API_KEY,
    baseURL: 'https://api.mem0.ai/v1',
    async test() {
      const res = await fetch(this.baseURL + '/memories/', {
        headers: { 'Authorization': 'Token ' + this.apiKey }
      });
      return res.ok;
    }
  },
  pinecone: {
    name: 'Pinecone',
    apiKey: process.env.PINECONE_API_KEY,
    index: 'legal-memory',
    async test() {
      return !!this.apiKey;
    }
  },
  groq: {
    name: 'Groq',
    apiKey: process.env.GROQ_API_KEY,
    baseURL: 'https://api.groq.com/openai/v1',
    async test() {
      const res = await fetch(this.baseURL + '/models', {
        headers: { Authorization: 'Bearer ' + this.apiKey }
      });
      return res.ok;
    }
  },
  supabase: {
    name: 'Supabase',
    url: process.env.SUPABASE_URL,
    key: process.env.SUPABASE_ANON_KEY,
    serviceKey: process.env.SUPABASE_SERVICE_ROLE,
    async test() {
      const res = await fetch(this.url + '/rest/v1/', {
        headers: { apikey: this.key, Authorization: 'Bearer ' + this.key }
      });
      return res.ok;
    }
  },
  courtlistener: {
    name: 'CourtListener',
    token: process.env.COURTLISTENER_TOKEN,
    baseURL: 'https://www.courtlistener.com/api/rest/v3',
    async test() {
      const res = await fetch(this.baseURL + '/courts/', {
        headers: { Authorization: 'Token ' + this.token }
      });
      return res.ok;
    }
  },
  notion: {
    name: 'Notion',
    token: process.env.NOTION_TOKEN,
    baseURL: 'https://api.notion.com/v1',
    async test() {
      const res = await fetch(this.baseURL + '/users/me', {
        headers: {
          'Authorization': 'Bearer ' + this.token,
          'Notion-Version': '2022-06-28'
        }
      });
      return res.ok;
    }
  },
  linear: {
    name: 'Linear',
    apiKey: process.env.LINEAR_API_KEY,
    baseURL: 'https://api.linear.app/graphql',
    async test() {
      const res = await fetch(this.baseURL, {
        method: 'POST',
        headers: { Authorization: this.apiKey, 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: '{ viewer { name } }' })
      });
      return res.ok;
    }
  }
};

class ConnectorHub {
  constructor() {
    this.status = {};
  }

  async testAll() {
    const results = {};
    for (const [name, connector] of Object.entries(connectors)) {
      try {
        results[name] = {
          name: connector.name,
          status: await connector.test() ? 'connected' : 'failed',
          hasConfig: !!(connector.token || connector.apiKey || connector.key)
        };
      } catch (e) {
        results[name] = { name: connector.name, status: 'error', error: e.message };
      }
    }
    this.status = results;
    return results;
  }

  getConnector(name) {
    return connectors[name];
  }

  getStatus() {
    return this.status;
  }
}

module.exports = { ConnectorHub, connectors };
