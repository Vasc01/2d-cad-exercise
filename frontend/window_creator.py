class WindowCreator:
    """Split the screen in windows and fill them

    The size of the terminal is evaluated and the sizes of the windows are calculated to have proper visual
    representation.

    Attributes:
        width (int): Number of available characters in the terminal horizontally
        height (int): Number of available characters in the terminal vertically
        ...

        For the creation of a window curses requires four attributes:
        - number of lines, size of the window vertically
        - number of columns, size of the window horizontally
        - horizontal position of top left corner for the window
        - vertical position of top left corner for the window
        These attributes are defined here for each window to be created in the user interface
    """
    def __init__(self, height, width):

        self.width = width
        self.height = height

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

    # define window sizes and positions
    def calculate_split(self, menu_window_nlines=3, tools_window_ncols=15, input_window_nlines=3,
                        prompt_window_nlines=3):
        """Calculate the window sizes for the user interface

        Only few fixed points are required to define the user interface, everything else is calculated from them and
        the size of the terminal.

        Args:
            menu_window_nlines (int): Height of the menu window.
            tools_window_ncols (int): Width of the tools window.
            input_window_nlines (int): Height of the input window.
            prompt_window_nlines (int): Height of the prompt.

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

    def get_menu_window(self):
        return self.menu_nlines, self.menu_ncols, self.menu_begin_y, self.menu_begin_x

    def get_tools_window(self):
        return self.tools_nlines, self.tools_ncols, self.tools_begin_y, self.tools_begin_x

    def get_ruler_window(self):
        return self.ruler_nlines, self.ruler_ncols, self.ruler_begin_y, self.ruler_begin_x

    def get_canvas_window(self):
        return self.canvas_nlines, self.canvas_ncols, self.canvas_begin_y, self.canvas_begin_x

    def get_prompt_window(self):
        return self.prompt_nlines, self.prompt_ncols, self.prompt_begin_y, self.prompt_begin_x

    def get_input_window(self):
        return self.input_nlines, self.input_ncols, self.input_begin_y, self.input_begin_x

    # inner windows
    def get_canvas_in(self):
        return self.canvas_in_nlines, self.canvas_in_ncols, self.canvas_in_begin_y, self.canvas_in_begin_x

    def get_prompt_in(self):
        return self.prompt_in_nlines, self.prompt_in_ncols, self.prompt_in_begin_y, self.prompt_in_begin_x

    def get_input_in(self):
        return self.input_in_nlines, self.input_in_ncols, self.input_in_begin_y, self.input_in_begin_x

    def get_palette_in(self):
        return self.palette_in_nlines, self.palette_in_ncols, self.palette_in_begin_y, self.palette_in_begin_x

    def position_menu_content(self):
        """Define/calculate positions for window content

        Having the positions and content in a dictionary accessible with a key helps to manipulate them dynamically
        during use.

        Returns:
            Dictionary with content and its positions
        """
        menu_window_content = {
            "undo": (1, 2, "<Undo"),
            "redo": (1, 9, "Redo>"),
            "save": (1, 20, "Save"),
            "load": (1, 27, "Load"),
            "help": (1, 34, "Help"),
            "about": (1, 41, "About"),
            "donate": (1, 49, "Donate"),
            "Quit": (1, self.menu_ncols - 6, "Quit")
        }
        return menu_window_content

    @staticmethod
    def position_tools_content():
        """Define/calculate positions for window content

        Having the positions and content in a dictionary accessible with a key helps to manipulate them dynamically
        during use.

        Returns:
            Dictionary with content and its positions
        """
        tools_window_content = {
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
        return tools_window_content

    def position_ruler_content(self):
        """Define/calculate positions for window content

        Dependent on available space different size of content is generated. The rulers always have the
        coordinate axes annotated at the end.

        Returns:
            Dictionary with content and its positions
        """
        ruler_window_content = {}

        for c in range(0, self.ruler_ncols - 12, 5):
            number = str(c)
            content = (1, c + 6, number)
            ruler_window_content[f"ncols-{c}"] = content

        for r in range(0, self.ruler_nlines - 6, 1):
            number = str(r)
            content = (r + 3, 2, number)
            ruler_window_content[f"nlines-{r}"] = content

        ruler_window_content["X"] = (1, self.ruler_ncols - 4, "X")
        ruler_window_content["Y"] = (self.ruler_nlines - 3, 2, "Y")

        return ruler_window_content

    @staticmethod
    def position_canvas_content():
        input_window_content = {"header": (0, 1, "Canvas")}
        return input_window_content

    @staticmethod
    def position_prompt_content():
        input_window_content = {"header": (0, 6, "Prompt")}
        return input_window_content

    @staticmethod
    def position_input_content():
        input_window_content = {"header": (0, 6, "Input")}
        return input_window_content

    @staticmethod
    def populate_window(window, population):
        for value in population.values():
            window.addstr(*value)
