import pytest
from main import authenticate, list_files, upload_file, download_file, delete_file

def test_integration():
  # Authenticate and get credentials
  creds = authenticate()
  assert creds.valid

  # List files
  items = list_files(creds)

  # Upload a file
  upload_file(creds, 'test.txt')

  file_id = None
  for item in items:
    if item['name'] == 'test.txt':
      file_id = item['id']
      break
    
  assert file_id is not None, "Uploaded file ID not found."

  # Download a file
  download_file(creds, file_id, 'downloaded_test.txt')

  # Delete a file
  delete_file(creds, file_id)