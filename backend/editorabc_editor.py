from abc import ABC, abstractmethod


class EditorAbc(ABC):

    @abstractmethod
    def move(self, x, y, delta_x, delta_y):
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

    def move(self, x, y, delta_x, delta_y):
        x += delta_x
        y += delta_y
        print("Editor is moving things")
        return x, y

    def rotate(self):
        print("Editor is rotating things")

    def mirror(self):
        print("Editor is mirroring things")

    def scale(self):
        print("Editor is scaling things")

    def fill(self):
        print("Editor is filling things")

    def clear(self):
        print("Editor is clearing things")
