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

        # variables
        self.reference_point = None

        # content for user interface
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

# -------------------MVP--------------------------------------------------------

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

    def canvas_to_temp(self, x, y):                                     # let view manage highlighting
        """Move elements and groups from canvas to temporary group.

        Allows selection and highlight of multiple elements. The selected elements are temporary taken out of the
        canvas for transformation. This way the rest of the elements on the canvas are unaffected.

        Args:
            x (int): Cursor position.
            y (int): Cursor position.
        Returns:
            None
        """

        # height, width = self.canvas_in.getmaxyx()

        for el in self.canvas_group.elements:
            if round(el.x) == x and round(el.y) == y:
                self.temporary_group.add(el)
                self.canvas_group.remove(el)
                # self.canvas_in.addstr(y, x, el.symbol, curses.A_STANDOUT)
                # try:
                #     for el_in in el.elements:
                #         # group-elements out of the canvas are not highlighted
                #         if round(el_in.x) not in range(0, width) or round(el_in.y) not in range(0, height):
                #             continue
                #         self.canvas_in.addstr(round(el_in.y), round(el_in.x), el_in.symbol, curses.A_STANDOUT)
                # except AttributeError:
                #     pass

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
