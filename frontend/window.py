"""Division of the screen in sub windows.

This module deals with the size of the sub windows and their content.
"""

import curses
from abc import ABC, abstractmethod


class WindowABC(ABC):

    @abstractmethod
    def create(self):
        raise NotImplemented


class WindowCalculator:
    """Calculate the screen split in sub windows.

    The size of the terminal affects the sizes of the sub windows. Here the correct dimensions are calculated
    for further use by the separate windows.


    Attributes:
        width (int): Number of available characters in the terminal horizontally.
        height (int): Number of available characters in the terminal vertically.
        ...

        For the creation of a window curses requires four attributes:
        - number of lines, size of the window vertically.
        - number of columns, size of the window horizontally.
        - horizontal position of top left corner for the window.
        - vertical position of top left corner for the window.
        These attributes are defined here for each window of the user interface.
    """
    def __init__(self):

        self.height = None
        self.width = None

        self.menu_nlines = 0
        self.menu_ncols = 0
        self.menu_begin_x = 0
        self.menu_begin_y = 0

        self.tools_nlines = 0
        self.tools_ncols = 0
        self.tools_begin_x = 0
        self.tools_begin_y = 0

        self.input_nlines = 0
        self.input_ncols = 0
        self.input_begin_x = 0
        self.input_begin_y = 0

        self.prompt_nlines = 0
        self.prompt_ncols = 0
        self.prompt_begin_x = 0
        self.prompt_begin_y = 0

        self.ruler_nlines = 0
        self.ruler_ncols = 0
        self.ruler_begin_x = 0
        self.ruler_begin_y = 0

        self.canvas_nlines = 0
        self.canvas_ncols = 0
        self.canvas_begin_x = 0
        self.canvas_begin_y = 0

        # inner windows
        self.canvas_in_nlines = 0
        self.canvas_in_ncols = 0
        self.canvas_in_begin_x = 0
        self.canvas_in_begin_y = 0

        self.input_in_nlines = 0
        self.input_in_ncols = 0
        self.input_in_begin_x = 0
        self.input_in_begin_y = 0

        self.prompt_in_nlines = 0
        self.prompt_in_ncols = 0
        self.prompt_in_begin_x = 0
        self.prompt_in_begin_y = 0

        self.palette_in_nlines = 0
        self.palette_in_ncols = 0
        self.palette_in_begin_x = 0
        self.palette_in_begin_y = 0

    def set_max_size(self, height, width):
        """Sets size of available space received from the terminal.

        Args:
            height (int): Height of terminal space.
            width (int): Width of terminal space.

        Returns:
            None
        """
        self.height = height
        self.width = width

    # define window sizes and positions
    def calculate_split(self, menu_window_nlines=3, tools_window_ncols=15, input_window_nlines=3,
                        prompt_window_nlines=3):
        """Calculates and sets sizes and starting points for all sub windows.

        Only view parameters are preset including tje zero-zero corner of the screen.
        The rest is calculated out of these parameters.

        Args:
            menu_window_nlines (int): Height of menu window.
            tools_window_ncols (int): Width of tools window.
            input_window_nlines (int): Height of input window.
            prompt_window_nlines (int): Height of prompt window.

        Returns:
            None
        """
        self.menu_nlines = menu_window_nlines
        self.menu_ncols = self.width
        self.menu_begin_x = 0
        self.menu_begin_y = 0

        self.tools_nlines = self.height - (self.menu_nlines - 1)
        self.tools_ncols = tools_window_ncols
        self.tools_begin_x = 0
        self.tools_begin_y = self.menu_nlines - 1

        self.input_nlines = input_window_nlines
        self.input_ncols = self.width - (self.tools_ncols - 1)
        self.input_begin_x = self.tools_ncols - 1
        self.input_begin_y = self.height - 3

        self.prompt_nlines = prompt_window_nlines
        self.prompt_ncols = self.width - (self.tools_ncols - 1)
        self.prompt_begin_x = self.tools_ncols - 1
        self.prompt_begin_y = self.input_begin_y - 2

        self.ruler_nlines = self.height - ((self.prompt_nlines - 1) + (self.input_nlines - 1)) - (self.menu_nlines - 1)
        self.ruler_ncols = self.width - (self.tools_ncols - 1)
        self.ruler_begin_x = self.tools_ncols - 1
        self.ruler_begin_y = self.menu_nlines - 1

        self.canvas_nlines = self.ruler_nlines - 2
        self.canvas_ncols = self.ruler_ncols - 5
        self.canvas_begin_x = self.ruler_begin_x + 5
        self.canvas_begin_y = self.ruler_begin_y + 2

        # inner windows
        self.canvas_in_nlines = self.canvas_nlines - 2
        self.canvas_in_ncols = self.canvas_ncols - 2
        self.canvas_in_begin_x = self.canvas_begin_x + 1
        self.canvas_in_begin_y = self.canvas_begin_y + 1

        self.input_in_nlines = self.input_nlines - 2
        self.input_in_ncols = self.input_ncols - 2
        self.input_in_begin_x = self.input_begin_x + 1
        self.input_in_begin_y = self.input_begin_y + 1

        self.prompt_in_nlines = self.prompt_nlines - 2
        self.prompt_in_ncols = self.prompt_ncols - 2
        self.prompt_in_begin_x = self.prompt_begin_x + 1
        self.prompt_in_begin_y = self.prompt_begin_y + 1

        self.palette_in_nlines = 2
        self.palette_in_ncols = self.tools_ncols - 4
        self.palette_in_begin_x = self.tools_begin_x + 2
        self.palette_in_begin_y = self.tools_begin_y + 2


