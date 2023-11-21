import curses

from abc import ABC, abstractmethod


class WindowABC(ABC):

    @abstractmethod
    def position_content(self):
        raise NotImplemented

    @abstractmethod
    def create(self):
        raise NotImplemented


class MenuWindow(WindowABC):

    def __init__(self, width, nlines=3):

        self.nlines = nlines
        self.ncols = width
        self.begin_x = 0
        self.begin_y = 0

        self.window = None

    def position_content(self):

        window_content = {
            "undo": (1, 2, "<Undo"),
            "redo": (1, 9, "Redo>"),
            "save": (1, 20, "Save"),
            "load": (1, 27, "Load"),
            "help": (1, 34, "Help"),
            "about": (1, 41, "About"),
            "donate": (1, 49, "Donate"),
            "Quit": (1, self.ncols - 6, "Quit")
        }

        return window_content

    def create(self):

        self.window = curses.newwin(self.nlines, self.ncols, self.begin_y, self.begin_x)

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        return self.window


class ToolsWindow(WindowABC):

    def __init__(self, height, menu_window_nlines=3, ncols=15):
        self.nlines = height - (menu_window_nlines - 1)
        self.ncols = ncols
        self.begin_x = 0
        self.begin_y = menu_window_nlines - 1

        self.window = None

    def position_content(self):

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
        self.window = curses.newwin(self.nlines, self.ncols, self.begin_y, self.begin_x)

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        return self.window


class InputWindow(WindowABC):

    def __init__(self, width, height, input_window_nlines=3, tools_window_ncols=15):
        self.nlines = input_window_nlines
        self.ncols = width - (tools_window_ncols - 1)
        self.begin_x = tools_window_ncols - 1
        self.begin_y = height - input_window_nlines

        self.window = None

    def position_content(self):
        input_window_content = {"header": (0, 6, "Input")}
        return input_window_content

    def create(self):
        self.window = curses.newwin(self.nlines, self.ncols, self.begin_y, self.begin_x)

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        return self.window


class PromptWindow(WindowABC):

    def __init__(self, width, height, prompt_window_nlines=3, tools_window_ncols=15, input_window_nlines=3):
        self.nlines = prompt_window_nlines
        self.ncols = width - (tools_window_ncols - 1)
        self.begin_x = tools_window_ncols - 1
        self.begin_y = height - input_window_nlines - 2

        self.window = None

    def position_content(self):
        window_content = {"header": (0, 6, "Prompt")}
        return window_content

    def create(self):
        self.window = curses.newwin(self.nlines, self.ncols, self.begin_y, self.begin_x)

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        return self.window


class RulerWindow(WindowABC):

    def __init__(self, width, height):
        self.nlines = height - ((3 - 1) + (3 - 1)) - (3 - 1)
        self.ncols = width - (15 - 1)
        self.begin_x = 15 - 1
        self.begin_y = 3 - 1

        self.window = None

    def position_content(self):
        """Define/calculate positions for window content

        Dependent on available space different size of content is generated. The rulers always have the
        coordinate axes annotated at the end.

        Returns:
            Dictionary with content and its positions
        """
        ruler_window_content = {}

        for c in range(0, self.ncols - 12, 5):
            number = str(c)
            content = (1, c + 6, number)
            ruler_window_content[f"ncols-{c}"] = content

        for r in range(0, self.nlines - 6, 1):
            number = str(r)
            content = (r + 3, 2, number)
            ruler_window_content[f"nlines-{r}"] = content

        ruler_window_content["X"] = (1, self.ncols - 4, "X")
        ruler_window_content["Y"] = (self.nlines - 3, 2, "Y")

        return ruler_window_content

    def create(self):
        self.window = curses.newwin(self.nlines, self.ncols, self.begin_y, self.begin_x)

        # content is placed at the corresponding coordinates
        window_content = self.position_content()
        for value in window_content.values():
            self.window.addstr(*value)

        # arrow characters are added after the window creation
        self.window.addch(1, self.ncols - 3, curses.ACS_RARROW)
        self.window.addch(self.nlines - 2, 2, curses.ACS_DARROW)

        return self.window


class CanvasWindow(WindowABC):
    def __init__(self):
        self.canvas_nlines = self.ruler_nlines - 2
        self.canvas_ncols = self.ruler_ncols - 5
        self.canvas_begin_x = self.ruler_begin_x + 5
        self.canvas_begin_y = self.ruler_begin_y + 2