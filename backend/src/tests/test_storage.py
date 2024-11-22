import asyncio
import os
from services.google_storage import GoogleCloudStorage
from config.settings import settings
import io

async def test_upload():
    print("=== Test Configuration ===")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    credentials_path = os.path.join(os.path.dirname(base_dir), 'credentials.json')
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"Base directory: {base_dir}")
    print(f"Expected credentials path: {credentials_path}")
    print(f"Credentials exists: {os.path.exists(credentials_path)}")
    print(f"Project ID: {settings.GOOGLE_CLOUD_PROJECT}")
    print(f"Bucket name: {settings.GOOGLE_CLOUD_BUCKET}")
    
    try:
        print("\n=== Testing Upload ===")
        storage = GoogleCloudStorage()
        test_content = io.BytesIO(b"Hello, World!")
        url = await storage.upload_file(test_content, "test.txt")
        print(f"File uploaded successfully: {url}")
        
        print("\n=== Testing Delete ===")
        try:
            await storage.delete_file("test.txt")
            print("File deleted successfully")
        except Exception as delete_error:
            print(f"Warning: Could not delete file: {str(delete_error)}")
            print("This is not critical as the file will be cleaned up automatically")
        
    except Exception as e:
        print(f"\n=== Error in Test ===")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_upload()) 