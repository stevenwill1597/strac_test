from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import os.path
import logging

# Define the scope for Google Drive API access
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
  """
  Authenticates the user using OAuth 2.0 and returns the credentials.

  Returns:
    Credentials: The authenticated user's credentials.
  """
  creds = None
  try:
    # Check if token.json exists to use existing credentials
    if os.path.exists('token.json'):
      creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Refresh or obtain new credentials if necessary
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        # Run local server to obtain new credentials
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
      # Save the credentials for future use
      with open('token.json', 'w') as token:
        token.write(creds.to_json())
  except Exception as e:
    logging.error(f"Failed to authenticate: {e}")
  return creds

def list_files(creds):
  """
  Lists files in the user's Google Drive.

  Args:
    creds (Credentials): The authenticated user's credentials.

  Returns:
    list: A list of files in the user's Google Drive.
  """
  try:
    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    # List files with specific fields
    results = service.files().list(
      pageSize=10, fields="nextPageToken, files(id, name, mimeType, modifiedTime)").execute()
    items = results.get('files', [])
    if not items:
      print('No files found.')
    else:
      print('Files:')
      for item in items:
        # Print file details
        print(f"{item['name']} ({item['id']}) - {item['mimeType']} - {item['modifiedTime']}")
    return items
  except HttpError as error:
    logging.error(f"An error occurred: {error}")
    return []

def upload_file(creds, file_path, folder_id=None):
  """
  Uploads a file to the user's Google Drive.

  Args:
    creds (Credentials): The authenticated user's credentials.
    file_path (str): The path to the file to upload.
    folder_id (str, optional): The ID of the folder to upload the file to.
  """
  try:
    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    # Prepare file metadata
    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
      file_metadata['parents'] = [folder_id]
    # Upload the file
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File ID: {file.get('id')}")
  except HttpError as error:
    logging.error(f"An error occurred: {error}")

def download_file(creds, file_id, destination):
  """
  Downloads a file from the user's Google Drive.

  Args:
    creds (Credentials): The authenticated user's credentials.
    file_id (str): The ID of the file to download.
    destination (str): The path to save the downloaded file.
  """
  try:
    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    # Request to download the file
    request = service.files().get_media(fileId=file_id)
    with open(destination, 'wb') as fh:
      downloader = MediaIoBaseDownload(fh, request)
      done = False
      while done is False:
        # Download the file in chunks
        done = downloader.next_chunk()
        print(f"Downloading...")
  except HttpError as error:
    logging.error(f"An error occurred: {error}")

def delete_file(creds, file_id):
  """
  Deletes a file from the user's Google Drive.

  Args:
    creds (Credentials): The authenticated user's credentials.
    file_id (str): The ID of the file to delete.
  """
  try:
    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    # Delete the file
    service.files().delete(fileId=file_id).execute()
    print(f"File {file_id} deleted.")
  except HttpError as error:
    logging.error(f"An error occurred: {error}")

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
    download_file(creds, file_id, 'downloaded_test.txt')

    # Delete the file
    print(f"Deleting file with ID: {file_id}")
    delete_file(creds, file_id)
  else:
    print("Uploaded file not found.")

if __name__ == "__main__":
  main()