#!/bin/bash
# Colossus Gateway - Secrets Sync Script
# Syncs between .env file and Supabase vault

set -e

ACTION=${1:-"status"}

case $ACTION in
  push)
    echo "Pushing .env to Supabase vault..."
    node -e "
      require('dotenv').config();
      const Keymaster = require('./keymaster');
      const km = new Keymaster();
      
      const envVars = Object.entries(process.env)
        .filter(([k]) => k.includes('KEY') || k.includes('TOKEN') || k.includes('SECRET') || k.includes('PASSWORD'))
        .filter(([k]) => !k.startsWith('npm_') && !k.startsWith('NODE_'));
      
      (async () => {
        for (const [key, value] of envVars) {
          await km.setKey(key, key, value, 'env-sync');
          console.log('Pushed:', key);
        }
        console.log('Done:', envVars.length, 'keys pushed');
      })();
    "
    ;;
    
  pull)
    echo "Pulling Supabase vault to .env..."
    node -e "
      const Keymaster = require('./keymaster');
      const km = new Keymaster();
      const fs = require('fs');
      
      (async () => {
        const keys = await km.getAllKeys();
        const envLines = keys.map(k => k.service + '=' + k.key_value);
        fs.writeFileSync('.env.generated', envLines.join('\n'));
        console.log('Written to .env.generated:', keys.length, 'keys');
      })();
    "
    ;;
    
  status)
    echo "=== Colossus Secrets Status ==="
    echo ""
    echo "Local .env:"
    if [ -f .env ]; then
      grep -c "." .env | xargs -I {} echo "  {} lines"
    else
      echo "  Not found"
    fi
    echo ""
    echo "Supabase vault:"
    node -e "
      const Keymaster = require('./keymaster');
      const km = new Keymaster();
      (async () => {
        const keys = await km.getAllKeys();
        console.log('  Keys:', keys.length);
        keys.forEach(k => console.log('   -', k.service, '(' + k.category + ')'));
      })();
    "
    ;;
    
  health)
    echo "=== Service Health ==="
    node -e "
      const Keymaster = require('./keymaster');
      const km = new Keymaster();
      (async () => {
        const health = await km.checkAllHealth();
        for (const [service, info] of Object.entries(health)) {
          const status = info.healthy ? '✓' : '✗';
          console.log('  ' + status, service, info.status);
        }
      })();
    "
    ;;
    
  *)
    echo "Usage: $0 {push|pull|status|health}"
    echo ""
    echo "  push   - Push .env keys to Supabase vault"
    echo "  pull   - Pull Supabase vault to .env.generated"
    echo "  status - Show secrets status"
    echo "  health - Check service health"
    ;;
esac
