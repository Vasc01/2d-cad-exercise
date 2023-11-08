import curses

from backend.core import Element
from frontend.command import MoveCommand, RotateCommand, MirrorCommand, ScaleCommand
from frontend.initial_data import transformer


class UIFunction:
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
        if shape_name in self.predefined_shapes:
            self.canvas_group.add(self.predefined_shapes[shape_name])

    def load_canvas(self):
        self.canvas_in.clear()
        for el in self.canvas_group.elements:
            symbol = el.symbol
            x = el.x
            y = el.y
            self.canvas_in.addstr(y, x, symbol)
            try:
                for el_in in el.elements:
                    symbol_in = el_in.symbol
                    x_in = el_in.x
                    y_in = el_in.y
                    self.canvas_in.addstr(y_in, x_in, symbol_in)
            except AttributeError:
                pass
        self.canvas_in.refresh()

    def load_palette(self):
        for el in self.palette_group.elements:
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

    # allow selection and highlight of multiple elements
    def canvas_to_temp(self, x, y):
        for el in self.canvas_group.elements:
            if el.x == x and el.y == y:
                self.temporary_group.add(el)
                self.canvas_group.remove(el)
                self.canvas_in.addstr(y, x, el.symbol, curses.A_STANDOUT)

    # allow selection and highlight of only one element
    def palette_to_temp(self, x, y):
        for el in self.palette_group.elements:
            if el.x == x and el.y == y:
                if len(self.temporary_group.elements) != 0:
                    self.temporary_group.elements.clear()
                    self.load_palette()
                self.temporary_group.add(el)
                self.palette_in.addstr(y, x, el.symbol, curses.A_STANDOUT)

    def canvas_to_reference_point(self, x, y):
        if self.reference_point:
            self.load_canvas()
        self.reference_point = (x, y)
        self.canvas_in.addstr(y, x, "+", curses.A_STANDOUT)

    def temp_to_canvas(self):
        for el in self.temporary_group.elements:
            el.x = round(el.x)
            el.y = round(el.y)

            # elements out of the canvas size are disregarded
            height, width = self.canvas_in.getmaxyx()
            if el.x not in range(0, width) or el.y not in range(0, height):
                continue

            self.canvas_group.add(el)

    def new_el_to_canvas(self, x, y):
        symbol = self.temporary_group.elements[0].symbol
        element = Element(x, y).set_transformer(transformer).set_symbol(symbol)
        self.canvas_group.add(element)
        self.canvas_in.addstr(y, x, symbol, curses.A_STANDOUT)

    def add(self):

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
