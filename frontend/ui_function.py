import curses

from backend.core import Element
from frontend.command import MoveCommand
from frontend.initial_data import transformer


class UIFunction:
    def __init__(self, canvas_in, prompt_in, input_in, palette_in, tools_window, position_tools_content,
                 canvas_group, temporary_group, palette):
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
        # content
        self.position_tools_content = position_tools_content

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

    @staticmethod
    def navigate(window, on_five):
        curses.noecho()
        curses.cbreak()
        height, width = window.getmaxyx()

        x, y = 0, 0
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

    # allow selection and highlight of multiple elements
    def canvas_to_temp(self, x, y):
        for el in self.canvas_group.elements:
            if el.x == x and el.y == y:
                self.temporary_group.add(el)
                self.canvas_group.remove(el)
                self.canvas_in.addstr(y, x, el.symbol, curses.A_STANDOUT)

    # allow selection and highlight of only one element
    def palette_to_temp(self, x, y):
        for el in self.palette.elements:
            if el.x == x and el.y == y:
                if len(self.temporary_group.elements) != 0:
                    self.temporary_group.elements.clear()
                    self.load_palette()
                self.temporary_group.add(el)
                self.palette_in.addstr(y, x, el.symbol, curses.A_STANDOUT)

    def temp_to_canvas(self):
        for el in self.temporary_group.elements:
            self.canvas_group.add(el)

    def new_el_to_canvas(self, x, y):
        symbol = self.temporary_group.elements[0].symbol
        element = Element(x, y).set_transformer(transformer).set_symbol(symbol)
        self.canvas_group.add(element)
        self.canvas_in.addstr(y, x, symbol, curses.A_STANDOUT)

    def move(self):

        self.highlight_tool("move")

        # selection
        self.highlight_tool("select")

        self.prompt_in.addstr(0, 2, f"Choose element! Navigate:NumLock arrows | Escape:Home | Select:5 | Deselect:-")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.canvas_to_temp)

        self.play_down_tool("select")
        # end of selection

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

        self.temp_to_canvas()
        self.temporary_group.elements.clear()

        self.load_canvas()
        curses.beep()

        self.play_down_tool("move")

    def add(self):

        self.highlight_tool("elements")

        # selection
        self.highlight_tool("select")

        self.prompt_in.addstr(0, 2, "Choose element! Navigate:NumLock arrows | Escape:Home | Select:5")
        self.prompt_in.refresh()

        self.navigate(self.palette_in, self.palette_to_temp)

        self.play_down_tool("select")
        # end of selection

        self.prompt_in.addstr(0, 2, "Place element! Navigate:NumLock arrows | Escape:Home | Place:5")
        self.prompt_in.refresh()

        self.navigate(self.canvas_in, self.new_el_to_canvas)

        self.temporary_group.elements.clear()

        self.load_canvas()
        self.load_palette()
        curses.beep()

        self.play_down_tool("elements")
