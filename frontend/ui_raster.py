import curses


def ui_windows(stdscr):

    stdscr.clear()

    height, width = stdscr.getmaxyx()

    menu_nlines = 3
    menu_ncols = width
    menu_begin_x = 0
    menu_begin_y = 0

    tools_nlines = height - (menu_nlines - 1)
    tools_ncols = 15
    tools_begin_x = 0
    tools_begin_y = menu_nlines - 1

    input_nlines = 3
    input_ncols = width - (tools_ncols - 1)
    input_begin_x = tools_ncols - 1
    input_begin_y = height - 3

    prompt_nlines = 3
    prompt_ncols = width - (tools_ncols - 1)
    prompt_begin_x = tools_ncols - 1
    prompt_begin_y = input_begin_y - 2

    ruler_nlines = height - ((prompt_nlines - 1) + (input_nlines - 1)) - (menu_nlines - 1)
    ruler_ncols = width - (tools_ncols - 1)
    ruler_begin_x = tools_ncols - 1
    ruler_begin_y = menu_nlines - 1

    canvas_nlines = ruler_nlines - 2
    canvas_ncols = ruler_ncols - 5
    canvas_begin_x = ruler_begin_x + 5
    canvas_begin_y = ruler_begin_y + 2

    # curses.newwin(nlines, ncols, begin_y, begin_x)

    menu_window = curses.newwin(menu_nlines, menu_ncols, menu_begin_y, menu_begin_x)
    menu_window.border()
    menu_window.addstr(1, 2, "<Undo")
    menu_window.addstr(1, 9, "Redo>")
    menu_window.addstr(1, 20, "Save")
    menu_window.addstr(1, 27, "Load")
    menu_window.addstr(1, 34, "Help")
    menu_window.addstr(1, 41, "About")
    menu_window.addstr(1, 49, "Donate")
    menu_window.refresh()

    tools_window = curses.newwin(tools_nlines, tools_ncols, tools_begin_y, tools_begin_x)
    tools_window.border()
    tools_window.addstr(1, 2, "Elements")
    tools_window.addstr(2, 2, "@ % X * + _")
    tools_window.addstr(3, 2, "Z ! } = O ?")
    tools_window.addstr(6, 2, "Select")
    tools_window.addstr(7, 2, "Deselect")
    tools_window.addstr(10, 2, "Move")
    tools_window.addstr(11, 2, "Rotate")
    tools_window.addstr(12, 2, "Mirror")
    tools_window.addstr(13, 2, "Scale")
    tools_window.addstr(14, 2, "Fill")
    tools_window.addstr(15, 2, "Union")
    tools_window.addstr(16, 2, "Difference")
    tools_window.addstr(17, 2, "Split")
    tools_window.refresh()

    ruler_window = curses.newwin(ruler_nlines, ruler_ncols, ruler_begin_y, ruler_begin_x)
    ruler_window.border()

    for c in range(0, ruler_ncols-12, 5):
        number = str(c)
        ruler_window.addstr(1, c+6, number)
    for r in range(0, ruler_nlines-5, 1):
        number = str(r)
        ruler_window.addstr(r+3, 2, number)

    ruler_window.addstr(1, width-17, "X")
    ruler_window.addstr(height-8, 2, "Y")
    ruler_window.refresh()

    canvas_window = curses.newwin(canvas_nlines, canvas_ncols, canvas_begin_y, canvas_begin_x)
    canvas_window.border()
    canvas_window.addstr(0, 1, "Canvas")
    canvas_window.refresh()

    prompt_window = curses.newwin(prompt_nlines, prompt_ncols, prompt_begin_y, prompt_begin_x)
    prompt_window.border()
    prompt_window.addstr(0, 6, "Prompt")
    prompt_window.addstr(1, 2, "Enter delta-x and delta-y in the format '<value x>,<value y>'")
    prompt_window.refresh()

    input_window = curses.newwin(input_nlines, input_ncols, input_begin_y, input_begin_x)
    input_window.border()
    input_window.addstr(0, 6, "Input")
    input_window.addstr(1, 2, "5,3")
    input_window.refresh()

    input_window.getch()


