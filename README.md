# Google Drive Integration Application

## Overview

This application integrates with Google Drive to perform the following tasks:

1. Authenticate the user using OAuth 2.0.
2. List files in the user’s Google Drive.
3. Upload a file to the user’s Google Drive.
4. Download a file from the user’s Google Drive.
5. Delete a file from the user’s Google Drive.

## Features

- **Authentication**: Securely authenticate users using OAuth 2.0.
- **File Management**: List, upload, download, and delete files in Google Drive.
- **Logging**: Capture important events and errors for debugging and monitoring.

## Setup Instructions

### Prerequisites

- Python 3.x installed on your system.
- A Google Cloud project with the Google Drive API enabled.
- OAuth 2.0 credentials (client ID and client secret) downloaded as `credentials.json`.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/stevenwill1597/strac_test
   cd strac_test
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

- Place your `credentials.json` file in the root directory of the project.

### Running the Application

1. Run the main script:

   ```bash
   python main.py
   ```

### Testing the Application

1. Run the unit test:

   ```bash
   pytest test_main.py
   ```

2. Run the integration test:

   ```bash
   pytest test_integration.py
   ```
