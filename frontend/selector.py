import curses

from frontend.command import MoveCommand

"""
TODO:
    - move cursor in given space
    - select position by taking x and y
    - find the element with that coordinates
    - save it in temporary group
        - for drawing use 1 element
        - for other use multiple Elements
"""


def selector(window, element):
    curses.noecho()
    curses.cbreak()

    x, y = 1, 1
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
            window.addstr(y, x, element.symbol)

        window.move(y, x)
        window.refresh()


def navigator_draw(window, group, element):
    curses.noecho()
    curses.cbreak()

    x, y = 1, 1
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
            # window.addstr(y, x, element.symbol) do not draw. just add element and it should appear
            element.x = x
            element.y = y
            group.add(element)

        window.move(y, x)
        window.refresh()


def navigator_select(window, canvas_group, selected_index, selected_elements):
    curses.noecho()
    curses.cbreak()

    x, y = 1, 1
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
            for el in canvas_group.elements:
                if el.x == x and el.y == y:
                    selected_elements.add(el)
                    canvas_group.remove(el)
                    window.addstr(y, x, el.symbol, curses.A_STANDOUT)

        window.move(y, x)
        window.refresh()


def move_initiation(window, input, prompt, group, canvas_group):
    prompt.addstr(1, 2, "Enter delta-x and delta-y in the format '<value x>,<value y>'")
    prompt.refresh()
    user_input = input.getstr(1, 2).decode(encoding="utf-8")
    x, y = [int(n) for n in user_input.split(",")]

    for el in group.elements:
        window.addstr(el.y, el.x, " ")

    move_things = MoveCommand(group, x, y)
    move_things.execute()

    for el in group.elements:
        canvas_group.add(el)

    group.elements.clear()

    # pack this in function
    for el in canvas_group.elements:
        symbol = el.symbol
        x = el.x
        y = el.y
        window.addstr(y, x, symbol)
    window.refresh()

    curses.beep()

    prompt.addstr(1, 2, "Choose a command. Use keyboard shortcuts.                            ")
    prompt.refresh()

    # clear previous input
    for position_x in range(1, 10):
        input.addstr(1, position_x, " ")
    input.refresh()
