"""Point-like entry in the 2D-plane with additional characteristics

This module defines the objects in 2D-space on which the transformations are executed.
Using the composite design pattern Elements and Groups of elements are defined.
"""

from abc import ABC, abstractmethod
from typing import List

from backend.memento import CanvasMemento
from backend.model import ModelABC
from backend.transformer import TransformerAbc


class ComponentAbc(ModelABC, ABC):
    pass

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
    """The smallest unit in the composite structure

    Besides the xy-coordinates the element has additional characteristics, which can make it
    distinguishable in multiple ways.

    Attributes:
            x (int/float): Location of the element.
            y (int/float): Location of the element.
            transformer (TransformerAbc): Defines the rules for coordinate transformation.
            name (str): Used for description purpose.
            symbol (str): Used for representation and distinction.
            symbol_color (str): Used for representation and distinction.
            background_color (str): Used for representation and distinction.
    """
    def __init__(self, x, y, transformer=TransformerAbc):
        self.x = x
        self.y = y
        self.transformer = transformer

        self.name = ""
        self.symbol = ""
        self.symbol_color = ""
        self.background_color = ""

        # needed for observer design pattern; presenter is the observer
        self.subscribers = []

    def attach(self, observer):
        self.subscribers.append(observer)

    def detach(self, observer):
        self.subscribers.remove(observer)

    def notify(self):
        for subscriber in self.subscribers:
            subscriber.update(self.x, self.y)

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
        self.notify()

    def rotate(self, theta):
        self.x, self.y = self.transformer.rotate(self.x, self.y, theta)
        self.notify()

    def mirror(self, axis):
        self.x, self.y = self.transformer.mirror(self.x, self.y, axis)
        self.notify()

    def scale(self, factor_x, factor_y):
        self.x, self.y = self.transformer.scale(self.x, self.y, factor_x, factor_y)
        self.notify()

    def fill(self, setter, value):
        """Connects the Group-class with the setters of this class

        The method receives indication which setter of this class should be activated
        and what value should be passed.

        Args:
            setter (str): Identifier for the setter.
            value (str): Value for the setter.

        Returns:
            None
        """
        if setter == "name":
            self.set_name(value)
        elif setter == "symbol":
            self.set_symbol(value)
        elif setter == "symbol color":
            self.set_symbol_color(value)
        elif setter == "background":
            self.set_background_color(value)


class Group(ComponentAbc):
    """A group can contain multiple objects of the class Element

    A group calls the coordinate transformation on all elements that it contains.

    Attributes:
            transformer (TransformerAbc): Defines the rules for coordinate transformation.
            elements (List): contains Element-objects
    """

    def __init__(self, transformer=TransformerAbc):
        self.x = 0
        self.y = 0
        self.symbol = "+"
        self.transformer = transformer
        self.elements: List[ComponentAbc] = []

        # needed for observer design pattern; presenter is the observer
        self.subscribers = []

    def attach(self, observer):
        self.subscribers.append(observer)

    def detach(self, observer):
        self.subscribers.remove(observer)

    def notify(self):
        for subscriber in self.subscribers:
            subscriber.update(self.x, self.y)

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

        self.x, self.y = self.transformer.move(self.x, self.y, delta_x, delta_y)
        self.notify()

    def rotate(self, theta):
        for element in self.elements:
            element.set_transformer(self.transformer)
            element.rotate(theta)

        self.x, self.y = self.transformer.rotate(self.x, self.y, theta)
        self.notify()

    def mirror(self, axis):
        for element in self.elements:
            element.set_transformer(self.transformer)
            element.mirror(axis)

        self.x, self.y = self.transformer.mirror(self.x, self.y, axis)
        self.notify()

    def scale(self, factor_x, factor_y):
        for element in self.elements:
            element.set_transformer(self.transformer)
            element.scale(factor_x, factor_y)

        self.x, self.y = self.transformer.scale(self.x, self.y, factor_x, factor_y)
        self.notify()

    def fill(self, setter: str, value):
        """Sets attribute values for all elements in the group

        Args:
            setter (str): Identifier for the setter.
            value (str): Value for the setter.

        Returns:
            None
        """
        for element in self.elements:
            element.fill(setter, value)

    def union(self, other):
        """Combines elements of two groups

        Args:
            other (Group): Group with elements, which will be added to the current group.

        Returns:
            List of elements.
        """
        self.elements.extend(other.elements)
        return self.elements

    def difference(self, other):
        """Reduce number of elements in the current group

        Args:
            other (Group): Group with elements, which will be removed from the current group
            if belonging to both groups.

        Returns:
            List of elements.
        """
        for element in self.elements:
            if element in other.elements:
                self.elements.remove(element)
        return self.elements

    def split(self, other):
        """Split the elements of two groups in three groups

        The split produces following result:
            Elements belonging only to the first group.
            Elements belonging only to the second group.
            Elements belonging to both groups.

        Args:
            other (Group): Group with elements.

        Returns:
            List with three entries, which are lists of elements.
        """
        elements_group_1 = []
        elements_intersection = []
        elements_group_2 = []

        for element in self.elements:
            if element not in other.elements:
                elements_group_1.append(element)
            else:
                elements_intersection.append(element)

        for element in other.elements:
            if element not in self.elements:
                elements_group_2.append(element)

        return [elements_group_1, elements_intersection, elements_group_2]


class Canvas(Group):
    """The canvas is a selection of all elements.
    """

    def create_memento(self):
        return CanvasMemento(self.elements)

    def restore_from_memento(self, memento):
        self.elements = memento.get_state()
