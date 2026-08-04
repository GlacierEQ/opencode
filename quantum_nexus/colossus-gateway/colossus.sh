#!/bin/bash
# Colossus Gateway - Start/Stop/Daemon manager
# Usage: ./colossus.sh [start|stop|restart|status|auth|logs]

ACTION=${1:-"status"}
DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$DIR/.colossus.pid"
LOG_FILE="$DIR/logs/colossus.log"
PORT=3002

mkdir -p "$DIR/logs"

start() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "Colossus already running (PID: $(cat "$PID_FILE"))"
        return
    fi
    
    echo "Starting Colossus Gateway..."
    
    if [ "$1" = "background" ]; then
        nohup node "$DIR/server.js" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        echo "✓ Started in background (PID: $!)"
        echo "  Dashboard: http://localhost:$PORT"
        echo "  Logs: tail -f $LOG_FILE"
    else
        echo "Starting in foreground (Ctrl+C to stop)..."
        node "$DIR/server.js"
    fi
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            rm -f "$PID_FILE"
            echo "✓ Stopped (PID: $PID)"
        else
            rm -f "$PID_FILE"
            echo "Process not running, cleaned up PID file"
        fi
    else
        echo "Not running"
    fi
}

status() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "✓ Running (PID: $(cat "$PID_FILE"))"
        echo "  Dashboard: http://localhost:$PORT"
        echo "  Logs: tail -f $LOG_FILE"
    else
        echo "✗ Not running"
    fi
}

logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo "No logs found"
    fi
}

auth() {
    echo "Opening browser for OAuth..."
    echo "Use this for: Google, GitHub, Dropbox, OneDrive"
    echo ""
    
    # Start auth helper
    node -e "
        const http = require('http');
        const { exec } = require('child_process');
        const url = require('url');
        
        const server = http.createServer((req, res) => {
            const query = url.parse(req.url, true).query;
            
            if (query.code) {
                console.log('Authorization code received!');
                console.log('Code:', query.code.substring(0, 20) + '...');
                
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end('<h1>✓ Authorized!</h1><p>You can close this tab.</p>');
                
                // Save to .env
                const fs = require('fs');
                const envFile = fs.readFileSync('.env', 'utf8');
                const provider = query.state || 'unknown';
                fs.writeFileSync('.env', envFile + '\n' + provider.toUpperCase() + '_AUTH_CODE=' + query.code);
                
                console.log('Saved to .env');
                server.close();
                process.exit(0);
            } else {
                res.writeHead(400);
                res.end('Waiting for auth...');
            }
        });
        
        server.listen(8080, () => {
            console.log('Auth callback listening on http://localhost:8080');
            console.log('Paste this redirect URI in your OAuth setup:');
            console.log('http://localhost:8080');
        });
    "
}

case $ACTION in
    start)
        start foreground
        ;;
    start-bg|daemon)
        start background
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        start background
        ;;
    status)
        status
        ;;
    auth)
        auth
        ;;
    logs)
        logs
        ;;
    *)
        echo "Colossus Gateway Manager"
        echo ""
        echo "Usage: $0 {start|start-bg|stop|restart|status|auth|logs}"
        echo ""
        echo "  start     - Run in foreground (Ctrl+C to stop)"
        echo "  start-bg  - Run in background (daemon mode)"
        echo "  stop      - Stop background process"
        echo "  restart   - Restart background process"
        echo "  status    - Check if running"
        echo "  auth      - Start OAuth callback server"
        echo "  logs      - Tail logs"
        ;;
esac
