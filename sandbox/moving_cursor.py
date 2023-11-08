import curses


def draw_menu(stdscr):

    x, y = 1, 1
    stdscr.move(y, x)

    cursor_input = None
    while cursor_input != curses.KEY_HOME:

        cursor_input = stdscr.getch()
        if cursor_input == curses.KEY_LEFT:
            x -= 1
        elif cursor_input == curses.KEY_RIGHT:
            x += 1
        elif cursor_input == curses.KEY_UP:
            y -= 1
        elif cursor_input == curses.KEY_DOWN:
            y += 1

        stdscr.move(y, x)
        stdscr.refresh()


curses.wrapper(draw_menu)

