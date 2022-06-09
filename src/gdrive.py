from __future__ import print_function

import os.path
from rich.console import Console

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ~ import directly when called from within src otherwise call from src
try:
    import main
except:
    from src import main


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/docs",
]

global service
service = None
console = Console()


def validate() -> build:
    """Validate credentials and enable OAuth authentication

    Returns:
        build: drive service containing rest API methods
    """

    global service
    creds = None

    # ~ The file token.json stores the user's access and refresh tokens, and is created
    # ~ automatically when the authorization flow completes for the first time.
    if os.path.exists("authentication/token.json"):
        creds = Credentials.from_authorized_user_file(
            "authentication/token.json", SCOPES
        )

    # ~ If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "authentication/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # ~ Save the credentials for the next run
        with open("authentication/token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # ~ create and return drive service containing rest API methods
        service = build("drive", "v3", credentials=creds)
        console.print("validated login", style="green")

        # ~ Return service for test
        return service

    except HttpError as e:
        # ~ when in developerMode print googleapiclient error else print standard error message
        if main.developerMode:
            console.print(f"Error authenticating drive → {e}", style="red")
        else:
            console.print(f"Error authenticating drive", style="red")

        # ~ Return none to fail test
        return None


def ls(root):
    page_token = None
    files = []
    while True:

        response = (
            service.files()
            .list(
                q=f"parents = '{root}'",
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
            )
            .execute()
        )
        for file in response.get("files", []):
            files.append(file)

        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break
    return files
