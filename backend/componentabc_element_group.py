# Composite pattern

from abc import ABC, abstractmethod
from typing import List
from backend.editorabc_editor import EditorAbc


class ComponentAbc(ABC):

    @abstractmethod
    def edit(self):
        pass


class Element(ComponentAbc):

    def __init__(self, editor: EditorAbc):
        self.x = ""
        self.y = ""
        self.name = ""
        self.symbol = ""
        self.symbol_color = ""
        self.background_color = ""
        self.editor = editor

    def edit(self):
        pass


class Group(ComponentAbc):

    def __init__(self):
        self.x = ""
        self.y = ""
        self.elements: List[ComponentAbc] = []

    def edit(self):
        for element in self.elements:
            element.edit()

