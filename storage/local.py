from storage.base import Storage
import os
import json

UPLOAD_DIR = "local_storage"

class LocalStorage(Storage):
    def __init__(self):
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    def list_files(self):
        files = []
        for name in os.listdir(UPLOAD_DIR):
            if name.endswith(".json"):
                continue

            path = os.path.join(UPLOAD_DIR, name)
            meta_path = path + ".json"

            uploader = "不明"
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    uploader = json.load(f).get("uploader", "不明")

            files.append({
                "name": name,
                "size": round(os.path.getsize(path) / 1024, 1),
                "uploader": uploader
            })
        return files

    def upload(self, filename, fileobj, metadata):
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            f.write(fileobj.read())

        with open(path + ".json", "w", encoding="utf-8") as f:
            json.dump(metadata, f)

    def delete(self, filename):
        path = os.path.join(UPLOAD_DIR, filename)
        os.remove(path)
        meta = path + ".json"
        if os.path.exists(meta):
            os.remove(meta)

    def open(self, filename):
        path = os.path.join(UPLOAD_DIR, filename)
        return open(path, "rb")
