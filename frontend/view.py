import curses
from abc import abstractmethod, ABC
from frontend.presenter import Presenter
from frontend.window import MenuWindow, ToolsWindow, InputWindow, PromptWindow, RulerWindow, CanvasWindow, \
    CanvasInnerWindow, InputInnerWindow, PromptInnerWindow, PaletteInnerWindow
from frontend.initial_data import (canvas_group, temporary_group, palette_group, predefined_square,
                                   predefined_z_shape, predefined_smiley)


class ViewABC(ABC):

    @abstractmethod
    def send_user_input(self):
        raise NotImplemented

    @abstractmethod
    def update_ui(self, window, data):
        raise NotImplemented


class View(ViewABC):

    def __init__(self):
        self.presenter = Presenter(self)

        # available terminal space
        self.ncols = 0
        self.nlines = 0
        # windows
        self.menu_window = None
        self.tools_window = None
        self.ruler_window = None
        self.canvas_window = None
        self.prompt_window = None
        self.input_window = None
        # inner windows
        self.palette_inner_window = None
        self.canvas_inner_window = None
        self.prompt_inner_window = None
        self.input_inner_window = None

# ------------------------------------------------------------------------------

    def send_user_input(self):
        raise NotImplemented
    #     # sends the user choice from the while loop to presenter if choice is correct

    def update_ui(self, update_window, entries):
        # functions loading and updating windows from tuples/lists with data

        # unpacking of the received update
        window = None
        if update_window == "canvas":
            window = self.canvas_inner_window
        elif update_window == "palette":
            window = self.palette_inner_window
        for entry in entries:
            y, x, symbol, *args = entry
            if args:
                window.addstr(y, x, symbol, *args)
            window.addstr(y, x, symbol)
        window.refresh()

# ------------------------------------------------------------------------------

    def load_canvas(self):
        raise NotImplemented

    def add(self):
        raise NotImplemented

    def delete(self):
        raise NotImplemented

    def move(self):
        raise NotImplemented

    def rotate(self):
        raise NotImplemented

    def mirror(self):
        raise NotImplemented

    def scale(self):
        raise NotImplemented

    def insert_shape(self):
        raise NotImplemented

    def clear(self):
        raise NotImplemented

    def initiate_windows(self, height, width):
        # windows
        self.menu_window = MenuWindow(width).create()
        self.tools_window = ToolsWindow(height).create()
        self.ruler_window = RulerWindow(height, width).create()
        self.canvas_window = CanvasWindow(height, width).create()
        self.prompt_window = PromptWindow(height, width).create()
        self.input_window = InputWindow(height, width).create()
        # inner windows
        self.palette_inner_window = PaletteInnerWindow().create()
        canvas_height, canvas_width = self.canvas_window.getmaxyx()
        self.canvas_inner_window = CanvasInnerWindow(canvas_height, canvas_width).create()
        prompt_nlines, prompt_ncols = self.prompt_window.getmaxyx()
        self.prompt_inner_window = PromptInnerWindow(prompt_nlines, prompt_ncols, height).create()
        input_height, input_width = self.input_window.getmaxyx()
        self.input_inner_window = InputInnerWindow(input_height, input_width, height).create()

    def create_main_loop(self, stdscr):

        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # create windows
        self.initiate_windows(height, width)

        # set content
        self.presenter.set_palette_group(palette_group)
        self.presenter.set_canvas_group(canvas_group)
        self.presenter.set_temporary_group(temporary_group)
        self.presenter.add_predefined_shape("square", predefined_square)
        self.presenter.add_predefined_shape("z-shape", predefined_z_shape)
        self.presenter.add_predefined_shape("smiley", predefined_smiley)

        # load content
        self.presenter.load_palette()
        # presenter.load_canvas()

        # loop during use and wait for command
        user_input = None
        while user_input != "q":

            self.input_inner_window.clear()
            self.input_inner_window.refresh()

            self.prompt_inner_window.clear()
            self.prompt_inner_window.addstr(0, 2, "Choose a command. Use keyboard shortcuts.")
            self.prompt_inner_window.refresh()

            if user_input == "a":
                self.add()
            elif user_input == "d":
                self.delete()
            elif user_input == "m":
                self.move()
            elif user_input == "r":
                self.rotate()
            elif user_input == "mi":
                self.mirror()
            elif user_input == "s":
                self.scale()
            elif user_input == "i":
                self.insert_shape()
            elif user_input == "c":
                self.clear()

            self.input_inner_window.clear()
            self.input_inner_window.refresh()

            self.prompt_inner_window.clear()
            self.prompt_inner_window.addstr(0, 2, "Choose a command. Use keyboard shortcuts.")
            self.prompt_inner_window.refresh()

            # new command input
            curses.echo()
            curses.nocbreak()
            user_input = self.input_inner_window.getstr(0, 2).decode(encoding="utf-8")

    def run_main_loop(self):
        # ui_execution
        curses.wrapper(self.create_main_loop)