
import os
import shutil
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
import json

class GmxDriveClient:
    """Google Drive API Client"""
    
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, folder_id: str, credentials_json: dict = None):
        """
        Initialize Drive Client
        
        Args:
            folder_id (str): Target Google Drive Folder ID
            credentials_json (dict, optional): Service Account Credentials
        """
        self.folder_id = folder_id
        
        if credentials_json:
            # Check if it's a Service Account or User OAuth Token
            if 'type' in credentials_json and credentials_json['type'] == 'service_account':
                print("   🔑 Authenticating with Service Account...")
                self.creds = service_account.Credentials.from_service_account_info(
                    credentials_json, scopes=self.SCOPES
                )
            else:
                print("   🔑 Authenticating with OAuth Token (User Account)...")
                # Assuming credentials_json is the token.json content
                self.creds = Credentials.from_authorized_user_info(credentials_json, self.SCOPES)
        else:
            # Fallback for local testing or environment variable
            # Ideally should pass credentials explicitly
            raise ValueError("Credentials are required")

        self.service = build('drive', 'v3', credentials=self.creds)

    def upload_folder(self, local_folder_path: str | Path, target_folder_id: str = None) -> str:
        """
        Uploads a local folder and its contents to Google Drive.
        
        Args:
            local_folder_path (str | Path): Path to the local folder
            target_folder_id (str, optional): ID of the parent folder on Drive. 
                                              Defaults to self.folder_id.
                                              
        Returns:
            str: ID of the uploaded folder
        """
        local_folder = Path(local_folder_path)
        if not local_folder.exists():
            raise FileNotFoundError(f"Local folder not found: {local_folder}")
        
        parent_id = target_folder_id if target_folder_id else self.folder_id
        
        # 1. Create the folder on Drive in the parent folder
        folder_metadata = {
            'name': local_folder.name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        
        # Check if folder already exists (optional, but good for idempotency)
        # For simplicity in this tool, we might just create a new one or handle duplication.
        # Let's simple check if exists to avoid duplicates if re-run
        existing = self._find_folder(local_folder.name, parent_id)
        if existing:
            drive_folder_id = existing['id']
            print(f"   Drive folder exists: {local_folder.name} (ID: {drive_folder_id})")
        else:
            drive_folder = self.service.files().create(
                body=folder_metadata, fields='id'
            ).execute()
            drive_folder_id = drive_folder.get('id')
            print(f"   Created Drive folder: {local_folder.name} (ID: {drive_folder_id})")

        # 2. Upload files in the directory
        for item in local_folder.iterdir():
            if item.is_file():
                self._upload_file(item, drive_folder_id)
            elif item.is_dir():
                # Recursive upload
                self.upload_folder(item, drive_folder_id)
                
        return drive_folder_id

    def _find_folder(self, name: str, parent_id: str):
        """Find a folder by name inside a parent folder"""
        query = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and '{parent_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = results.get('files', [])
        return files[0] if files else None

    def _upload_file(self, file_path: Path, parent_id: str):
        """Upload a single file"""
        file_metadata = {
            'name': file_path.name,
            'parents': [parent_id]
        }
        media = MediaFileUpload(
            str(file_path),
            resumable=True
        )
        # Check existence to update or skip? Let's update (overwrite) logic
        # Ideally: trash old file and upload new, or update content.
        # Simple approach: Check if exists, if so delete? Or just upload duplicate?
        # Standard drive behavior allows duplicates. Let's try to avoid them.
        existing = self._find_file(file_path.name, parent_id)
        if existing:
            # Update existing file content
            self.service.files().update(
                fileId=existing['id'],
                media_body=media
            ).execute()
            print(f"   Updated file: {file_path.name}")
        else:
            self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(f"   Uploaded file: {file_path.name}")

    def _find_file(self, name: str, parent_id: str):
        """Find a file by name inside a parent folder"""
        query = f"name='{name}' and '{parent_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = results.get('files', [])
        return files[0] if files else None
