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

    def __init__(self, height, menu_window_nlines, ncols=15):
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

