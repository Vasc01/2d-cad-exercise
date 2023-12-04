"""Provide connection between the frontend and backend.

Complex manipulations of data are sent to the backend. Simpler manipulations are handled in the presenter.
The result is sent as simplified data to the frontend.
"""
from abc import ABC, abstractmethod

from backend.core import Group, Element
from frontend.command import MoveCommand, RotateCommand, MirrorCommand, ScaleCommand
from frontend.initial_data import transformer


class PresenterABC(ABC):

    @abstractmethod
    def receive_user_input(self, component, command,  command_values):
        raise NotImplementedError

    @abstractmethod
    def update(self, x, y):
        raise NotImplementedError


class Presenter(PresenterABC):
    """Receives information from the frontend and returns it after calculations are done.

    Attributes:
        canvas_group (None/Group): Group that contains the elements currently on the canvas.
        temporary_group (None/Group): Group that contains elements during manipulation.
        palette_group (None/Group): Preset elements to chose from.
        predefined_shapes (dict): Preset shapes to import on the canvas.
        reference_point (None/tuple): User chosen coordinates as reference for transformations.
        canvas_entries (list): Simplified element data to be used by the view-module.
        palette_entries (list): Simplified element data to be used by the view-module.
    """

    def __init__(self, view):
        self.view = view

        # groups with elements
        self.canvas_group = None
        self.temporary_group = None
        self.palette_group = None
        self.predefined_shapes = {}

        # variables
        self.reference_point = None

        # content for user interface
        self.canvas_entries = []
        self.palette_entries = []

# -------------------MVP--------------------------------------------------------

    def receive_user_input(self, component, command,  command_values):
        """Used by view

        The view calls this method to activate commands used on elements/group.

        Args:
            component (Group): Group to be manipulated in the backend.
            command (str): Transformation type.
            command_values: Data needed for the specific transformation.
        """

        if command == "move":
            delta_x, delta_y = command_values
            move_command = MoveCommand(component, delta_x, delta_y)
            move_command.attach(self)
            move_command.execute()

        elif command == "rotate":
            theta, reference_point = command_values
            transformer.set_reference(*reference_point)
            rotate_command = RotateCommand(component, theta)
            rotate_command.execute()

        elif command == "mirror":
            direction, reference_point = command_values
            transformer.set_reference(*reference_point)
            mirror_command = MirrorCommand(component, direction)
            mirror_command.execute()

        elif command == "scale":
            scale_x, scale_y, reference_point = command_values
            transformer.set_reference(*reference_point)
            scale_command = ScaleCommand(component, scale_x, scale_y)
            scale_command.execute()

    def update(self, x, y):
        """Used by the model

        The model calls this method as part of observer design pattern and sends as parameters
        the newly calculated x and y
        """
        pass

# ------------------------------------------------------------------------------

    def set_canvas_group(self, canvas_group):
        self.canvas_group = canvas_group

    def set_temporary_group(self, temporary_group):
        self.temporary_group = temporary_group

    def set_palette_group(self, palette_group):
        self.palette_group = palette_group

    def add_predefined_shape(self, shape_name, shape_group):
        if shape_name not in self.predefined_shapes:
            self.predefined_shapes[shape_name] = shape_group

    def create_palette_view(self):
        for el in self.palette_group.elements:
            self.palette_entries.append((el.y, el.x, el.symbol))

    def load_palette_view(self):
        self.create_palette_view()
        self.view.update_ui("palette", self.palette_entries)
        self.palette_entries.clear()

    def create_canvas_view(self):

        for el in self.canvas_group.elements:
            self.canvas_entries.append((el.y, el.x, el.symbol))

            # check if there are elements in the element - true if it is a group
            try:
                for el_in in el.elements:
                    self.canvas_entries.append((el_in.y, el_in.x, el_in.symbol))
                    self.canvas_entries.append((el.y, el.x, el.symbol, "reverse"))
            except AttributeError:
                pass

    def load_canvas_view(self):
        self.create_canvas_view()
        self.view.update_ui("canvas", self.canvas_entries)
        self.canvas_entries.clear()

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

    def canvas_to_temp(self, x, y):
        """Move elements and groups from canvas to temporary group.

        Allows selection and highlight of multiple elements. The selected elements are temporary taken out of the
        canvas for transformation. This way the rest of the elements on the canvas are unaffected.

        Args:
            x (int): Cursor position.
            y (int): Cursor position.
        Returns:
            None
        """

        for el in self.canvas_group.elements:

            # check if element position is the same as cursor position
            if round(el.x) == x and round(el.y) == y:
                self.temporary_group.add(el)
                self.canvas_group.remove(el)
                self.view.update_ui("canvas", [(y, x, el.symbol, "standout")])

                # in case the element is a groped shape the inner elements are highlighted too
                try:
                    for el_in in el.elements:
                        self.view.update_ui("canvas", [(el_in.y, el_in.x, el_in.symbol, "standout")])
                except AttributeError:
                    pass

    def palette_to_temp(self, x, y):
        """Adds element from the predefined palette to the temporary group.

        Allows selection and highlight of only one element.

        Args:
            x (int): Cursor position.
            y (int): Cursor position.
        Returns:
            None
        """
        # check if there is element at the selected coordinates
        for el in self.palette_group.elements:
            if el.x == x and el.y == y:

                # override the selection each time; allow only one selection to draw with
                if len(self.temporary_group.elements) != 0:
                    self.temporary_group.elements.clear()
                    self.load_palette_view()
                self.temporary_group.add(el)
                self.view.update_ui("palette", [(y, x, el.symbol, "standout")])

    def temp_to_canvas(self):
        """Returns elements and groups to the canvas usually after the transformation.

        Args:

        Returns:
            None
        """
        for el in self.temporary_group.elements:
            self.canvas_group.add(el)

    def new_el_to_canvas(self, x, y):
        """Single element is created on the canvas

        Single element selected from the palette with Add Element command is created on the canvas at the current
        cursor position.

        Args:
            x (int): Cursor position.
            y (int): Cursor position.
        Returns:
            None
        """
        symbol = self.temporary_group.elements[0].symbol
        element = Element(x, y).set_transformer(transformer).set_symbol(symbol)
        self.canvas_group.add(element)
        self.view.update_ui("canvas", [(y, x, symbol, "standout")])
