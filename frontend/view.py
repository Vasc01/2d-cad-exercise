import curses
from abc import abstractmethod, ABC
from frontend.presenter import Presenter
from frontend.window import MenuWindow, ToolsWindow, InputWindow, PromptWindow, RulerWindow, CanvasWindow, \
    CanvasInnerWindow, InputInnerWindow, PromptInnerWindow, PaletteInnerWindow
from frontend.initial_data import (canvas_group, temporary_group, palette_group, predefined_square,
                                   predefined_z_shape, predefined_smiley)


class ViewABC(ABC):

    @abstractmethod
    def update_ui(self, window, data):
        raise NotImplemented

    @abstractmethod
    def run_main_loop(self):
        raise NotImplemented


class View(ViewABC):

    def __init__(self):
        self.presenter = Presenter(self)

        # available terminal space
        # self.ncols = 0
        # self.nlines = 0
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
        # content
        self.tools_window_content = None
        # variables
        self.reference_point = None

# -------------------MVP--------------------------------------------------------

    def update_ui(self, update_window, entries):
        # functions loading and updating windows from tuples/lists with data

        # check which window is the data ment for
        window = None
        if update_window == "canvas":
            window = self.canvas_inner_window
        elif update_window == "palette":
            window = self.palette_inner_window

        # unpack component representation
        for entry in entries:
            y, x, symbol, *args = entry

            # if received data has additional parameter for highlighting
            parameter = None
            if args:
                if args[0] == "standout":
                    parameter = curses.A_STANDOUT
                elif args[0] == "reverse":
                    parameter = curses.A_REVERSE
                self.add_string(window, y, x, symbol, parameter=parameter)

            # if received data has NO parameter for highlighting
            else:
                self.add_string(window, y, x, symbol)
        window.refresh()

    @staticmethod
    def add_string(window, y, x, symbol, parameter=None):
        """Input verification to avoid software crash.
            Only round numbers are accepted by curses.
            Only entries within the canvas are acceptable
        """
        height, width = window.getmaxyx()

        if parameter:
            if round(x) in range(0, width) or round(y) in range(0, height):
                window.addstr(round(y), round(x), symbol, parameter)

        else:
            if round(x) in range(0, width) or round(y) in range(0, height):
                window.addstr(round(y), round(x), symbol)

# ------------------------------------------------------------------------------
    def highlight_tool(self, tool):
        content = self.tools_window_content[tool]
        self.tools_window.addstr(*content, curses.A_STANDOUT)
        self.tools_window.refresh()

    def play_down_tool(self, tool):
        content = self.tools_window_content[tool]
        self.tools_window.addstr(*content)
        self.tools_window.refresh()

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
            self.load_canvas_view()
        self.reference_point = (x, y)
        self.canvas_inner_window.addstr(y, x, "+", curses.A_STANDOUT)

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

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Choose element! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.palette_inner_window, self.presenter.palette_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Place element! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.canvas_inner_window, self.presenter.new_el_to_canvas)

        self.presenter.temporary_group.elements.clear()

        # loading canvas and palette clears highlights
        self.presenter.load_canvas_view()
        self.presenter.load_palette_view()
        curses.beep()

        self.play_down_tool("elements")

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
        self.tools_window_content = ToolsWindow(height).position_content()
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
        self.presenter.load_palette_view()
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

        # wrapper sets up the terminal for the program
        # when the program is closed wrapper restores the default terminal settings
        curses.wrapper(self.create_main_loop)
