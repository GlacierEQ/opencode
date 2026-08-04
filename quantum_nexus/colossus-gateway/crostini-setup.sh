#!/bin/bash
# Crostini Setup Script for Pixel Tab
# Handles ChromeOS 130+ Crostini integration

set -e

echo "╔══════════════════════════════════════════════════╗"
echo "║  Crostini Setup - Pixel Tab                     ║"
echo "║  ChromeOS 130+ Optimized                        ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# System info
echo "=== System Info ==="
echo "Kernel: $(uname -r)"
echo "User: $(whoami)"
echo "Home: $HOME"
echo ""

# Update system
echo "=== Updating System ==="
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo ""
echo "=== Installing Dependencies ==="
sudo apt install -y \
  curl git build-essential \
  xdg-utils \
  nodejs npm \
  python3 python3-pip \
  jq htop tmux

# Install Node 22
echo ""
echo "=== Installing Node.js 22 ==="
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -
sudo apt install -y nodejs

echo "Node: $(node --version)"
echo "Npm: $(npm --version)"

# Install Go (for various tools)
echo ""
echo "=== Installing Go ==="
GO_VERSION="1.23.4"
curl -fsSL "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz" | sudo tar -C /usr/local -xzf -
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin

# Install Rust
echo ""
echo "=== Installing Rust ==="
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source ~/.cargo/env

# Chrome integration
echo ""
echo "=== Configuring Chrome Integration ==="
sudo apt install -y xdg-utils
xdg-settings set default-web-browser google-chrome.desktop 2>/dev/null || true

# Create browser helper
mkdir -p ~/bin
cat > ~/bin/open-browser << 'BROWSEREOF'
#!/bin/bash
# Open URL in ChromeOS Chrome from Crostini
if [ -z "$1" ]; then
    echo "Usage: open-browser <url>"
    exit 1
fi

# Try xdg-open first (works on ChromeOS 130+)
xdg-open "$1" 2>/dev/null && exit 0

# Fallback: write to shared file
echo "$1" >> /tmp/browser-urls.txt
echo "URL queued. Open Chrome and check /tmp/browser-urls.txt"
BROWSEREOF
chmod +x ~/bin/open-browser

# Optimize for ChromeOS
echo ""
echo "=== Optimizing for ChromeOS ==="

# Memory optimization
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Disable unneeded services
sudo systemctl disable bluetooth 2>/dev/null || true
sudo systemctl disable avahi-daemon 2>/dev/null || true
sudo systemctl disable cups 2>/dev/null || true

# Install Colossus Gateway
echo ""
echo "=== Installing Colossus Gateway ==="
REPO_DIR="$HOME/opencode"

if [ -d "$REPO_DIR" ]; then
    echo "Updating existing repo..."
    cd "$REPO_DIR" && git pull
else
    git clone https://github.com/GlacierEQ/opencode.git "$REPO_DIR"
fi

cd "$REPO_DIR/quantum_nexus/colossus-gateway"
npm install

# Create .env if missing
if [ ! -f .env ]; then
    cat > .env << 'ENVEOF'
# Colossus Gateway Environment
PORT=3002
HOST=0.0.0.0

# Supabase
SUPABASE_URL=https://kjebemdgvjvuutzvhbtp.supabase.co
SUPABASE_ANON_KEY=your_key_here
SUPABASE_SERVICE_ROLE=your_key_here

# Add other keys as needed
ENVEOF
    echo "Created .env — add your keys!"
fi

# Create systemd service
echo ""
echo "=== Setting up Systemd Service ==="
sudo tee /etc/systemd/system/colossus.service << SERVICEEOF
[Unit]
Description=Colossus Gateway
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=$(which node) server.js
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
SERVICEEOF

sudo systemctl daemon-reload
sudo systemctl enable colossus
echo "Service installed. Start with: sudo systemctl start colossus"

# Add aliases
echo ""
echo "=== Adding Aliases ==="
cat >> ~/.bashrc << 'ALIASES'

# Colossus aliases
alias colossus-start='sudo systemctl start colossus'
alias colossus-stop='sudo systemctl stop colossus'
alias colossus-restart='sudo systemctl restart colossus'
alias colossus-status='sudo systemctl status colossus'
alias colossus-logs='journalctl -u colossus -f'
alias colossus-dev='cd ~/opencode/quantum_nexus/colossus-gateway && ./colossus.sh start'

# Quick nav
alias cdcolossus='cd ~/opencode/quantum_nexus/colossus-gateway'
alias cdquantum='cd ~/opencode/quantum_nexus'

# Tools
alias ports='netstat -tlnp'
alias myip='curl -s ifconfig.me'
alias localip='hostname -I | awk "{print \$1}"'
ALIASES

source ~/.bashrc 2>/dev/null || true

# Summary
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  ✓ Setup Complete!                               ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║                                                  ║"
echo "║  Start Colossus:                                 ║"
echo "║    sudo systemctl start colossus                 ║"
echo "║                                                  ║"
echo "║  Dashboard:                                      ║"
echo "║    http://localhost:3002                          ║"
echo "║                                                  ║"
echo "║  From Note9 (find Pixel Tab IP):                 ║"
echo "║    http://$(hostname -I | awk '{print $1}'):3002    ║"
echo "║                                                  ║"
echo "║  Browser auth:                                   ║"
echo "║    xdg-open http://localhost:3002/auth/google     ║"
echo "║                                                  ║"
echo "║  View logs:                                      ║"
echo "║    colossus-logs                                 ║"
echo "║                                                  ║"
╚══════════════════════════════════════════════════╝
echo ""
echo "Reboot recommended for all changes to take effect."
