from storage.base import Storage
from azure.storage.blob import BlobServiceClient
import os
import io

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

    def open(self, filename):
        blob_client = self.container_client.get_blob_client(filename)
        stream = blob_client.download_blob()
        return io.BytesIO(stream.readall())
