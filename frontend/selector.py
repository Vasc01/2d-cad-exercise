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
            curses.beep()
            x -= 1
        elif cursor_input == ord("6"):
            curses.beep()
            x += 1
        elif cursor_input == ord("8"):
            curses.beep()
            y -= 1
        elif cursor_input == ord("2"):
            curses.beep()
            y += 1
        elif cursor_input == ord("5"):
            curses.beep()
            window.addstr(y, x, element.symbol)

        window.move(y, x)
        window.refresh()



