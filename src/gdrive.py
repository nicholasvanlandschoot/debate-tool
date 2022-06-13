from __future__ import print_function
import json

import os.path
from rich.console import Console

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ~ import directly when called from within src otherwise call from src
try:
    import main, storage
except:
    from src import main, storage


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/docs",
]

global service
global docs_service
console = Console()


def validate_docs() -> build:
    global docs_service
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds_docs = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("authentication/token.json"):
        creds_docs = Credentials.from_authorized_user_file(
            "authentication/token.json", SCOPES
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds_docs or not creds_docs.valid:
        if creds_docs and creds_docs.expired and creds_docs.refresh_token:
            creds_docs.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "authentication/credentials.json", SCOPES
            )
            creds_docs = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("authentication/token.json", "w") as token:
            token.write(creds_docs.to_json())

    try:
        docs_service = build("docs", "v1", credentials=creds_docs)
    except HttpError as err:
        print(err)


def validate() -> build:
    """Validate credentials and enable OAuth authentication

    Returns:
        build: drive service containing rest API methods
    """
    global service
    global docs_service
    service = None
    creds = None

    validate_docs()

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
        docs_service = build("docs", "v1", credentials=creds)
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


def create(_name, _parent, _path, _type):
    requestBody = {
        "name": _name,
        "mimeType": _type,
        "parents": [_parent],
    }
    obj = service.files().create(body=requestBody).execute()

    storage.DriveObject(name=_name, id=obj.get("id"), path=_path)


def deleteFile(_id):
    storage.objects["id"][_id]._forget()
    service.files().delete(fileId=_id).execute()


def ls(root) -> list:
    """Get all direct children of a drive object"""
    page_token = None
    files = []

    while True:

        # ~ Query google drive API for all direct children of current root
        response = (
            service.files()
            .list(
                q=f"trashed=false and parents = '{root}'",
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token,
            )
            .execute()
        )

        # ~ add all children to return array
        for file in response.get("files", []):
            files.append(file)

        # ~ keep going if there are more pages with children
        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break

    return files


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

    Args:
        element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get("textRun")
    if not text_run:
        return ""
    return text_run.get("content")


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
    in nested elements.

    Args:
        elements: a list of Structural Elements.
    """
    text = ""
    for value in elements:
        if "paragraph" in value:
            elements = value.get("paragraph").get("elements")
            for elem in elements:
                text += read_paragraph_element(elem)
        elif "table" in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get("table")
            for row in table.get("tableRows"):
                cells = row.get("tableCells")
                for cell in cells:
                    text += read_structural_elements(cell.get("content"))
        elif "tableOfContents" in value:
            # The text in the TOC is also in a Structural Element
            toc = value.get("tableOfContents")
            text += read_structural_elements(toc.get("content"))
    return text


def fetch_file(_id, _name, _snipName = None):
    global docs_service
    doc_content = (
        service.files()
        .export(
            fileId=_id,
            mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        .execute()
    )
    with open(f"{storage.relpath}/userdata/snippets/{_name}.docx", "wb") as f:
        f.write(doc_content)
    
    if _snipName == None:
        _snipName = _name
    osSnipName = _snipName.replace(":","/")

    with open(f"{storage.relpath}/userdata/snippets.json", "r") as f:
        jsonObj = json.load(f)
    
    jsonObj.update({_snipName:f'{storage.relpath}/userdata/snippets/{osSnipName}.docx'})
    jsonObj = json.dumps(jsonObj)
    with open(f"{storage.relpath}/userdata/snippets.json", "w") as f:
        f.write(jsonObj)