class MenuWindow(WindowABC):
    """Creates the menu window and its content.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """
    def __init__(self, window_calculator):

        self.window_calculator = window_calculator
        self.window = None

    def position_content(self):
        """Contains dictionary with content and corresponding coordinates.

        Returns:
            Dictionary with content and corresponding coordinates.
        """

        window_content = {
            "undo": (1, 2, "<Undo"),
            "redo": (1, 9, "Redo>"),
            "save": (1, 20, "Save"),
            "load": (1, 27, "Load"),
            "help": (1, 34, "Help"),
            "about": (1, 41, "About"),
            "donate": (1, 49, "Donate"),
            "Quit": (1, self.window_calculator.menu_ncols - 6, "Quit")
        }

        return window_content

    def create(self):
        """Creates curses window and places content in it.

        Returns:
            Newly created curses window with content.
        """

        self.window = curses.newwin(self.window_calculator.menu_nlines,
                                    self.window_calculator.menu_ncols,
                                    self.window_calculator.menu_begin_y,
                                    self.window_calculator.menu_begin_x)
        self.window.border()

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        self.window.refresh()
        return self.window


class ToolsWindow(WindowABC):
    """Creates the tools window and its content.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """

    def __init__(self, window_calculator):

        self.window_calculator = window_calculator
        self.window = None

    def position_content(self):
        """Contains dictionary with content and corresponding coordinates.

        Returns:
            Dictionary with content and corresponding coordinates.
        """

        window_content = {
            "elements": (1, 2, "Add Element"),
            "delete": (4, 2, "Del Element"),
            "insert": (5, 2, "Insert Shape"),
            "clear": (6, 2, "Clear All"),
            "select": (8, 2, "Select Mode"),
            "move": (10, 2, "Move"),
            "rotate": (11, 2, "Rotate"),
            "mirror": (12, 2, "MIrror"),
            "scale": (13, 2, "Scale"),
            "fill": (15, 2, "Fill"),
            "union": (16, 2, "Union"),
            "difference": (17, 2, "Difference"),
            "split": (18, 2, "Split")
        }
        return window_content

    def create(self):
        """Creates curses window and places content in it.

        Returns:
            Newly created curses window with content.
        """

        self.window = curses.newwin(self.window_calculator.tools_nlines,
                                    self.window_calculator.tools_ncols,
                                    self.window_calculator.tools_begin_y,
                                    self.window_calculator.tools_begin_x)
        self.window.border()

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        self.window.refresh()
        return self.window


class InputWindow(WindowABC):
    """Creates the input window and its content.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """

    def __init__(self, window_calculator):

        self.window_calculator = window_calculator
        self.window = None

    def position_content(self):
        """Contains dictionary with content and corresponding coordinates.

        Returns:
            Dictionary with content and corresponding coordinates.
        """

        input_window_content = {"header": (0, 6, "Input")}
        return input_window_content

    def create(self):
        """Creates curses window and places content in it.

        Returns:
            Newly created curses window with content.
        """
        self.window = curses.newwin(self.window_calculator.input_nlines,
                                    self.window_calculator.input_ncols,
                                    self.window_calculator.input_begin_y,
                                    self.window_calculator.input_begin_x)
        self.window.border()

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        self.window.refresh()
        return self.window


class PromptWindow(WindowABC):
    """Creates the prompt window and its content.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """

    def __init__(self, window_calculator):

        self.window_calculator = window_calculator
        self.window = None

    def position_content(self):
        """Contains dictionary with content and corresponding coordinates.

        Returns:
            Dictionary with content and corresponding coordinates.
        """
        window_content = {"header": (0, 6, "Prompt")}
        return window_content

    def create(self):
        """Creates curses window and places content in it.

        Returns:
            Newly created curses window with content.
        """
        self.window = curses.newwin(self.window_calculator.prompt_nlines,
                                    self.window_calculator.prompt_ncols,
                                    self.window_calculator.prompt_begin_y,
                                    self.window_calculator.prompt_begin_x)
        self.window.border()

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        self.window.refresh()
        return self.window


