def position_menu_content(ncols):

    menu_window_content = {
        "undo": (1, 2, "<Undo"),
        "redo": (1, 9, "Redo>"),
        "save": (1, 20, "Save"),
        "load": (1, 27, "Load"),
        "help": (1, 34, "Help"),
        "about": (1, 41, "About"),
        "donate": (1, 49, "Donate"),
        "Quit": (1, ncols - 6, "Quit")
    }
    return menu_window_content


def position_tools_content():
    tools_window_content = {
        "elements": (1, 2, "Add Element"),
        "select": (6, 2, "Select"),
        "move": (10, 2, "Move"),
        "rotate": (11, 2, "Rotate"),
        "mirror": (12, 2, "Mirror"),
        "scale": (13, 2, "Scale"),
        "fill": (14, 2, "Fill"),
        "union": (15, 2, "Union"),
        "difference": (16, 2, "Difference"),
        "split": (17, 2, "Split")
    }
    return tools_window_content


def position_ruler_content(ncols, nlines):
    ruler_window_content = {}

    for c in range(0, ncols - 12, 5):
        number = str(c)
        content = (1, c + 6, number)
        ruler_window_content[f"ncols-{c}"] = content

    for r in range(0, nlines - 6, 1):
        number = str(r)
        content = (r + 3, 2, number)
        ruler_window_content[f"nlines-{r}"] = content

    ruler_window_content["X"] = (1, ncols - 4, "X")
    ruler_window_content["Y"] = (nlines - 3, 2, "Y")

    return ruler_window_content


def position_canvas_content():
    input_window_content = {"header": (0, 1, "Canvas")}
    return input_window_content


def position_prompt_content():
    input_window_content = {"header": (0, 6, "Prompt")}
    return input_window_content


def position_input_content():
    input_window_content = {"header": (0, 6, "Input")}
    return input_window_content


def populate_window(window, population):
    for value in population.values():
        window.addstr(*value)
