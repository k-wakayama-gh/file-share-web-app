from storage.base import Storage
import os

UPLOAD_DIR = "local_storage"

class LocalStorage(Storage):
    def __init__(self):
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    def list_files(self):
        files = []
        for name in os.listdir(UPLOAD_DIR):
            path = os.path.join(UPLOAD_DIR, name)

            if not os.path.isfile(path):
                continue

            files.append({
                "name": name,
                "size": round(os.path.getsize(path) / (1024 * 1024), 1),
            })
        return files

    def upload(self, filename, fileobj):
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            f.write(fileobj.read())

    def delete(self, filename):
        path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(path):
            os.remove(path)

    def open(self, filename):
        path = os.path.join(UPLOAD_DIR, filename)
        return open(path, "rb")
