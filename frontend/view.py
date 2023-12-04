"""Handle the frontend interactivity.

The frontend has complex behavior to provide interactive experience. This module implements the behavior.
"""
import curses
from abc import abstractmethod, ABC

from frontend.presenter import Presenter
from frontend.window import MenuWindow, ToolsWindow, InputWindow, PromptWindow, RulerWindow, CanvasWindow, \
    CanvasInnerWindow, InputInnerWindow, PromptInnerWindow, PaletteInnerWindow, WindowCalculator
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
    """Contains all the functionalities for the frontend.

    This class initiates the creation of the user interface, initiates the predefined data,
    and awaits user input.
    It also creates the presenter object that handles the connection to the backend.

    Attributes:
        menu_window (None/curses window): Menu window.
        tools_window (None/curses window): Tools window.
        ruler_window (None/curses window) = Ruler in x and y direction.
        canvas_window (None/curses window) = Frame for canvas_inner_window.
        prompt_window (None/curses window) = Frame for prompt_inner_window.
        input_window (None/curses window) = Frame for input_inner_window.

        palette_inner_window (None/curses window) = Display of available drawing elements.
        canvas_inner_window (None/curses window) = Main drawing window.
        prompt_inner_window (None/curses window) = Information and prompt messages appear here.
        input_inner_window (None/curses window) = Captures user input.

        tools_window_content (dict): Makes the content available for highlighting.
        reference_point (None/tuple): Contains the reference point coordinates.
    """

    def __init__(self):
        self.presenter = Presenter(self)

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

