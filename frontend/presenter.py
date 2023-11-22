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

    def __init__(self, view):
        self.view = view

        # groups with elements
        self.canvas_group = None
        self.temporary_group = None
        self.palette_group = None
        self.predefined_shapes = {}

        # needed for ui
        self.canvas_entries = []
        self.palette_entries = []

    def set_canvas_group(self, canvas_group):
        self.canvas_group = canvas_group

    def set_temporary_group(self, temporary_group):
        self.temporary_group = temporary_group

    def set_palette_group(self, palette_group):
        self.palette_group = palette_group

    def add_predefined_shape(self, shape_name, shape_group):
        if shape_name not in self.predefined_shapes:
            self.predefined_shapes[shape_name] = shape_group

# ------------------------------------------------------------------------------

    def receive_user_input(self):
        pass

    def create_view(self):
        self.view.update_ui()

    def update(self, x, y):
        """Used by the model

        The model calls this method as part of observer design pattern and sends as parameters
        the newly calculated x and y
        """
        pass

# ------------------------------------------------------------------------------

    def create_palette_view(self):
        for el in self.palette_group.elements:
            self.palette_entries.append((el.y, el.x, el.symbol))

    def load_palette(self):
        self.create_palette_view()
        self.view.update_ui("palette", self.palette_entries)

    def create_canvas_view(self, height, width):

        for el in self.canvas_group.elements:
            # elements out of the canvas are not displayed, yet they still exist
            if round(el.x) not in range(0, width) or round(el.y) not in range(0, height):
                continue
            self.canvas_entries.append((round(el.y), round(el.x), el.symbol))

            try:
                for el_in in el.elements:
                    # group-elements out of the canvas are not displayed, yet they still exist
                    if round(el_in.x) not in range(0, width) or round(el_in.y) not in range(0, height):
                        continue
                    self.canvas_entries.append((round(el_in.y), round(el_in.x), el_in.symbol))
                    self.canvas_entries.append((round(el.y), round(el.x), el.symbol, "reverse"))
            except AttributeError:
                pass

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
