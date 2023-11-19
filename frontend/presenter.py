from abc import ABC, abstractmethod

from backend.core import Group, Element
from frontend.initial_data import transformer


class PresenterABC(ABC):

    @abstractmethod
    def receive_user_input(self):
        raise NotImplementedError

    @abstractmethod
    def create_view(self):
        raise NotImplementedError

    @abstractmethod
    def update(self, x, y):
        raise NotImplementedError


class Presenter(PresenterABC):

    def __init__(self, view, canvas_group, temporary_group, palette_group):
        self.view = view

        # groups with elements
        self.canvas_group = canvas_group
        self.temporary_group = temporary_group
        self.palette_group = palette_group
        self.predefined_shapes = {}

    def receive_user_input(self):
        pass

    def create_view(self):
        self.view.update()

    def update(self, x, y):
        """Used by the model

        The model calls this method as part of observer design pattern and sends as parameters
        the newly calculated x and y
        """
        pass

    def add_predefined_shape(self, shape_name, shape_group):
        if shape_name not in self.predefined_shapes:
            self.predefined_shapes[shape_name] = shape_group

    def predefined_shape_to_canvas(self, shape_name):
        """Insert predefined shape on the canvas.

        A copy of the predefined shape is created. This way the original doesn't get lost after transformations
        or deletion.

        Args:
            shape_name (str): A predefined shape.
        Returns:
            None
        """
        if shape_name in self.predefined_shapes:
            new_group = Group()
            new_group.set_transformer(transformer)
            new_group.x = self.predefined_shapes[shape_name].x
            new_group.y = self.predefined_shapes[shape_name].y
            for el in self.predefined_shapes[shape_name].elements:
                new_element = Element(el.x, el.y).set_transformer(transformer).set_symbol(el.symbol)
                new_group.add(new_element)
            self.canvas_group.add(new_group)