# -------------------MVP-part---------------------------------------------------

    def update_ui(self, update_window, entries):
        """ Receives information prom the presenter ready to be displayed.
        Parameters:
            update_window (curses window): window to receive the update.
            entries: (list): update data.
        Returns:
            None
        """

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

        Only integer numbers are accepted by curses.
        Only entries within the canvas are acceptable.

        Args:
            window (curses window): Used to determine available space for placing elements on the screen.
            x (int/float): Element position in x direction.
            y (int/float): Element position in y direction.
            symbol (str): Element symbol to be placed on canvas.
            parameter (curses command): Highlight or Reverse displayed symbol.
        """
        height, width = window.getmaxyx()

        if parameter:
            if round(x) in range(0, width) and round(y) in range(0, height):
                window.addstr(round(y), round(x), symbol, parameter)

        else:
            if round(x) in range(0, width) and round(y) in range(0, height):
                window.addstr(round(y), round(x), symbol)

# ------------------------------------------------------------------------------

    def highlight_tool(self, tool):
        """Highlights content in the tools window.
        Args:
            tool (string): A key to call content from the tool window entries.
        """
        content = self.tools_window_content[tool]
        self.tools_window.addstr(*content, curses.A_STANDOUT)
        self.tools_window.refresh()

    def play_down_tool(self, tool):
        """Removes highlight from content in the tools window.
        Args:
            tool (string): A key to call content from the tool window entries.
        """
        content = self.tools_window_content[tool]
        self.tools_window.addstr(*content)
        self.tools_window.refresh()

    def canvas_to_reference_point(self, x, y):
        """Marks and remembers the reference point.

        Multiple attempts are possible, only the last one is valid.

        Args:
            x (int): Cursor position.
            y (int): Cursor position.
        Returns:
            None
        """
        if self.reference_point:
            self.canvas_inner_window.clear()
            self.presenter.load_canvas_view()
            self.canvas_inner_window.refresh()
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
        """Removes selected elements from the canvas.

        Allows navigation to a position, selection of elements on the canvas multiple times until interrupted
        by the user. The selected elements are automatically removed on exit from the command.
        Dynamic prompts and relevant highlighting guide the user.

        Args:

        Returns:
            None
        """
        self.highlight_tool("delete")

        # start of selection
        self.highlight_tool("select")

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, f"Choose element to delete! Navigate:NumLock arrows"
                                              f" | Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.canvas_inner_window, self.presenter.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.presenter.temporary_group.elements.clear()

        self.canvas_inner_window.clear()
        self.presenter.load_canvas_view()
        self.canvas_inner_window.refresh()

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

        # start of selection
        self.highlight_tool("select")

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, f"Choose element! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.canvas_inner_window, self.presenter.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Enter delta-x and delta-y in the format '<value x>,<value y>'")
        self.prompt_inner_window.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_inner_window.getstr(0, 2).decode(encoding="utf-8")
        x, y = [int(n) for n in user_input.split(",")]

        # send user input to presenter
        movement = (x, y)
        self.presenter.receive_user_input(self.presenter.temporary_group, "move", movement)

        self.presenter.temp_to_canvas()
        self.presenter.temporary_group.elements.clear()

        self.canvas_inner_window.clear()
        self.presenter.load_canvas_view()
        self.canvas_inner_window.refresh()
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

        # start of selection
        self.highlight_tool("select")

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Select center of rotation! Navigate:NumLock arrows"
                                              " | Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.canvas_inner_window, self.canvas_to_reference_point)

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Choose elements! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.canvas_inner_window, self.presenter.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Enter angle of rotation in degrees in the format '<value>'.  "
                                              "Positive values: clockwise rotation")
        self.prompt_inner_window.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_inner_window.getstr(0, 2).decode(encoding="utf-8")
        theta = int(user_input)

        rotation_values = (theta, self.reference_point)
        self.presenter.receive_user_input(self.presenter.temporary_group, "rotate", rotation_values)

        self.presenter.temp_to_canvas()
        self.presenter.temporary_group.elements.clear()
        self.reference_point = None

        self.canvas_inner_window.clear()
        self.presenter.load_canvas_view()
        self.canvas_inner_window.refresh()
        curses.beep()

        self.play_down_tool("rotate")

    def mirror(self):
        """Mirrors selected elements and groups.

        Allows navigation to a position, selection of elements or groups on the canvas multiple times
        until interrupted
        by the user, entry of three possible mirror options. The selected elements are automatically mirrored
        on exit from the command. Dynamic prompts and relevant highlighting guide the user.

        Args:

        Returns:
            None
        """
        self.highlight_tool("mirror")

        # selection
        self.highlight_tool("select")

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Select reference point! Navigate:NumLock arrows "
                                              "| Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.canvas_inner_window, self.canvas_to_reference_point)

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Choose elements! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.canvas_inner_window, self.presenter.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Enter mirror direction in the format 'xy' or 'x' or 'y'")
        self.prompt_inner_window.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_inner_window.getstr(0, 2).decode(encoding="utf-8")
        direction = user_input

        mirror_values = (direction, self.reference_point)
        self.presenter.receive_user_input(self.presenter.temporary_group, "mirror", mirror_values)

        self.presenter.temp_to_canvas()
        self.presenter.temporary_group.elements.clear()
        self.reference_point = None

        self.canvas_inner_window.clear()
        self.presenter.load_canvas_view()
        self.canvas_inner_window.refresh()
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

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Select reference point! Navigate:NumLock arrows "
                                              "| Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.canvas_inner_window, self.canvas_to_reference_point)

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Choose elements! Navigate:NumLock arrows | Select:5 | Escape:Home")
        self.prompt_inner_window.refresh()

        self.navigate(self.canvas_inner_window, self.presenter.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Enter scale-x and scale-y in the format '<value x>,<value y>'")
        self.prompt_inner_window.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_inner_window.getstr(0, 2).decode(encoding="utf-8")
        scale_x, scale_y = [int(n) for n in user_input.split(",")]

        scale_values = (scale_x, scale_y, self.reference_point)
        self.presenter.receive_user_input(self.presenter.temporary_group, "scale", scale_values)

        self.presenter.temp_to_canvas()
        self.presenter.temporary_group.elements.clear()
        self.reference_point = None

        self.canvas_inner_window.clear()
        self.presenter.load_canvas_view()
        self.canvas_inner_window.refresh()
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

        self.prompt_inner_window.clear()
        available_shapes = ', '.join(shape_name for shape_name in self.presenter.predefined_shapes)
        self.prompt_inner_window.addstr(0, 2, f"Chose a shape to insert: {available_shapes}")
        self.prompt_inner_window.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_inner_window.getstr(0, 2).decode(encoding="utf-8")

        self.presenter.predefined_shape_to_canvas(user_input)

        self.canvas_inner_window.clear()
        self.presenter.load_canvas_view()
        self.canvas_inner_window.refresh()
        curses.beep()

        self.play_down_tool("insert")

    def clear(self):
        """Clears the canvas from all elements and groups.

        Args:

        Returns:
            None
        """
        self.highlight_tool("clear")

        self.prompt_inner_window.clear()
        self.prompt_inner_window.addstr(0, 2, "Clear canvas? y/n")
        self.prompt_inner_window.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_inner_window.getstr(0, 2).decode(encoding="utf-8")

        if user_input == "y":
            self.presenter.canvas_group.elements.clear()

        self.canvas_inner_window.clear()
        self.presenter.load_canvas_view()
        self.canvas_inner_window.refresh()
        curses.beep()

        self.play_down_tool("clear")

    def initiate_windows(self, height, width):
        """Creates all sub windows.

        Args:
            height (int): Available vertical space.
            width (int): Available horizontal space.
        Returns:
            None
        """
        # calculates window sizes based on the available pixels in the terminal
        window_calculator = WindowCalculator()
        window_calculator.set_max_size(height, width)
        window_calculator.calculate_split()

        # windows
        self.menu_window = MenuWindow(window_calculator).create()
        self.tools_window = ToolsWindow(window_calculator).create()
        self.tools_window_content = ToolsWindow(window_calculator).position_content()
        self.ruler_window = RulerWindow(window_calculator).create()
        self.canvas_window = CanvasWindow(window_calculator).create()
        self.prompt_window = PromptWindow(window_calculator).create()
        self.input_window = InputWindow(window_calculator).create()

        # inner windows
        self.palette_inner_window = PaletteInnerWindow(window_calculator).create()
        self.canvas_inner_window = CanvasInnerWindow(window_calculator).create()
        self.prompt_inner_window = PromptInnerWindow(window_calculator).create()
        self.input_inner_window = InputInnerWindow(window_calculator).create()

    def create_main_loop(self, stdscr):
        """Initiates windows creation, loads data, waits for user input.

        Args:
            stdscr (curses window): An initial window provided by curses that spans over the entire available space.
        Returns:
            None
        """

        # stdscr is the complete size of the terminal, all available pixels on the screen
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
        self.presenter.load_canvas_view()

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
