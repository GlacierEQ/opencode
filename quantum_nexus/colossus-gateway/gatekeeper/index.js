/**
 * GATEKEEPER - Agent Swarm Orchestration Service
 * 
 * Responsibilities:
 * - Diamond agent structure (hierarchical routing)
 * - Enterprise agent management
 * - Deep research orchestration
 * - Presentation preparation
 * - Swarm rails (guardrails for agent actions)
 * - Endpoint management
 */

class Gatekeeper {
  constructor() {
    this.agents = new Map();
    this.teams = new Map();
    this.tasks = new Map();
    this.rails = new Map();
    this.initDefaultAgents();
    this.initRails();
  }

  initDefaultAgents() {
    // Diamond Structure: Executive → Manager → Worker → Specialist
    const agents = {
      // Executive Layer
      'executive': {
        id: 'executive',
        name: 'Executive Orchestrator',
        tier: 'executive',
        capabilities: ['route', 'delegate', 'escalate', 'summarize'],
        status: 'active',
        description: 'Top-level decision maker, routes to managers'
      },
      // Manager Layer
      'research-manager': {
        id: 'research-manager',
        name: 'Research Manager',
        tier: 'manager',
        capabilities: ['research', 'analyze', 'verify', 'compile'],
        status: 'active',
        agents: ['deep-researcher', 'fact-checker', 'source-analyzer'],
        description: 'Manages research operations'
      },
      'legal-manager': {
        id: 'legal-manager',
        name: 'Legal Manager',
        tier: 'manager',
        capabilities: ['legal', 'draft', 'file', 'cite'],
        status: 'active',
        agents: ['motion-drafter', 'evidence-analyzer', 'deadline-tracker'],
        description: 'Manages legal operations'
      },
      'ops-manager': {
        id: 'ops-manager',
        name: 'Operations Manager',
        tier: 'manager',
        capabilities: ['deploy', 'monitor', 'scale', 'debug'],
        status: 'active',
        agents: ['devops', 'monitor', 'backup'],
        description: 'Manages infrastructure'
      },
      // Worker Layer
      'deep-researcher': {
        id: 'deep-researcher',
        name: 'Deep Researcher',
        tier: 'worker',
        capabilities: ['web-search', 'paper-analysis', 'citation', 'synthesis'],
        status: 'active',
        tools: ['webfetch', 'websearch', 'grep'],
        description: 'Conducts deep research on any topic'
      },
      'fact-checker': {
        id: 'fact-checker',
        name: 'Fact Checker',
        tier: 'worker',
        capabilities: ['verify', 'cross-reference', 'validate'],
        status: 'active',
        description: 'Verifies claims and cross-references sources'
      },
      'motion-drafter': {
        id: 'motion-drafter',
        name: 'Motion Drafter',
        tier: 'worker',
        capabilities: ['draft', 'format', 'cite', 'proofread'],
        status: 'active',
        description: 'Drafts legal motions and documents'
      },
      'presentation-prep': {
        id: 'presentation-prep',
        name: 'Presentation Specialist',
        tier: 'worker',
        capabilities: ['slide-deck', 'visuals', 'narrative', 'export'],
        status: 'active',
        description: 'Prepares presentations and visual materials'
      },
      // Specialist Layer
      'source-analyzer': {
        id: 'source-analyzer',
        name: 'Source Analyzer',
        tier: 'specialist',
        capabilities: ['credibility', 'bias-detection', 'extraction'],
        status: 'active',
        description: 'Analyzes source credibility and extracts key info'
      },
      'deadline-tracker': {
        id: 'deadline-tracker',
        name: 'Deadline Tracker',
        tier: 'specialist',
        capabilities: ['track', 'remind', 'prioritize', 'escalate'],
        status: 'active',
        description: 'Tracks deadlines and sends reminders'
      }
    };

    Object.values(agents).forEach(a => this.agents.set(a.id, a));
  }

  initRails() {
    // Guardrails for agent actions
    this.rails.set('no-secrets', {
      name: 'No Secrets in Output',
      validate: (output) => !/(?:key|token|secret|password|api)[_-]?key\s*[:=]\s*['"]?[A-Za-z0-9_-]{20,}/i.test(output)
    });

    this.rails.set('max-tokens', {
      name: 'Max Token Limit',
      validate: (output) => output.length < 100000
    });

    this.rails.set('no-harmful', {
      name: 'No Harmful Content',
      validate: (output) => !/(?:hack|exploit|attack|malware|ransomware)/i.test(output)
    });

    this.rails.set('legal-accuracy', {
      name: 'Legal Citation Required',
      validate: (output, context) => {
        if (context?.type !== 'legal') return true;
        return /\d+\s+(?:U\.S\.|F\. supp\.|F\.3d|F\.2d)/.test(output) || output.length < 500;
      }
    });
  }

  // Route a task to the appropriate agent
  route(task) {
    const { type, priority, complexity } = task;

    // Executive routing
    if (complexity === 'high' || priority === 'critical') {
      return this.agents.get('executive');
    }

    // Type-based routing
    const routes = {
      'research': 'research-manager',
      'legal': 'legal-manager',
      'ops': 'ops-manager',
      'presentation': 'presentation-prep',
      'fact-check': 'fact-checker',
      'draft': 'motion-drafter',
      'deadline': 'deadline-tracker'
    };

    const agentId = routes[type] || 'executive';
    return this.agents.get(agentId);
  }

  // Execute a task with rails
  async execute(task, input) {
    const agent = this.route(task);
    if (!agent) return { error: 'No agent available' };

    // Apply rails
    for (const [railName, rail] of this.rails) {
      if (!rail.validate(input, task)) {
        return { error: `Rail ${railName} blocked execution`, agent: agent.id };
      }
    }

    // Log task
    const taskId = Date.now().toString(36);
    this.tasks.set(taskId, {
      id: taskId,
      task,
      agent: agent.id,
      status: 'executing',
      startedAt: new Date().toISOString()
    });

    return {
      taskId,
      agent: agent.id,
      status: 'dispatched',
      message: `Task dispatched to ${agent.name}`
    };
  }

  // Get all agents
  getAgents() {
    return Array.from(this.agents.values());
  }

  // Get agents by tier
  getAgentsByTier(tier) {
    return Array.from(this.agents.values()).filter(a => a.tier === tier);
  }

  // Get task status
  getTask(taskId) {
    return this.tasks.get(taskId);
  }

  // Get all active tasks
  getActiveTasks() {
    return Array.from(this.tasks.values()).filter(t => t.status === 'executing');
  }

  // Get swarm status
  getSwarmStatus() {
    const agents = this.getAgents();
    return {
      total: agents.length,
      active: agents.filter(a => a.status === 'active').length,
      tiers: {
        executive: this.getAgentsByTier('executive').length,
        manager: this.getAgentsByTier('manager').length,
        worker: this.getAgentsByTier('worker').length,
        specialist: this.getAgentsByTier('specialist').length
      },
      activeTasks: this.getActiveTasks().length,
      rails: Array.from(this.rails.keys())
    };
  }
}

module.exports = Gatekeeper;
