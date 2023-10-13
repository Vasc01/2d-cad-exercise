# Composite pattern

from abc import ABC, abstractmethod
from typing import List
from backend.editorabc_editor import EditorAbc


class ComponentAbc(ABC):

    @abstractmethod
    def move(self, x, y):
        pass


class Leaf(ComponentAbc):

    def __init__(self, editor: EditorAbc):
        self.x = 1
        self.y = 1
        self.name = ""
        self.symbol = ""
        self.symbol_color = ""
        self.background_color = ""
        self.editor = editor

    def move(self, delta_x, delta_y):
        self.x, self.y = self.editor.move(self.x, self.y, delta_x, delta_y)


class Composite(ComponentAbc):

    def __init__(self, editor: EditorAbc):
        self.x = ""
        self.y = ""
        self.elements: List[ComponentAbc] = []
        self.editor = editor

    def add(self, element: Leaf):
        self.elements.append(element)

    def remove(self, element: Leaf):
        self.elements.remove(element)

    def move(self, delta_x, delta_y):
        for element in self.elements:
            element.move(delta_x, delta_y)

