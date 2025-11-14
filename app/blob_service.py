"""Azure Blob Storage service for image uploads"""

import os
import uuid
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions


class BlobStorageService:
    """Azure Blob Storage service"""

    def __init__(self, connection_string, container_original, container_thumbnail):
        """
        Init blob storage service

        Args:
            connection_string: Azure Storage connection string
            container_original: Original images container
            container_thumbnail: Thumbnails container
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_original = container_original
        self.container_thumbnail = container_thumbnail

        self._ensure_containers_exist()

    def _ensure_containers_exist(self):
        """Make sure containers exist"""
        try:
            original_container = self.blob_service_client.get_container_client(self.container_original)
            if not original_container.exists():
                original_container.create_container()

            thumbnail_container = self.blob_service_client.get_container_client(self.container_thumbnail)
            if not thumbnail_container.exists():
                thumbnail_container.create_container()
        except Exception as e:
            print(f"Error creating containers: {e}")

    def _get_file_extension(self, filename):
        """Get file extension"""
        return os.path.splitext(filename)[1].lower()

    def _generate_unique_filename(self, original_filename):
        """
        Generate unique filename

        Args:
            original_filename: Original filename

        Returns:
            Unique filename (UUID + extension)
        """
        ext = self._get_file_extension(original_filename)
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{ext}"

    def upload_file(self, file_stream, original_filename, content_type='image/jpeg'):
        """
        Upload file to Azure Blob

        Args:
            file_stream: File stream
            original_filename: Original filename
            content_type: File MIME type

        Returns:
            dict: Contains blob_name and url
        """
        try:
            blob_name = self._generate_unique_filename(original_filename)
            container_client = self.blob_service_client.get_container_client(self.container_original)

            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(file_stream, content_type=content_type, overwrite=True)

            blob_url = blob_client.url

            return {
                'success': True,
                'blob_name': blob_name,
                'url': blob_url
            }

        except Exception as e:
            print(f"Upload error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def generate_download_url(self, blob_name, container_name=None, expiry_hours=24):
        """
        Generate download URL with SAS token

        Args:
            blob_name: Blob filename
            container_name: Container name (default: originals)
            expiry_hours: URL validity in hours

        Returns:
            Full URL with SAS token
        """
        try:
            if container_name is None:
                container_name = self.container_original

            account_name = self.blob_service_client.account_name
            account_key = self.blob_service_client.credential.account_key

            sas_token = generate_blob_sas(
                account_name=account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=expiry_hours)
            )

            blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
            return blob_url

        except Exception as e:
            print(f"Error generating URL: {e}")
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name or self.container_original,
                blob=blob_name
            )
            return blob_client.url

    def delete_file(self, blob_name, container_name=None):
        """
        Delete file

        Args:
            blob_name: Blob filename
            container_name: Container name (default: originals)

        Returns:
            bool: Success status
        """
        try:
            if container_name is None:
                container_name = self.container_original

            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.delete_blob()

            return True

        except Exception as e:
            print(f"Delete error: {e}")
            return False

    def get_thumbnail_url(self, original_blob_name):
        """
        Get thumbnail URL if exists

        Args:
            original_blob_name: Original blob name

        Returns:
            Thumbnail URL or None
        """
        try:
            container_client = self.blob_service_client.get_container_client(self.container_thumbnail)
            blob_client = container_client.get_blob_client(original_blob_name)

            if blob_client.exists():
                return self.generate_download_url(original_blob_name, self.container_thumbnail)
            else:
                return None

        except Exception as e:
            print(f"Error getting thumbnail: {e}")
            return None


def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg', 'gif', 'webp'}):
    """
    Check if file extension is allowed

    Args:
        filename: Filename
        allowed_extensions: Set of allowed extensions

    Returns:
        bool: Whether extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
