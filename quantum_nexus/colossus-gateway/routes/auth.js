/**
 * OAuth Browser Auth Routes
 * Handles browser-based sign-in for Google, GitHub, Dropbox, OneDrive
 */

const express = require('express');
const { exec } = require('child_process');
const router = express.Router();

// OAuth configurations
const OAUTH_CONFIGS = {
  google: {
    authUrl: 'https://accounts.google.com/o/oauth2/auth',
    scope: 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file',
    clientId: process.env.GOOGLE_CLIENT_ID,
    redirectUri: 'http://localhost:3002/auth/callback/google'
  },
  github: {
    authUrl: 'https://github.com/login/oauth/authorize',
    scope: 'repo read:org workflow',
    clientId: process.env.GITHUB_OAUTH_CLIENT_ID,
    redirectUri: 'http://localhost:3002/auth/callback/github'
  },
  dropbox: {
    authUrl: 'https://www.dropbox.com/oauth2/authorize',
    scope: '',
    clientId: process.env.DROPBOX_APP_KEY,
    redirectUri: 'http://localhost:3002/auth/callback/dropbox'
  },
  onedrive: {
    authUrl: 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    scope: 'files.readwrite offline_access',
    clientId: process.env.ONEDRIVE_CLIENT_ID,
    redirectUri: 'http://localhost:3002/auth/callback/onedrive'
  }
};

// Start OAuth flow
router.get('/auth/:provider', (req, res) => {
  const provider = req.params.provider;
  const config = OAUTH_CONFIGS[provider];
  
  if (!config) {
    return res.status(400).json({ error: 'Unknown provider: ' + provider });
  }

  const params = new URLSearchParams({
    client_id: config.clientId,
    redirect_uri: config.redirectUri,
    response_type: 'code',
    scope: config.scope,
    state: provider
  });

  const authUrl = `${config.authUrl}?${params.toString()}`;
  
  // Try to open browser
  const startBrowser = process.platform === 'darwin' ? 'open' :
                       process.platform === 'win32' ? 'start' :
                       'xdg-open';

  exec(`${startBrowser} "${authUrl}"`, (err) => {
    if (err) {
      // Browser not available, return URL
      res.json({
        provider,
        authUrl,
        message: 'Open this URL in your browser'
      });
    } else {
      res.json({
        provider,
        message: 'Browser opened',
        authUrl
      });
    }
  });
});

// OAuth callback handler
router.get('/auth/callback/:provider', (req, res) => {
  const provider = req.params.provider;
  const code = req.query.code;
  const error = req.query.error;

  if (error) {
    return res.send(`
      <html>
        <body style="font-family: sans-serif; padding: 40px; background: #0a0a0f; color: #e0e0e0;">
          <h1 style="color: #ff4444;">✗ Authorization Failed</h1>
          <p>Error: ${error}</p>
          <p>You can close this tab.</p>
        </body>
      </html>
    `);
  }

  if (!code) {
    return res.status(400).send('No authorization code received');
  }

  // Store the auth code
  const fs = require('fs');
  const envPath = __dirname + '/.env';
  
  let envContent = '';
  if (fs.existsSync(envPath)) {
    envContent = fs.readFileSync(envPath, 'utf8');
  }

  const codeVar = `${provider.toUpperCase()}_AUTH_CODE`;
  
  // Update or add the code
  if (envContent.includes(codeVar + '=')) {
    envContent = envContent.replace(new RegExp(codeVar + '=.*'), codeVar + '=' + code);
  } else {
    envContent += `\n${codeVar}=${code}`;
  }

  fs.writeFileSync(envPath, envContent);

  res.send(`
    <html>
      <body style="font-family: sans-serif; padding: 40px; background: #0a0a0f; color: #e0e0e0;">
        <h1 style="color: #00ff88;">✓ ${provider.charAt(0).toUpperCase() + provider.slice(1)} Authorized!</h1>
        <p>Authorization code saved. You can close this tab.</p>
        <p style="color: #888; font-size: 0.9em;">Code: ${code.substring(0, 20)}...</p>
      </body>
    </html>
  `);
  
  console.log(`[${provider}] Authorization code received and saved`);
});

// Exchange code for token (server-side)
router.post('/auth/token/:provider', async (req, res) => {
  const provider = req.params.provider;
  const fs = require('fs');
  const envPath = __dirname + '/.env';
  
  if (!fs.existsSync(envPath)) {
    return res.status(400).json({ error: 'No .env file' });
  }

  const envContent = fs.readFileSync(envPath, 'utf8');
  const codeMatch = envContent.match(new RegExp(`${provider.toUpperCase()}_AUTH_CODE=(.+)`));
  
  if (!codeMatch) {
    return res.status(400).json({ error: 'No auth code found. Run /auth/' + provider + ' first' });
  }

  const code = codeMatch[1].trim();

  // Token exchange logic per provider
  const tokenEndpoints = {
    google: 'https://oauth2.googleapis.com/token',
    github: 'https://github.com/login/oauth/access_token',
    dropbox: 'https://api.dropbox.com/oauth2/token',
    onedrive: 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
  };

  try {
    const response = await fetch(tokenEndpoints[provider], {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        code,
        client_id: process.env[`${provider.toUpperCase()}_CLIENT_ID`],
        client_secret: process.env[`${provider.toUpperCase()}_CLIENT_SECRET`],
        redirect_uri: `http://localhost:3002/auth/callback/${provider}`,
        grant_type: 'authorization_code'
      })
    });

    const data = await response.json();
    
    if (data.access_token || data.access_token) {
      // Save token
      const tokenVar = `${provider.toUpperCase()}_ACCESS_TOKEN`;
      if (envContent.includes(tokenVar + '=')) {
        envContent.replace(new RegExp(tokenVar + '=.*'), tokenVar + '=' + data.access_token);
      } else {
        envContent += `\n${tokenVar}=${data.access_token}`;
      }
      fs.writeFileSync(envPath, envContent);
      
      res.json({ success: true, provider, tokenReceived: true });
    } else {
      res.json({ success: false, provider, error: data });
    }
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// List auth status
router.get('/auth/status', (req, res) => {
  const fs = require('fs');
  const envPath = __dirname + '/.env';
  
  const providers = ['google', 'github', 'dropbox', 'onedrive'];
  const status = {};

  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    
    providers.forEach(p => {
      const hasToken = envContent.includes(`${p.toUpperCase()}_ACCESS_TOKEN=`);
      const hasCode = envContent.includes(`${p.toUpperCase()}_AUTH_CODE=`);
      status[p] = { authenticated: hasToken, pendingAuth: hasCode };
    });
  } else {
    providers.forEach(p => {
      status[p] = { authenticated: false, pendingAuth: false };
    });
  }

  res.json(status);
});

module.exports = router;
