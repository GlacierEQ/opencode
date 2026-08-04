/**
 * COLOSSUS GATEWAY - Unified Entry Point
 * 
 * Combines Keymaster (key management) + Gatekeeper (agent orchestration)
 * Single server, single port, unified API
 */

const express = require('express');
const cors = require('cors');
const { WebSocketServer } = require('ws');
const http = require('http');
const path = require('path');

const Keymaster = require('./keymaster');
const Gatekeeper = require('./gatekeeper');

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server, path: '/ws' });

// Initialize services
const keymaster = new Keymaster();
const gatekeeper = new Gatekeeper();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ==================== KEYMASTER ROUTES ====================

// Get all keys (masked)
app.get('/api/keys', async (req, res) => {
  const keys = await keymaster.getAllKeys();
  res.json({ keys, count: keys.length });
});

// Get key for a service
app.get('/api/keys/:service', async (req, res) => {
  const key = await keymaster.getKey(req.params.service);
  if (!key) return res.status(404).json({ error: 'Key not found' });
  res.json({ service: req.params.service, key: '••••••••' + key.slice(-4) });
});

// Set/update a key
app.post('/api/keys', async (req, res) => {
  const { service, keyName, keyValue, category } = req.body;
  if (!service || !keyName || !keyValue) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  const success = await keymaster.setKey(service, keyName, keyValue, category);
  res.json({ success, service });
});

// Rotate a key
app.post('/api/keys/:service/rotate', async (req, res) => {
  const { newKey } = req.body;
  if (!newKey) return res.status(400).json({ error: 'Missing newKey' });
  const result = await keymaster.rotateKey(req.params.service, newKey);
  res.json(result);
});

// Health check for a service
app.get('/api/health/:service', async (req, res) => {
  const health = await keymaster.checkHealth(req.params.service);
  res.json(health);
});

// Health check all services
app.get('/api/health', async (req, res) => {
  const health = await keymaster.checkAllHealth();
  res.json(health);
});

// ==================== GATEKEEPER ROUTES ====================

// Get all agents
app.get('/api/agents', (req, res) => {
  const agents = gatekeeper.getAgents();
  res.json({ agents, count: agents.length });
});

// Get agents by tier
app.get('/api/agents/tier/:tier', (req, res) => {
  const agents = gatekeeper.getAgentsByTier(req.params.tier);
  res.json({ agents, tier: req.params.tier });
});

// Get swarm status
app.get('/api/swarm/status', (req, res) => {
  const status = gatekeeper.getSwarmStatus();
  res.json(status);
});

// Execute a task
app.post('/api/swarm/execute', async (req, res) => {
  const { task, input } = req.body;
  if (!task) return res.status(400).json({ error: 'Missing task' });
  const result = await gatekeeper.execute(task, input);
  res.json(result);
});

// Get task status
app.get('/api/swarm/task/:id', (req, res) => {
  const task = gatekeeper.getTask(req.params.id);
  if (!task) return res.status(404).json({ error: 'Task not found' });
  res.json(task);
});

// Get active tasks
app.get('/api/swarm/tasks', (req, res) => {
  const tasks = gatekeeper.getActiveTasks();
  res.json({ tasks, count: tasks.length });
});

// ==================== UNIFIED ROUTES ====================

// System status
app.get('/api/status', async (req, res) => {
  const [health, swarm] = await Promise.all([
    keymaster.checkAllHealth(),
    Promise.resolve(gatekeeper.getSwarmStatus())
  ]);
  res.json({
    gateway: 'Colossus Gateway',
    version: '1.0.0',
    uptime: process.uptime(),
    keymaster: { services: Object.keys(health).length, healthy: Object.values(health).filter(h => h.healthy).length },
    gatekeeper: swarm,
    timestamp: new Date().toISOString()
  });
});

// ==================== WEBSOCKET ====================

wss.on('connection', (ws) => {
  console.log('Client connected to Colossus Gateway');
  
  ws.send(JSON.stringify({
    type: 'welcome',
    message: 'Connected to Colossus Gateway',
    services: ['keymaster', 'gatekeeper']
  }));

  ws.on('message', async (data) => {
    try {
      const msg = JSON.parse(data);
      
      switch (msg.type) {
        case 'health':
          const health = await keymaster.checkAllHealth();
          ws.send(JSON.stringify({ type: 'health', data: health }));
          break;
        case 'status':
          const status = gatekeeper.getSwarmStatus();
          ws.send(JSON.stringify({ type: 'status', data: status }));
          break;
        case 'execute':
          const result = await gatekeeper.execute(msg.task, msg.input);
          ws.send(JSON.stringify({ type: 'result', data: result }));
          break;
      }
    } catch (e) {
      ws.send(JSON.stringify({ type: 'error', message: e.message }));
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// ==================== START ====================

const PORT = process.env.PORT || 3002;

server.listen(PORT, () => {
  console.log(`
╔══════════════════════════════════════════════════╗
║           COLOSSUS GATEWAY v1.0.0                ║
║                                                  ║
║  Keymaster: Unified key management               ║
║  Gatekeeper: Agent swarm orchestration           ║
║                                                  ║
║  HTTP:  http://localhost:${PORT}                   ║
║  WS:    ws://localhost:${PORT}/ws                  ║
╚══════════════════════════════════════════════════╝
  `);
});

module.exports = { app, server, keymaster, gatekeeper };
