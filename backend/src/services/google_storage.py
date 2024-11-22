from google.cloud import storage
from google.oauth2 import service_account
from config.settings import settings
import os
from datetime import datetime, timedelta

class GoogleCloudStorage:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        credentials_path = os.path.join(os.path.dirname(base_dir), 'credentials.json')
        
        print(f"Initializing Google Cloud Storage:")
        print(f"Project ID: {settings.GOOGLE_CLOUD_PROJECT}")
        print(f"Bucket Name: {settings.GOOGLE_CLOUD_BUCKET}")
        print(f"Credentials Path: {credentials_path}")
        
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Credentials file not found at {credentials_path}")
            
        try:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            
            self.client = storage.Client(
                credentials=credentials,
                project=settings.GOOGLE_CLOUD_PROJECT
            )
            
            print(f"Successfully created storage client")
            
            self.bucket = self.client.bucket(settings.GOOGLE_CLOUD_BUCKET)
            print(f"Successfully connected to bucket: {settings.GOOGLE_CLOUD_BUCKET}")
            
        except Exception as e:
            print(f"Error initializing Google Cloud Storage: {str(e)}")
            raise

    async def upload_file(self, file, filename: str) -> str:
        """Upload a file to Google Cloud Storage and return its public URL"""
        blob = self.bucket.blob(f"pdfs/{filename}")
        blob.upload_from_file(file)
        
        # Make the file publicly accessible
        blob.make_public()
        
        return blob.public_url

    async def get_signed_url(self, blob_name: str, expiration: int = 3600) -> str:
        """Get a signed URL for a file that expires after a certain time"""
        blob = self.bucket.blob(f"pdfs/{blob_name}")
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.utcnow() + timedelta(seconds=expiration),
            method="GET"
        )
        return url

    async def delete_file(self, filename: str) -> bool:
        """Delete a file from Google Cloud Storage"""
        blob = self.bucket.blob(f"pdfs/{filename}")
        blob.delete()
        return True 