class RulerWindow(WindowABC):
    """Creates the ruler window and its content.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """

    def __init__(self, window_calculator):

        self.window_calculator = window_calculator
        self.window = None

    def position_content(self):
        """Define/calculate positions for window content.

        Dependent on available space different size of content is generated. The rulers always have the
        coordinate axes annotated at the end.

        Returns:
            Dictionary with content and its positions.
        """
        window_content = {}

        for c in range(0, self.window_calculator.ruler_ncols - 12, 5):
            number = str(c)
            content = (1, c + 6, number)
            window_content[f"ncols-{c}"] = content

        for r in range(0, self.window_calculator.ruler_nlines - 6, 1):
            number = str(r)
            content = (r + 3, 2, number)
            window_content[f"nlines-{r}"] = content

        window_content["X"] = (1, self.window_calculator.ruler_ncols - 4, "X")
        window_content["Y"] = (self.window_calculator.ruler_nlines - 3, 2, "Y")

        return window_content

    def create(self):
        """Creates curses window and places content in it.

        Returns:
            Newly created curses window with content.
        """
        self.window = curses.newwin(self.window_calculator.ruler_nlines,
                                    self.window_calculator.ruler_ncols,
                                    self.window_calculator.ruler_begin_y,
                                    self.window_calculator.ruler_begin_x)
        self.window.border()

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        # arrow characters are added after the window creation
        self.window.addch(1, self.window_calculator.ruler_ncols - 3, curses.ACS_RARROW)
        self.window.addch(self.window_calculator.ruler_nlines - 2, 2, curses.ACS_DARROW)

        self.window.refresh()
        return self.window


class CanvasWindow(WindowABC):
    """Creates the canvas window and its content.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """

    def __init__(self, window_calculator):
        self.window_calculator = window_calculator

        self.window = None

    def position_content(self):
        """Contains dictionary with content and corresponding coordinates.

        Returns:
            Dictionary with content and corresponding coordinates.
        """
        window_content = {"header": (0, 1, "Canvas")}
        return window_content

    def create(self):
        """Creates curses window and places content in it.

        Returns:
            Newly created curses window with content.
        """
        self.window = curses.newwin(self.window_calculator.canvas_nlines,
                                    self.window_calculator.canvas_ncols,
                                    self.window_calculator.canvas_begin_y,
                                    self.window_calculator.canvas_begin_x)
        self.window.border()

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        self.window.refresh()
        return self.window


class CanvasInnerWindow(WindowABC):
    """Creates the canvas inner window.

    It is used to display dynamic information and be able to delete it without
    disturbing the frames and content defined by other windows.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """

    def __init__(self, window_calculator):

        self.window_calculator = window_calculator
        self.window = None

    def create(self):
        """Creates curses window.

        Returns:
            Newly created curses window.
        """
        self.window = curses.newwin(self.window_calculator.canvas_in_nlines,
                                    self.window_calculator.canvas_in_ncols,
                                    self.window_calculator.canvas_in_begin_y,
                                    self.window_calculator.canvas_in_begin_x)

        return self.window


class InputInnerWindow(WindowABC):
    """Creates the input inner window.

    It is used to display dynamic information and be able to delete it without
    disturbing the frames and content defined by other windows.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """

    def __init__(self, window_calculator):

        self.window_calculator = window_calculator
        self.window = None

    def create(self):
        """Creates curses window.

        Returns:
            Newly created curses window.
        """
        self.window = curses.newwin(self.window_calculator.input_in_nlines,
                                    self.window_calculator.input_in_ncols,
                                    self.window_calculator.input_in_begin_y,
                                    self.window_calculator.input_in_begin_x)

        return self.window


class PromptInnerWindow(WindowABC):
    """Creates the prompt inner window.

    It is used to display dynamic information and be able to delete it without
    disturbing the frames and content defined by other windows.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """

    def __init__(self, window_calculator):

        self.window_calculator = window_calculator
        self.window = None

    def create(self):
        """Creates curses window.

        Returns:
            Newly created curses window.
        """
        self.window = curses.newwin(self.window_calculator.prompt_in_nlines,
                                    self.window_calculator.prompt_in_ncols,
                                    self.window_calculator.prompt_in_begin_y,
                                    self.window_calculator.prompt_in_begin_x)

        return self.window


class PaletteInnerWindow(WindowABC):
    """Creates the palette inner window.

    It is used to display dynamic information and be able to delete it without
    disturbing the frames and content defined by other windows.

    Attributes:
        window_calculator (WindowCalculator): Makes calculated values for window size and position available.
        window (curses window object): Newly created curses window for use in the user interface.
    """
    def __init__(self, window_calculator):

        self.window_calculator = window_calculator
        self.window = None

    def create(self):
        """Creates curses window.

         Returns:
             Newly created curses window.
         """
        self.window = curses.newwin(self.window_calculator.palette_in_nlines,
                                    self.window_calculator.palette_in_ncols,
                                    self.window_calculator.palette_in_begin_y,
                                    self.window_calculator.palette_in_begin_x)

        return self.window
