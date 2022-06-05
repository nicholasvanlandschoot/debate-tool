from __future__ import print_function

import os.path
import sys
from rich.console import Console
import main

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/docs']

global service 
service = None
console = Console()


def validate():
    '''Validate credentials and enable OAuth authentication
    '''
    global service

    creds = None
   
    #~ The file token.json stores the user's access and refresh tokens, and is created 
    #~ automatically when the authorization flow completes for the first time.
    if os.path.exists('authentication/token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    #~ If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'authentication/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('authentication/credentials.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
        console.print('validated login', style='green')
        return service

    except HttpError as e:
        if main.developerMode: console.print(f'Error authenticating drive → {e}', style='red')
        else: console.print(f'Error authenticating drive', style='red')
