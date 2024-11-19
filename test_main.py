import pytest
from unittest.mock import patch, MagicMock
from main import authenticate, list_files, upload_file, download_file, delete_file

# Mock credentials
@pytest.fixture
def mock_creds():
  return MagicMock()

# Test authenticate function
@patch('main.os.path.exists', return_value=True)
@patch('main.Credentials.from_authorized_user_file')
def test_authenticate(mock_from_authorized_user_file, mock_exists):
  mock_from_authorized_user_file.return_value = MagicMock(valid=True)
  creds = authenticate()
  assert creds.valid

# Test list_files function
@patch('main.build')
def test_list_files(mock_build, mock_creds):
  mock_service = MagicMock()
  mock_build.return_value = mock_service
  mock_service.files().list().execute.return_value = {
    'files': [{'id': '1', 'name': 'test.txt', 'mimeType': 'text/plain', 'modifiedTime': '2024-11-18T00:00:00Z'}]
  }
  list_files(mock_creds)
  mock_service.files().list.assert_called_once()

# Test upload_file function
@patch('main.build')
@patch('main.MediaFileUpload')
def test_upload_file(mock_media_file_upload, mock_build, mock_creds):
  mock_service = MagicMock()
  mock_build.return_value = mock_service
  mock_service.files().create().execute.return_value = {'id': '1'}
  upload_file(mock_creds, 'test.txt')
  mock_service.files().create.assert_called_once()

# Test download_file function
@patch('main.build')
@patch('main.open', new_callable=MagicMock)
@patch('main.MediaIoBaseDownload')
def test_download_file(mock_media_io_base_download, mock_open, mock_build, mock_creds):
  mock_service = MagicMock()
  mock_build.return_value = mock_service
  mock_downloader = MagicMock()
  mock_media_io_base_download.return_value = mock_downloader
  mock_downloader.next_chunk.return_value = (MagicMock(progress=1.0), True)
  download_file(mock_creds, '1', 'destination.txt')
  mock_service.files().get_media.assert_called_once()

# Test delete_file function
@patch('main.build')
def test_delete_file(mock_build, mock_creds):
  mock_service = MagicMock()
  mock_build.return_value = mock_service
  delete_file(mock_creds, '1')
  mock_service.files().delete.assert_called_once()