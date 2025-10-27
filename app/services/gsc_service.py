import reflex as rx
import os
import logging
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
REDIRECT_URI = "http://localhost:3000/oauth/callback"


def get_gsc_auth_url() -> str | None:
    """Generates the Google OAuth URL for GSC.

    The user will be redirected to this URL to authenticate and grant permissions.
    Returns None if the client_secret.json is not configured.
    """
    if not os.path.exists(CLIENT_SECRETS_FILE):
        logging.error(
            f"{CLIENT_SECRETS_FILE} not found. GSC integration is not configured."
        )
        return None
    try:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
        )
        auth_url, _ = flow.authorization_url(prompt="consent")
        return auth_url
    except Exception as e:
        logging.exception(f"Error generating GSC auth URL: {e}")
        return None


def get_gsc_credentials(authorization_code: str):
    """Fetches the GSC credentials using the authorization code from the callback."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(code=authorization_code)
    return flow.credentials


def list_gsc_sites(credentials):
    """Lists the sites (properties) the user has access to in GSC."""
    service = build("searchconsole", "v1", credentials=credentials)
    site_list = service.sites().list().execute()
    return site_list.get("siteEntry", [])