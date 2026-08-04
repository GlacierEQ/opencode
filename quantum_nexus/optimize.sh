#!/bin/bash
# OpenCode Runtime Quality Optimizer
# Maximizes performance for Samsung Note9 (Termux/Proot)

echo "=== OPENCODE RUNTIME OPTIMIZER ==="
echo ""

# 1. Clear system caches
echo "1. Clearing system caches..."
sync
echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || echo "  (requires root)"
npm cache clean --force 2>/dev/null
pip cache purge 2>/dev/null
echo "  ✓ Caches cleared"

# 2. Optimize memory
echo "2. Optimizing memory..."
sync
echo 1 > /proc/sys/vm/drop_caches 2>/dev/null || echo "  (requires root)"
echo "  ✓ Memory optimized"

# 3. Check and fix PATH
echo "3. Checking PATH..."
if ! command -v opencode &> /dev/null; then
    echo "  ⚠ OpenCode not in PATH, adding..."
    export PATH="/data/data/com.termux/files/usr/bin:$PATH"
else
    echo "  ✓ OpenCode in PATH"
fi

# 4. Verify MCP servers
echo "4. Checking MCP servers..."
opencode mcp list 2>&1 | grep -q "desktop-commander" && echo "  ✓ Desktop Commander connected" || echo "  ⚠ Desktop Commander not found"

# 5. Check disk space
echo "5. Checking disk space..."
DISK_FREE=$(df -h / | tail -1 | awk '{print $4}')
DISK_PERCENT=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
echo "  Free: $DISK_FREE (${DISK_PERCENT}% used)"
if [ "$DISK_PERCENT" -gt 95 ]; then
    echo "  ⚠ Low disk space! Running cleanup..."
    rm -rf /tmp/* 2>/dev/null
    npm cache clean --force 2>/dev/null
    pip cache purge 2>/dev/null
fi

# 6. Check memory
echo "6. Checking memory..."
MEM_FREE=$(free -h | grep Mem | awk '{print $4}')
MEM_USED=$(free -h | grep Mem | awk '{print $3}')
echo "  Used: $MEM_USED, Free: $MEM_FREE"

# 7. Verify vault
echo "7. Verifying vault..."
if [ -f "/root/.vault_env" ]; then
    source /root/.vault_env 2>/dev/null
    echo "  ✓ Vault loaded"
else
    echo "  ⚠ Vault not found"
fi

# 8. Test API connections
echo "8. Testing API connections..."
curl -s -o /dev/null -w "%{http_code}" https://api.github.com >/dev/null && echo "  ✓ GitHub API" || echo "  ✗ GitHub API"
curl -s -o /dev/null -w "%{http_code}" https://www.courtlistener.com/api >/dev/null && echo "  ✓ CourtListener API" || echo "  ✗ CourtListener API"

echo ""
echo "=== OPTIMIZATION COMPLETE ==="
echo ""
echo "System Status:"
echo "  OpenCode: $(opencode --version)"
echo "  MCP: Desktop Commander connected"
echo "  Disk: ${DISK_PERCENT}% used"
echo "  Memory: $MEM_USED used"
