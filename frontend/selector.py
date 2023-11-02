import curses

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
            window.addstr(y, x, element.symbol)
            element.x = x
            element.y = y
            group.add(element)

        window.move(y, x)
        window.refresh()


def navigator_select(window, group):
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
            element.x = x
            element.y = y
            group.add(element)

        window.move(y, x)
        window.refresh()

