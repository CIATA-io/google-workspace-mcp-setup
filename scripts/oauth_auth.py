#!/usr/bin/env python3
"""
Standalone OAuth authorization for google_workspace_mcp.

Saves tokens to ~/.google_workspace_mcp/credentials/{email}.json
in the exact format the MCP server expects.

Usage:
    OAUTHLIB_INSECURE_TRANSPORT=1 uv run --with google-auth-oauthlib scripts/oauth_auth.py

Uses port 9090 (not 8000) to avoid conflicts with the MCP server.
"""

import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/presentations.readonly",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/tasks.readonly",
    "https://www.googleapis.com/auth/contacts",
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/chat.spaces",
    "https://www.googleapis.com/auth/chat.spaces.readonly",
    "https://www.googleapis.com/auth/chat.messages",
    "https://www.googleapis.com/auth/chat.messages.readonly",
    "https://www.googleapis.com/auth/cse",
    "https://www.googleapis.com/auth/script.projects",
    "https://www.googleapis.com/auth/script.projects.readonly",
    "https://www.googleapis.com/auth/script.deployments",
    "https://www.googleapis.com/auth/script.deployments.readonly",
    "https://www.googleapis.com/auth/script.processes",
    "https://www.googleapis.com/auth/script.metrics",
]

CLIENT_SECRET = os.path.expanduser("~/.google_workspace_mcp/client_secret.json")
CREDS_DIR = os.path.expanduser("~/.google_workspace_mcp/credentials")


def main():
    if not os.path.exists(CLIENT_SECRET):
        print(f"❌ Client secret not found at: {CLIENT_SECRET}")
        print("   Download it from Google Cloud Console and place it there.")
        return

    os.makedirs(CREDS_DIR, exist_ok=True)

    print("🔐 Starting OAuth flow... Browser should open.")
    print(f"   Using client secret: {CLIENT_SECRET}")
    print(f"   Using port 9090 for callback (avoids MCP server port 8000 conflict)\n")

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, scopes=SCOPES)
    creds = flow.run_local_server(
        port=9090, open_browser=True, prompt="consent", access_type="offline"
    )

    email = input("\nEnter your Google email (e.g. user@gmail.com): ").strip()
    if not email or "@" not in email:
        print("❌ Invalid email address.")
        return

    # IMPORTANT: filename must be {email}.json — the library's
    # LocalDirectoryCredentialStore._get_credential_path() constructs
    # the path as f"{user_email}.json"
    token_file = os.path.join(CREDS_DIR, f"{email}.json")

    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes) if creds.scopes else SCOPES,
    }

    with open(token_file, "w") as f:
        json.dump(token_data, f, indent=2)

    print(f"\n✅ Authorization successful!")
    print(f"   Tokens saved to: {token_file}")
    print(f"   You can now start Antigravity.")


if __name__ == "__main__":
    main()
