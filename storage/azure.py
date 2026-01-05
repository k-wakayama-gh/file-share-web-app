from storage.base import Storage
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os

class AzureBlobStorage(Storage):
    def __init__(self):
        conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container = os.getenv("AZURE_STORAGE_CONTAINER")

        blob_service = BlobServiceClient.from_connection_string(conn)
        self.container_client = blob_service.get_container_client(container)

    def list_files(self):
        files = []
        for blob in self.container_client.list_blobs():
            files.append({
                "name": blob.name,
                "size": round(blob.size / (1024 * 1024), 1),
            })
        return files

    def upload(self, filename, fileobj):
        blob_client = self.container_client.get_blob_client(filename)
        blob_client.upload_blob(fileobj, overwrite=True)

    def delete(self, filename):
        blob_client = self.container_client.get_blob_client(filename)
        blob_client.delete_blob()

    def get_sas_url(self, filename, expires_in_seconds=3600):
        blob_client = self.container_client.get_blob_client(filename)

        account_name = blob_client.account_name
        account_key = blob_client.credential.account_key

        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=self.container_client.container_name,
            blob_name=filename,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(seconds=expires_in_seconds)
        )

        return f"{blob_client.url}?{sas_token}"
    
    def open(self, filename):
        raise NotImplementedError()
