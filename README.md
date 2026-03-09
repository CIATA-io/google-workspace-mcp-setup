# Google Workspace MCP Setup for Antigravity

Setup guide for running [`google_workspace_mcp`](https://github.com/taylorwilsdon/google_workspace_mcp) as an MCP server in [Antigravity](https://blog.google/technology/google-deepmind/project-mariner-gemini-ai-agent/).

## Why?

Replaces the built-in `tools-for-mcp-server-extension` (proprietary, ~8 services, limited write) with an open-source alternative: **12 services, 83+ tools, MIT licensed**.

| Feature | Old Extension | google_workspace_mcp |
|---------|--------------|---------------------|
| Services | ~8 | 12 (+ Forms, Tasks, Contacts, Search, Apps Script) |
| Tools | ~30 | 83+ |
| Write support | Limited | Full |
| Source | Proprietary | MIT open-source |

## Quick Start

### 1. Install `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create Google Cloud OAuth Credentials

1. [console.cloud.google.com](https://console.cloud.google.com/) → Create/select a project
2. **APIs & Services → Credentials → Create Credentials → OAuth Client ID → Desktop Application**
3. Download `client_secret_*.json`
4. Move it:
```bash
mkdir -p ~/.google_workspace_mcp
mv ~/Downloads/client_secret_*.json ~/.google_workspace_mcp/client_secret.json
```

### 3. Enable Google APIs

> ⚠️ Enable on the **same project** where you created the OAuth credentials.

| API | Enable Link |
|-----|-------------|
| Gmail | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com) |
| Calendar | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com) |
| Drive | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com) |
| Docs | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=docs.googleapis.com) |
| Sheets | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com) |
| Slides | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=slides.googleapis.com) |
| People | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=people.googleapis.com) |
| Tasks | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=tasks.googleapis.com) |
| Chat | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=chat.googleapis.com) |
| Forms | [Enable](https://console.cloud.google.com/flows/enableapi?apiid=forms.googleapis.com) |

Wait 1-2 minutes after enabling for propagation.

### 4. Run OAuth (BEFORE starting Antigravity)

> ⚠️ **Critical:** Do this BEFORE Antigravity is running. The MCP server uses port 8000 for OAuth callbacks, and Antigravity spawns multiple instances that compete for the port. This script uses port 9090 instead.

```bash
OAUTHLIB_INSECURE_TRANSPORT=1 uv run --with google-auth-oauthlib scripts/oauth_auth.py
```

This opens a browser for Google consent. After authorizing, enter your email when prompted. Tokens are saved to `~/.google_workspace_mcp/credentials/{email}.json`.

### 5. Configure Antigravity

Copy the template and fill in your credentials:

```bash
cp config/mcp_config.template.json ~/.gemini/antigravity/mcp_config.json
```

Edit `~/.gemini/antigravity/mcp_config.json` and replace:
- `YOUR_USER` → your macOS username
- `YOUR_CLIENT_ID` → your OAuth Client ID
- `YOUR_CLIENT_SECRET` → your OAuth Client Secret

### 6. Start Antigravity & Test

Open Antigravity, start a new conversation, and ask: *"Search my recent emails"*

## Pitfalls

| Problem | Fix |
|---------|-----|
| `GOOGLE_OAUTH_CLIENT_ID: Not Set` | Must set as explicit env vars in `mcp_config.json`, `client_secret.json` alone isn't enough |
| Port 8000 conflict during OAuth | Run `scripts/oauth_auth.py` BEFORE Antigravity starts (uses port 9090) |
| Token file not found | Must be named `{email}.json`, not `{email}_token.json` |
| API not enabled | Enable APIs on the **same project** that owns the OAuth credentials |
| Tools not registering | Clean restart of Antigravity; start with `core` tier, upgrade to `extended` later |

## Tool Tiers

| Tier | Tools | Best for |
|------|-------|----------|
| `core` | ~52 | Getting started, less overhead |
| `extended` | ~83 | Full functionality |
| `complete` | All | Everything including experimental |

## File Locations

| File | Purpose |
|------|---------|
| `~/.gemini/antigravity/mcp_config.json` | MCP server configuration |
| `~/.google_workspace_mcp/client_secret.json` | Google OAuth credentials |
| `~/.google_workspace_mcp/credentials/{email}.json` | Stored OAuth tokens |
| `~/.local/bin/uvx` | uv package runner |

## License

MIT
