from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def list_files(self):
        pass

    @abstractmethod
    def upload(self, filename, fileobj):
        pass

    @abstractmethod
    def delete(self, filename):
        pass

    @abstractmethod
    def open(self, filename):
        pass
