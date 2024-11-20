from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
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
  return items

def upload_file(creds, file_path, folder_id=None):
  service = build('drive', 'v3', credentials=creds)
  file_metadata = {'name': os.path.basename(file_path)}
  if folder_id:
    file_metadata['parents'] = [folder_id]
  media = MediaFileUpload(file_path, resumable=True)
  file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
  print(f"File ID: {file.get('id')}")

def download_file(creds, file_id, destination):
  service = build('drive', 'v3', credentials=creds)
  request = service.files().get_media(fileId=file_id)
  with open(destination, 'wb') as fh:
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
      print(f"Download {int(status.progress() * 100)}%")

def delete_file(creds, file_id):
  service = build('drive', 'v3', credentials=creds)
  service.files().delete(fileId=file_id).execute()
  print(f"File {file_id} deleted.")

def main():
  # Authenticate and get credentials
  creds = authenticate()
  if not creds or not creds.valid:
    print("Failed to authenticate.")
    return

  # List files
  print("Listing files:")
  list_files(creds)

  # Upload a file
  file_path = 'test.txt'
  print(f"Uploading file: {file_path}")
  upload_file(creds, file_path)

  # List files again to see the uploaded file
  print("Listing files after upload:")
  items = list_files(creds)

  # Find the uploaded file ID
  file_id = None
  for item in items:
    if item['name'] == os.path.basename(file_path):
      file_id = item['id']
      break

  if file_id:
    # Download the file
    print(f"Downloading file with ID: {file_id}")
    download_file(creds, file_id, 'download_test.txt')

    # Delete the file
    print(f"Deleting file with ID: {file_id}")
    delete_file(creds, file_id)
  else:
    print("Uploaded file not found.")

if __name__ == "__main__":
  main()