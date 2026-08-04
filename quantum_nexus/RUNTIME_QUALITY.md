# RUNTIME QUALITY GUIDE
## Maximizing OpenCode Performance

### Quick Commands
```bash
# Run optimizer
/root/quantum_nexus/optimize.sh

# Check status
opencode --version && opencode mcp list

# Clear caches
npm cache clean --force && pip cache purge

# Check disk
df -h / | tail -1

# Check memory
free -h | head -2
```

### Performance Tips

#### 1. Memory Management
- **Current:** 3.6GB used / 5.4GB total
- **Tip:** Close unused apps to free RAM
- **Command:** `free -h` to check

#### 2. Disk Space
- **Current:** 2.4GB free (98% used)
- **Tip:** Regular cleanup of temp files
- **Command:** `/root/quantum_nexus/optimize.sh`

#### 3. MCP Servers
- **Desktop Commander:** ✓ Connected
- **Tip:** Only load needed MCP servers
- **Command:** `opencode mcp list`

#### 4. API Connections
- **GitHub:** ✓ Working
- **CourtListener:** ✓ Working
- **Tip:** Use environment variables for keys
- **Command:** `source /root/.vault_env`

#### 5. OpenCode Config
- **Location:** `/root/.config/opencode/opencode.jsonc`
- **Tip:** Keep references minimal
- **Current:** tower, quantum_nexus, buckets

### System Requirements
| Component | Status | Notes |
|-----------|--------|-------|
| OpenCode | v1.18.11 ✓ | Latest |
| Desktop Commander | ✓ | Connected |
| Python | 3.14.4 ✓ | Latest |
| Node | v26.4.0 ✓ | Latest |
| Git | 2.53.0 ✓ | Latest |

### Optimization Schedule
- **Daily:** Run `/root/quantum_nexus/optimize.sh`
- **Weekly:** Check disk space, clear caches
- **Monthly:** Update packages, review config

### Troubleshooting
1. **Slow response:** Clear caches, check memory
2. **MCP not connecting:** Restart opencode
3. **API errors:** Check vault, verify keys
4. **Disk full:** Run optimizer, delete temp files
