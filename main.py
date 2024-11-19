from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
  creds = None
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
      token.write(creds.to_json())
    return creds

def list_files(creds):
  service = build('drive', 'v3', credentials=creds)
  results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name, mimeType, modifiedTime)").execute()
  items = results.get('files', [])
  if not items:
    print('No files found.')
  else:
    print('Files:')
    for item in items:
      print(f"{item['name']} ({item['id']}) - {item['mimeType']} - {item['modifiedTime']}")