import curses

from backend.core import Element
from frontend.command import MoveCommand
from frontend.window_content import position_tools_content
from frontend.initial_data import transformer


class UIFunction:
    def __init__(self, canvas_in, prompt_in, input_in, palette_in, tools_window, canvas_group, temporary_group, palette):
        # ui_windows
        self.canvas_in = canvas_in
        self.prompt_in = prompt_in
        self.input_in = input_in
        self.palette_in = palette_in
        self.tools_window = tools_window
        # groups with elements
        self.canvas_group = canvas_group
        self.temporary_group = temporary_group
        self.palette = palette

    def load_canvas(self):
        for el in self. canvas_group.elements:
            symbol = el.symbol
            x = el.x
            y = el.y
            self.canvas_in.addstr(y, x, symbol)
        self.canvas_in.refresh()

    def load_palette(self):
        for el in self. palette.elements:
            symbol = el.symbol
            x = el.x
            y = el.y
            self.palette_in.addstr(y, x, symbol)
        self.palette_in.refresh()

    # select from canvas and transfer to temporary group for transformation
    def select(self):
        curses.noecho()
        curses.cbreak()

        # highlight select-label in tools window
        select = position_tools_content()["select"]
        self.tools_window.addstr(*select, curses.A_STANDOUT)
        self.tools_window.refresh()

        self.prompt_in.addstr(0, 2, f"Choose element! Navigate:NumLock arrows | Escape:Home | Select:5 | Deselect:-")
        self.prompt_in.refresh()

        x, y = 0, 0
        self.canvas_in.move(y, x)

        cursor_input = None
        while cursor_input != ord("7"):

            cursor_input = self.canvas_in.getch()
            if cursor_input == ord("4"):
                x -= 1
            elif cursor_input == ord("6"):
                x += 1
            elif cursor_input == ord("8"):
                y -= 1
            elif cursor_input == ord("2"):
                y += 1
            elif cursor_input == ord("5"):
                for el in self.canvas_group.elements:
                    if el.x == x and el.y == y:
                        self.temporary_group.add(el)
                        self.canvas_group.remove(el)
                        self.canvas_in.addstr(y, x, el.symbol, curses.A_STANDOUT)
            elif cursor_input == ord("-"):
                pass
                # deselect

            self.canvas_in.move(y, x)
            self.canvas_in.refresh()

        # return to normal select-label in tools window
        select = position_tools_content()["select"]
        self.tools_window.addstr(*select)
        self.tools_window.refresh()

        self.prompt_in.clear()
        self.prompt_in.addstr(0, 2, "Choose a command. Use keyboard shortcuts.")
        self.prompt_in.refresh()

    # def move(self, window, input, prompt, group, canvas_group):
    def move(self):

        # highlight move-label in tools window
        move = position_tools_content()["move"]
        self.tools_window.addstr(*move, curses.A_STANDOUT)
        self.tools_window.refresh()

        self.select()

        self.prompt_in.addstr(0, 2, "Enter delta-x and delta-y in the format '<value x>,<value y>'")
        self.prompt_in.refresh()

        curses.echo()
        curses.nocbreak()
        user_input = self.input_in.getstr(0, 2).decode(encoding="utf-8")
        x, y = [int(n) for n in user_input.split(",")]

        # delete representation of elements from the canvas
        for el in self.temporary_group.elements:
            self.canvas_in.addstr(el.y, el.x, " ")

        move_elements = MoveCommand(self.temporary_group, x, y)
        move_elements.execute()

        # add to canvas and remove from temporary group
        for el in self.temporary_group.elements:
            self.canvas_group.add(el)
        self.temporary_group.elements.clear()

        self.load_canvas()
        curses.beep()

        # return to normal move-label in tools window
        move = position_tools_content()["move"]
        self.tools_window.addstr(*move)
        self.tools_window.refresh()

    def select_from_palette(self):
        curses.noecho()
        curses.cbreak()

        # highlight select-label in tools window
        select = position_tools_content()["select"]
        self.tools_window.addstr(*select, curses.A_STANDOUT)
        self.tools_window.refresh()

        self.prompt_in.addstr(0, 2, "Choose element! Navigate:NumLock arrows | Escape:Home | Select:5")
        self.prompt_in.refresh()

        x, y = 0, 0
        self.palette_in.move(y, x)

        cursor_input = None
        while cursor_input != ord("7"):
            cursor_input = self.palette_in.getch()
            if cursor_input == ord("4"):
                x -= 1
            elif cursor_input == ord("6"):
                x += 1
            elif cursor_input == ord("8"):
                y -= 1
            elif cursor_input == ord("2"):
                y += 1
            elif cursor_input == ord("5"):

                for el in self.palette.elements:
                    if el.x == x and el.y == y:
                        self.temporary_group.add(el)
                        self.palette_in.addstr(y, x, el.symbol, curses.A_STANDOUT)
            elif cursor_input == ord("-"):
                pass
                # deselect

            self.palette_in.move(y, x)
            self.palette_in.refresh()

        # return to normal select-label in tools window
        select = position_tools_content()["select"]
        self.tools_window.addstr(*select)
        self.tools_window.refresh()

        self.prompt_in.clear()
        # self.prompt_in.addstr(0, 2, "Choose a command. Use keyboard shortcuts.")
        self.prompt_in.refresh()

    def add(self):

        # highlight add element-label in tools window
        select = position_tools_content()["elements"]
        self.tools_window.addstr(*select, curses.A_STANDOUT)
        self.tools_window.refresh()

        self.select_from_palette()

        self.prompt_in.addstr(0, 2, "Place element! Navigate:NumLock arrows | Escape:Home | Place:5")
        self.prompt_in.refresh()

        self.place_on_canvas()

        self.temporary_group.elements.clear()

        self.load_canvas()
        self.load_palette()
        curses.beep()

        # return to normal add element-label in tools window
        select = position_tools_content()["elements"]
        self.tools_window.addstr(*select)
        self.tools_window.refresh()

    def place_on_canvas(self):
        curses.noecho()
        curses.cbreak()

        x, y = 0, 0
        self.canvas_in.move(y, x)

        cursor_input = None
        while cursor_input != ord("7"):

            cursor_input = self.canvas_in.getch()
            if cursor_input == ord("4"):
                x -= 1
            elif cursor_input == ord("6"):
                x += 1
            elif cursor_input == ord("8"):
                y -= 1
            elif cursor_input == ord("2"):
                y += 1
            elif cursor_input == ord("5"):
                symbol = self.temporary_group.elements[0].symbol
                element = Element(x, y).set_transformer(transformer).set_symbol(symbol)
                self.canvas_group.add(element)
                self.canvas_in.addstr(y, x, symbol, curses.A_STANDOUT)

            elif cursor_input == ord("-"):
                pass
                # deselect/remove

            self.canvas_in.move(y, x)
            self.canvas_in.refresh()
