# Composite pattern

from abc import ABC, abstractmethod
from typing import List
from backend.transformer import TransformerAbc


class ComponentAbc(ABC):

    @abstractmethod
    def set_transformer(self, transformer):
        pass

    @abstractmethod
    def move(self, *args):
        pass

    @abstractmethod
    def rotate(self, *args):
        pass

    @abstractmethod
    def mirror(self, *args):
        pass

    @abstractmethod
    def scale(self, *args):
        pass

    @abstractmethod
    def fill(self, *args):
        pass


class Element(ComponentAbc):

    def __init__(self, x, y, transformer=TransformerAbc):
        self.x = x
        self.y = y
        self.transformer = transformer

        self.name = ""
        self.symbol = ""
        self.symbol_color = ""
        self.background_color = ""

    def set_transformer(self, transformer):
        self.transformer = transformer
        return self

    def set_name(self, name):
        self.name = name
        return self

    def set_symbol(self, symbol):
        self.symbol = symbol
        return self

    def set_symbol_color(self, color):
        self.symbol_color = color
        return self

    def set_background_color(self, color):
        self.background_color = color
        return self

    def move(self, delta_x, delta_y):
        self.x, self.y = self.transformer.move(self.x, self.y, delta_x, delta_y)

    def rotate(self, theta):
        self.x, self.y = self.transformer.rotate(self.x, self.y, theta)

    def mirror(self, axis):
        self.x, self.y = self.transformer.mirror(self.x, self.y, axis)

    def scale(self, factor_x, factor_y):
        self.x, self.y = self.transformer.mirror(self.x, self.y, factor_x, factor_y)

    def fill(self, setter, value):
        self.set_name(value) if setter == "set_name"


class Group(ComponentAbc):

    def __init__(self, transformer=TransformerAbc):
        self.x = ""
        self.y = ""
        self.transformer = transformer

        self.elements: List[ComponentAbc] = []

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

    def rotate(self, theta):
        for element in self.elements:
            element.set_transformer(self.transformer)
            element.rotate(theta)

    def mirror(self, axis):
        for element in self.elements:
            element.set_transformer(self.transformer)
            element.mirror(axis)

    def scale(self, factor_x, factor_y):
        for element in self.elements:
            element.set_transformer(self.transformer)
            element.scale(factor_x, factor_y)

    def fill(self, setter, value):
        for element in self.elements:
            element.fill(setter, value)

    def union(self, other):
        self.elements.extend(other.elements)
        return self.elements

    def difference(self, other):
        for element in self.elements:
            if element in other.elements:
                self.elements.remove(element)
        return self.elements

    def split(self, other):
        elements_group_1 = []
        elements_intersection = []
        elements_group_2 = []



        return self.elements
