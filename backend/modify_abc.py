from abc import ABC, abstractmethod


class ModifyAbc(ABC):

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def rotate(self):
        pass

    @abstractmethod
    def mirror(self):
        pass

    @abstractmethod
    def scale(self):
        pass

    @abstractmethod
    def fill(self):
        pass

    @abstractmethod
    def clear(self):
        pass
