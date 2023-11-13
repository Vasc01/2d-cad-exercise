"""Handle the frontend interactivity.

The frontend has complex behavior to provide interactive experience. This module implements the behavior.
"""

import curses

from backend.core import Element, Group
from frontend.command import MoveCommand, RotateCommand, MirrorCommand, ScaleCommand
from frontend.initial_data import transformer


class UIFunction:
    """Contains all the functionalities for the frontend.

    Attributes:
        canvas_in (curses window): Canvas inner window(within the frame).
        prompt_in (curses window): Prompt inner window(within the frame).
        input_in (curses window): Input inner window(within the frame).
        palette_in (curses window): Palette inner window(within the frame).
        tools_window (curses window): Left toolbar window.
        canvas_group (Group): Contains the elements and groups displayed on the canvas.
        temporary_group (Group): Contains the elements undergoing transformations.
        palette_group (Group): Contains predefined elements to choose from when adding an element to the canvas.
        predefined_shapes (dictionary): Contains the predefined shapes to chose from when inserting a shape.
        position_tools_content (dictionary): Content of the left toolbar with coordinates to be
        addressed when highlighted
        reference_point (None/tuple): Contains the reference point coordinates.
    """
    def __init__(self, canvas_in, prompt_in, input_in, palette_in, tools_window, position_tools_content,
                 canvas_group, temporary_group, palette_group):

        # ui_windows
        self.canvas_in = canvas_in
        self.prompt_in = prompt_in
        self.input_in = input_in
        self.palette_in = palette_in
        self.tools_window = tools_window

        # groups with elements
        self.canvas_group = canvas_group
        self.temporary_group = temporary_group
        self.palette_group = palette_group
        self.predefined_shapes = {}

        # content
        self.position_tools_content = position_tools_content

        # variables
        self.reference_point = None

    def add_predefined_shape(self, shape_name, shape_group):
        if shape_name not in self.predefined_shapes:
            self.predefined_shapes[shape_name] = shape_group

    def predefined_shape_to_canvas(self, shape_name):
        """Insert predefined shape on the canvas.

        A copy of the predefined shape is created. This way the original doesn't get lost after transformations
        or deletion.

        Args:
            shape_name (Group): A predefined shape.
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

    def load_canvas(self):
        """Load elements and groups placed on the canvas.

        The canvas can handle only integer numbers, so all the entries are rounded before displaying them.
        If an entry turns out to be a group its elements are accessed and displayed in addition to the group center.

        Args:

        Returns:
            None
        """
        height, width = self.canvas_in.getmaxyx()

        self.canvas_in.clear()
        for el in self.canvas_group.elements:
            # elements out of the canvas are not displayed, yet they still exist
            if round(el.x) not in range(0, width) or round(el.y) not in range(0, height):
                continue
            self.canvas_in.addstr(round(el.y), round(el.x), el.symbol)

            try:
                for el_in in el.elements:
                    # group-elements out of the canvas are not displayed, yet they still exist
                    if round(el_in.x) not in range(0, width) or round(el_in.y) not in range(0, height):
                        continue
                    self.canvas_in.addstr(round(el_in.y), round(el_in.x), el_in.symbol)
                    self.canvas_in.addstr(round(el.y), round(el.x), el.symbol, curses.A_REVERSE)
            except AttributeError:
                pass
        self.canvas_in.refresh()

    def load_palette(self):
        for el in self.palette_group.elements:
            self.palette_in.addstr(el.y, el.x, el.symbol)
        self.palette_in.refresh()

    @staticmethod
    def navigate(window, on_five):
        """Navigate the canvas or the palette with initial elements.

        The navigation is required in multiple commands. It keeps the cursor within the window the user is navigating.

        Args:
            window (curses window): Window to navigate in.
            on_five (function): A function executed on pressing number five on the numpad. This function will receive
            the current cursor position as integer numbers.
        Returns:
            None
        """
        curses.noecho()
        curses.cbreak()
        height, width = window.getmaxyx()

        # place cursor closer to middle of the screen for faster navigation
        x, y = int(width / 3), int(height / 3)
        window.move(y, x)

        cursor_input = None
        while cursor_input != ord("7"):

            cursor_input = window.getch()
            if cursor_input == ord("4"):
                x -= 1
            elif cursor_input == ord("6"):
                x += 1
            elif cursor_input == ord("8"):
                y -= 1
            elif cursor_input == ord("2"):
                y += 1
            elif cursor_input == ord("5"):
                on_five(x, y)

            # prevent cursor from leaving the screen
            x = max(0, x)
            x = min(width - 1, x)
            y = max(0, y)
            y = min(height - 1, y)

            window.move(y, x)
            window.refresh()

    def highlight_tool(self, tool):
        content = self.position_tools_content[tool]
        self.tools_window.addstr(*content, curses.A_STANDOUT)
        self.tools_window.refresh()

    def play_down_tool(self, tool):
        content = self.position_tools_content[tool]
        self.tools_window.addstr(*content)
        self.tools_window.refresh()

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

        height, width = self.canvas_in.getmaxyx()

        for el in self.canvas_group.elements:
            if round(el.x) == x and round(el.y) == y:
                self.temporary_group.add(el)
                self.canvas_group.remove(el)
                self.canvas_in.addstr(y, x, el.symbol, curses.A_STANDOUT)
                try:
                    for el_in in el.elements:
                        # group-elements out of the canvas are not highlighted
                        if round(el_in.x) not in range(0, width) or round(el_in.y) not in range(0, height):
                            continue
                        self.canvas_in.addstr(round(el_in.y), round(el_in.x), el_in.symbol, curses.A_STANDOUT)
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
        for el in self.palette_group.elements:
            if el.x == x and el.y == y:
                if len(self.temporary_group.elements) != 0:
                    self.temporary_group.elements.clear()
                    self.load_palette()
                self.temporary_group.add(el)
                self.palette_in.addstr(y, x, el.symbol, curses.A_STANDOUT)

    def canvas_to_reference_point(self, x, y):
        """Marks amd remembers the reference point.

        Multiple attempts are possible, only the last one is valid.

        Args:
            x (int): Cursor position.
            y (int): Cursor position.
        Returns:
            None
        """
        if self.reference_point:
            self.load_canvas()
        self.reference_point = (x, y)
        self.canvas_in.addstr(y, x, "+", curses.A_STANDOUT)

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
        self.canvas_in.addstr(y, x, symbol, curses.A_STANDOUT)

    def add(self):
        """Adds elements to the canvas one by one.

        Allows navigation to a position, placement of elements on the canvas multiple times until interrupted
        by the user. Dynamic prompts and relevant highlighting guide the user.

        Args:

        Returns:
            None
        """
        self.highlight_tool("elements")

        # selection
        self.highlight_tool("select")

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Choose element! Navigate:NumLock arrows | Escape:Home | Select:5")
        self.prompt_in.refresh()

        self.navigate(self.palette_in, self.palette_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Place element! Navigate:NumLock arrows | Escape:Home | Place:5")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.new_el_to_canvas)

        self.temporary_group.elements.clear()

        self.load_canvas()
        self.load_palette()
        curses.beep()

        self.play_down_tool("elements")

    def delete(self):
        """Removes selected elements from the canvas.

        Allows navigation to a position, selection of elements on the canvas multiple times until interrupted
        by the user. The selected elements are automatically removed on exit from the command.
        Dynamic prompts and relevant highlighting guide the user.

        Args:

        Returns:
            None
        """
        self.highlight_tool("delete")

        # selection
        self.highlight_tool("select")

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, f"Choose element to delete! Navigate:NumLock arrows | Escape:Home "
                                    f"| Select:5")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.temporary_group.elements.clear()

        self.load_canvas()
        curses.beep()

        self.play_down_tool("delete")

    def move(self):
        """Moves selected elements and groups.

        Allows navigation to a position, selection of elements or groups on the canvas multiple times until interrupted
        by the user, entry of values for relative movement. The selected elements are automatically moved on exit from
        the command. Dynamic prompts and relevant highlighting guide the user.

        Args:

        Returns:
            None
        """
        self.highlight_tool("move")

        # selection
        self.highlight_tool("select")

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, f"Choose element! Navigate:NumLock arrows | Escape:Home | Select:5 | Deselect:-")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Enter delta-x and delta-y in the format '<value x>,<value y>'")
        self.prompt_in.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_in.getstr(0, 2).decode(encoding="utf-8")
        x, y = [int(n) for n in user_input.split(",")]

        move_elements = MoveCommand(self.temporary_group, x, y)
        move_elements.execute()

        self.temp_to_canvas()
        self.temporary_group.elements.clear()

        self.load_canvas()
        curses.beep()

        self.play_down_tool("move")

    def rotate(self):
        """Rotates selected elements and groups.

        Allows navigation to a position, selection of elements or groups on the canvas multiple times until interrupted
        by the user, entry of value for rotation in degrees. The selected elements are automatically rotated
        on exit from the command. Dynamic prompts and relevant highlighting guide the user.

        Args:

        Returns:
            None
        """
        self.highlight_tool("rotate")

        # selection
        self.highlight_tool("select")

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Select center of rotation! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.canvas_to_reference_point)

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Choose elements! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Enter angle of rotation in degrees in the format '<value>'.  "
                                    "Positive values: clockwise rotation")
        self.prompt_in.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_in.getstr(0, 2).decode(encoding="utf-8")
        theta = int(user_input)

        transformer.set_reference(*self.reference_point)
        rotate_elements = RotateCommand(self.temporary_group, theta)
        rotate_elements.execute()

        self.temp_to_canvas()
        self.temporary_group.elements.clear()
        self.reference_point = None

        self.load_canvas()
        curses.beep()

        self.play_down_tool("rotate")

    def mirror(self):
        """Mirrors selected elements and groups.

        Allows navigation to a position, selection of elements or groups on the canvas multiple times until interrupted
        by the user, entry of three possible mirror options. The selected elements are automatically mirrored
        on exit from the command. Dynamic prompts and relevant highlighting guide the user.

        Args:

        Returns:
            None
        """
        self.highlight_tool("mirror")

        # selection
        self.highlight_tool("select")

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Select reference point! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.canvas_to_reference_point)

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Choose elements! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Enter mirror direction in the format 'xy' or 'x' or 'y'")
        self.prompt_in.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_in.getstr(0, 2).decode(encoding="utf-8")
        direction = user_input

        transformer.set_reference(*self.reference_point)
        mirror_elements = MirrorCommand(self.temporary_group, direction)
        mirror_elements.execute()

        self.temp_to_canvas()
        self.temporary_group.elements.clear()
        self.reference_point = None

        self.load_canvas()
        curses.beep()

        self.play_down_tool("mirror")

    def scale(self):
        """Scale selected elements and groups.

        Allows navigation to a position, selection of elements or groups on the canvas multiple times until interrupted
        by the user, entry of scale values for x and y direction. The selected elements are automatically scaled
        on exit from the command. Dynamic prompts and relevant highlighting guide the user.

        Args:

        Returns:
            None
        """
        self.highlight_tool("scale")

        # selection
        self.highlight_tool("select")

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Select reference point! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.canvas_to_reference_point)

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Choose elements! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Enter scale-x and scale-y in the format '<value x>,<value y>'")
        self.prompt_in.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_in.getstr(0, 2).decode(encoding="utf-8")
        scale_x, scale_y = [int(n) for n in user_input.split(",")]

        transformer.set_reference(*self.reference_point)
        scale_elements = ScaleCommand(self.temporary_group, scale_x, scale_y)
        scale_elements.execute()

        self.temp_to_canvas()
        self.temporary_group.elements.clear()
        self.reference_point = None

        self.load_canvas()
        curses.beep()

        self.play_down_tool("scale")

    def insert_shape(self):
        """Insert predefined groups.

        Inserts one predefined shape per activation. The user is prompted to address the required shape by name
        from the listed names of the available shapes.

        Args:

        Returns:
            None
        """
        self.highlight_tool("insert")

        self.prompt_in.clear()
        available_shapes = ', '.join(shape_name for shape_name in self.predefined_shapes)
        self.prompt_in.addstr(0, 2, f"Chose a shape to insert: {available_shapes}")
        self.prompt_in.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_in.getstr(0, 2).decode(encoding="utf-8")

        self.predefined_shape_to_canvas(user_input)

        self.load_canvas()
        curses.beep()

        self.play_down_tool("insert")

    def clear(self):
        """Clears the canvas from all elements and groups.

        Args:

        Returns:
            None
        """
        self.highlight_tool("clear")

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Clear canvas? y/n")
        self.prompt_in.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_in.getstr(0, 2).decode(encoding="utf-8")

        if user_input == "y":
            self.canvas_group.elements.clear()

        self.load_canvas()
        curses.beep()

        self.play_down_tool("clear")
