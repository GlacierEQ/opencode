# CLOUD BUCKET
## Cloud Storage Status

### Active
| Provider | Status | Token | Expires |
|----------|--------|-------|---------|
| Cloudflare R2 | ✓ Active | cfat_... | 2027 |

### Expired (Needs Reauth)
| Provider | Status | Issue |
|----------|--------|-------|
| Dropbox (glacier) | ✗ Expired | Browser reauth |
| Dropbox (kahala) | ✗ Expired | Browser reauth |
| OneDrive | ✗ Expired | Browser reauth |
| Google Drive | ✗ Invalid | Key truncated |

### Cloudflare R2 Config
```ini
[cloudflare-r2]
type = s3
provider = Cloudflare
access_key_id = [REDACTED - see .vault_env]
secret_access_key = [REDACTED - see .vault_env]
endpoint = https://<account-id>.r2.cloudflarestorage.com
region = auto
```

### Reconnection Commands
```bash
# OneDrive
rclone config reconnect onedrive:

# Dropbox
rclone config

# R2 Test
rclone lsd cloudflare-r2:
```

### Fallback Strategy
1. **Primary:** Cloudflare R2 (active)
2. **Secondary:** Reconnect OneDrive
3. **Tertiary:** Reconnect Dropbox
4. **Emergency:** Local storage only
