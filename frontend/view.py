import curses

from abc import abstractmethod, ABC


class ViewABC(ABC):

    @abstractmethod
    def send_user_input(self):
        raise NotImplemented

    @abstractmethod
    def update_ui(self):
        raise NotImplemented


class UserInterface(ViewABC):

    def __init__(self, presenter):

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

        self.presenter = presenter

    def send_user_input(self):
        raise NotImplemented
        # sends the user choice from the while loop to presenter if choice is correct

    def update_ui(self):
        raise NotImplemented
        # functions loading and updating windows from tuples/lists with data

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

        # refresh all

    def expect_main_command(self, stdscr):

        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # create windows
        self.initiate_windows(height, width)

        # presenter.load_palette()
        # presenter.load_canvas()
        # presenter.add_predefined_shape("square", predefined_square)
        # presenter.add_predefined_shape("z-shape", predefined_z_shape)
        # presenter.add_predefined_shape("smiley", predefined_smiley)

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
        curses.wrapper(self.expect_main_command)
