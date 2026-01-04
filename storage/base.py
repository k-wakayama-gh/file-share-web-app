from abc import ABC, abstractmethod
from typing import BinaryIO

class Storage(ABC):
    @abstractmethod
    def list_files(self):
        pass

    @abstractmethod
    def upload(self, filename: str, fileobj: BinaryIO, metadata: dict):
        pass

    @abstractmethod
    def delete(self, filename: str):
        pass

    @abstractmethod
    def open(self, filename: str):
        """読み取り用のファイルオブジェクトを返す"""
        pass
