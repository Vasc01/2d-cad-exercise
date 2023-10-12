from abc import ABC, abstractmethod


class EditorAbc(ABC):

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


class Editor(EditorAbc):

    def add(self):
        pass

    def remove(self):
        pass

    def move(self):
        pass

    def rotate(self):
        pass

    def mirror(self):
        pass

    def scale(self):
        pass

    def fill(self):
        pass

    def clear(self):
        pass
