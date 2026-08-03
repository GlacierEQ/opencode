"""
DROPBOX CLIENT
File Storage & Retrieval for Evidence Management
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    import dropbox
except ImportError:
    import subprocess
    subprocess.check_call(["pip3", "install", "dropbox"])
    import dropbox


class DropboxClient:
    """Client for Dropbox API v2."""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.environ.get("DROPBOX_ACCESS_TOKEN", "")
        self.client = dropbox.Dropbox(self.access_token) if self.access_token else None
    
    def connect(self) -> bool:
        """Test connection and return account info."""
        if not self.client:
            return False
        try:
            account = self.client.users_get_current_account()
            return True
        except Exception:
            return False
    
    def list_folder(self, path: str = "") -> List[Dict[str, Any]]:
        """List files and folders in path."""
        if not self.client:
            return []
        
        entries = []
        try:
            result = self.client.files_list_folder(path)
            for entry in result.entries:
                entry_info = {
                    "name": entry.name,
                    "path": entry.path_lower,
                    "type": "folder" if isinstance(entry, dropbox.files.FolderMetadata) else "file",
                    "size": getattr(entry, "size", None),
                    "modified": getattr(entry, "server_modified", None)
                }
                entries.append(entry_info)
        except dropbox.exceptions.ApiError as e:
            print(f"Dropbox API error: {e}")
        
        return entries
    
    def download_file(self, dropbox_path: str) -> Optional[bytes]:
        """Download file contents."""
        if not self.client:
            return None
        
        try:
            metadata, response = self.client.files_download(dropbox_path)
            return response.content
        except dropbox.exceptions.ApiError as e:
            print(f"Download error: {e}")
            return None
    
    def upload_file(self, local_path: str, dropbox_path: str) -> bool:
        """Upload file to Dropbox."""
        if not self.client:
            return False
        
        try:
            with open(local_path, 'rb') as f:
                self.client.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
            return True
        except Exception as e:
            print(f"Upload error: {e}")
            return False
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search Dropbox for files matching query."""
        if not self.client:
            return []
        
        results = []
        try:
            search_result = self.client.files_search_v2(query)
            for match in search_result.matches:
                metadata = match.metadata.get_metadata()
                results.append({
                    "name": metadata.name,
                    "path": metadata.path_lower,
                    "type": "folder" if isinstance(metadata, dropbox.files.FolderMetadata) else "file"
                })
        except dropbox.exceptions.ApiError as e:
            print(f"Search error: {e}")
        
        return results
    
    def get_shared_link(self, dropbox_path: str) -> Optional[str]:
        """Get or create shared link for file."""
        if not self.client:
            return None
        
        try:
            links = self.client.sharing_list_shared_links(path=dropbox_path)
            if links.links:
                return links.links[0].url
            
            link = self.client.sharing_create_shared_link_with_settings(dropbox_path)
            return link.url
        except dropbox.exceptions.ApiError:
            return None
    
    def get_temporary_link(self, dropbox_path: str) -> Optional[str]:
        """Get temporary download link for file."""
        if not self.client:
            return None
        
        try:
            result = self.client.files_get_temporary_link(dropbox_path)
            return result.link
        except dropbox.exceptions.ApiError:
            return None


# --- Standalone Usage ---
if __name__ == "__main__":
    print("=" * 60)
    print("  DROPBOX CLIENT - Evidence Storage")
    print("=" * 60)
    
    client = DropboxClient()
    
    if client.connect():
        print("\n[OK] Connected to Dropbox")
        
        # List root folder
        entries = client.list_folder()
        print(f"\nRoot folder contents: {len(entries)} items")
        for entry in entries[:10]:
            print(f"  [{entry['type']}] {entry['name']}")
    else:
        print("\n[ERROR] Could not connect to Dropbox")
        print("        Set DROPBOX_ACCESS_TOKEN environment variable")
