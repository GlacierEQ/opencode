"""
MCP SERVER MANAGER
Model Context Protocol Server Orchestration
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class MCPServer:
    """MCP Server configuration."""
    name: str
    command: str
    args: List[str]
    env: Dict[str, str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "command": self.command,
            "args": self.args,
            "env": self.env or {}
        }


class MCPServerManager:
    """Manage Model Context Protocol servers."""
    
    # Default MCP servers for legal research
    DEFAULT_SERVERS = {
        "filesystem": MCPServer(
            name="filesystem",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", str(Path.home()), "/Volumes"]
        ),
        "github": MCPServer(
            name="github",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": ""}
        ),
        "fetch": MCPServer(
            name="fetch",
            command="uvx",
            args=["mcp-server-fetch"]
        ),
        "git": MCPServer(
            name="git",
            command="uvx",
            args=["mcp-server-git"]
        ),
        "sequential-thinking": MCPServer(
            name="sequential-thinking",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-sequential-thinking"]
        )
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path.home() / ".config" / "opencode"
        self.config_file = self.config_dir / "mcp_servers.json"
        self.servers: Dict[str, MCPServer] = dict(self.DEFAULT_SERVERS)
    
    def add_server(self, server: MCPServer) -> None:
        """Add or update an MCP server."""
        self.servers[server.name] = server
    
    def remove_server(self, name: str) -> bool:
        """Remove an MCP server."""
        if name in self.servers:
            del self.servers[name]
            return True
        return False
    
    def save_config(self) -> bool:
        """Save MCP server configuration to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            config = {
                "mcpServers": {
                    name: server.to_dict()
                    for name, server in self.servers.items()
                }
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_config(self) -> bool:
        """Load MCP server configuration from file."""
        if not self.config_file.exists():
            return False
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            for name, server_config in config.get("mcpServers", {}).items():
                self.servers[name] = MCPServer(
                    name=name,
                    command=server_config["command"],
                    args=server_config["args"],
                    env=server_config.get("env")
                )
            
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    
    def list_servers(self) -> List[str]:
        """List all configured server names."""
        return list(self.servers.keys())
    
    def get_server(self, name: str) -> Optional[MCPServer]:
        """Get server configuration by name."""
        return self.servers.get(name)


# --- Standalone Usage ---
if __name__ == "__main__":
    print("=" * 60)
    print("  MCP SERVER MANAGER")
    print("=" * 60)
    
    manager = MCPServerManager()
    
    # List default servers
    print("\nDefault MCP Servers:")
    for name in manager.list_servers():
        server = manager.get_server(name)
        print(f"  - {name}: {server.command} {' '.join(server.args[:2])}...")
    
    # Save config
    if manager.save_config():
        print(f"\n[OK] Config saved to {manager.config_file}")
