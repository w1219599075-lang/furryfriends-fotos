"""
Azure Blob Storage 服务类
用于处理图片上传到Azure Blob Storage
"""

import os
import uuid
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from werkzeug.utils import secure_filename


class BlobStorageService:
    """Azure Blob Storage 服务类"""

    def __init__(self, connection_string, container_original, container_thumbnail):
        """
        初始化 Blob Storage 服务

        Args:
            connection_string: Azure Storage 连接字符串
            container_original: 原图容器名称
            container_thumbnail: 缩略图容器名称
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_original = container_original
        self.container_thumbnail = container_thumbnail

        # 确保容器存在
        self._ensure_containers_exist()

    def _ensure_containers_exist(self):
        """确保容器存在，如果不存在则创建"""
        try:
            # 检查原图容器
            original_container = self.blob_service_client.get_container_client(self.container_original)
            if not original_container.exists():
                original_container.create_container()

            # 检查缩略图容器
            thumbnail_container = self.blob_service_client.get_container_client(self.container_thumbnail)
            if not thumbnail_container.exists():
                thumbnail_container.create_container()
        except Exception as e:
            print(f"检查/创建容器时出错: {e}")

    def _get_file_extension(self, filename):
        """获取文件扩展名"""
        return os.path.splitext(filename)[1].lower()

    def _generate_unique_filename(self, original_filename):
        """
        生成唯一的文件名

        Args:
            original_filename: 原始文件名

        Returns:
            唯一的文件名 (UUID + 扩展名)
        """
        ext = self._get_file_extension(original_filename)
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{ext}"

    def upload_file(self, file_stream, original_filename, content_type='image/jpeg'):
        """
        上传文件到 Azure Blob Storage

        Args:
            file_stream: 文件流对象
            original_filename: 原始文件名
            content_type: 文件MIME类型

        Returns:
            dict: 包含blob_name和url的字典
        """
        try:
            # 生成唯一文件名
            blob_name = self._generate_unique_filename(original_filename)

            # 获取容器客户端
            container_client = self.blob_service_client.get_container_client(self.container_original)

            # 上传文件
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(file_stream, content_type=content_type, overwrite=True)

            # 获取文件URL
            blob_url = blob_client.url

            return {
                'success': True,
                'blob_name': blob_name,
                'url': blob_url
            }

        except Exception as e:
            print(f"上传文件时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def generate_download_url(self, blob_name, container_name=None, expiry_hours=24):
        """
        生成带SAS令牌的下载URL

        Args:
            blob_name: Blob文件名
            container_name: 容器名称（默认使用原图容器）
            expiry_hours: 链接有效期（小时）

        Returns:
            带SAS令牌的完整URL
        """
        try:
            if container_name is None:
                container_name = self.container_original

            # 获取账户信息
            account_name = self.blob_service_client.account_name
            account_key = self.blob_service_client.credential.account_key

            # 生成SAS令牌
            sas_token = generate_blob_sas(
                account_name=account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=expiry_hours)
            )

            # 构建完整URL
            blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
            return blob_url

        except Exception as e:
            print(f"生成下载URL时出错: {e}")
            # 如果生成SAS令牌失败，返回基本URL
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name or self.container_original,
                blob=blob_name
            )
            return blob_client.url

    def delete_file(self, blob_name, container_name=None):
        """
        删除文件

        Args:
            blob_name: Blob文件名
            container_name: 容器名称（默认使用原图容器）

        Returns:
            bool: 删除是否成功
        """
        try:
            if container_name is None:
                container_name = self.container_original

            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.delete_blob()

            return True

        except Exception as e:
            print(f"删除文件时出错: {e}")
            return False

    def get_thumbnail_url(self, original_blob_name):
        """
        获取缩略图URL（如果存在）

        Args:
            original_blob_name: 原图的blob名称

        Returns:
            缩略图URL，如果不存在则返回None
        """
        try:
            container_client = self.blob_service_client.get_container_client(self.container_thumbnail)
            blob_client = container_client.get_blob_client(original_blob_name)

            # 检查缩略图是否存在
            if blob_client.exists():
                return self.generate_download_url(original_blob_name, self.container_thumbnail)
            else:
                return None

        except Exception as e:
            print(f"获取缩略图URL时出错: {e}")
            return None


def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg', 'gif', 'webp'}):
    """
    检查文件扩展名是否允许

    Args:
        filename: 文件名
        allowed_extensions: 允许的扩展名集合

    Returns:
        bool: 是否允许
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
