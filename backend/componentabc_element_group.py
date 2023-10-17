# Composite pattern

from abc import ABC, abstractmethod
from typing import List
from backend.transformer import TransformerAbc


class ComponentAbc(ABC):

    @abstractmethod
    def set_transformer(self, transformer):
        pass

    @abstractmethod
    def move(self, x, y):
        pass


class Element(ComponentAbc):

    def __init__(self, x, y, transformer=TransformerAbc):
        self.x = x
        self.y = y
        self.name = ""
        self.symbol = ""
        self.symbol_color = ""
        self.background_color = ""
        self.transformer = transformer

    def set_transformer(self, transformer):
        self.transformer = transformer

    def move(self, *args):
        self.x, self.y = self.transformer.move(self.x, self.y, *args)

    def rotate(self):
        self.transformer.rotate()

    def mirror(self):
        self.transformer.mirror()

    def scale(self):
        self.transformer.scale()

    def fill(self):
        pass


class Group(ComponentAbc):

    def __init__(self, transformer=TransformerAbc):
        self.x = ""
        self.y = ""
        self.elements: List[ComponentAbc] = []
        self.transformer = transformer

    def add(self, element: Element):
        self.elements.append(element)

    def remove(self, element: Element):
        self.elements.remove(element)

    def set_transformer(self, transformer):
        self.transformer = transformer

    def move(self, delta_x, delta_y):
        for element in self.elements:
            element.set_transformer(self.transformer)
            element.move(delta_x, delta_y)

    def fill(self):
        pass
