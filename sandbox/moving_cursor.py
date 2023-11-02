import curses


def draw_menu(stdscr):

    x, y = 1, 1
    stdscr.move(y, x)

    cursor_input = None
    while cursor_input != curses.KEY_HOME:

        cursor_input = stdscr.getch()
        if cursor_input == curses.KEY_LEFT:
            curses.beep()
            x -= 1
        elif cursor_input == curses.KEY_RIGHT:
            curses.beep()
            x += 1
        elif cursor_input == curses.KEY_UP:
            curses.beep()
            y -= 1
        elif cursor_input == curses.KEY_DOWN:
            curses.beep()
            y += 1

        stdscr.move(y, x)
        stdscr.refresh()


curses.wrapper(draw_menu)

