import curses


def draw_menu(stdscr):

    stdscr.border()
    # stdscr.getch()

    x, y = 0, 0

    selection_input = None
    while selection_input != "KEY_HOME":

        selection_input = stdscr.getkey()
        if selection_input == "KEY_LEFT":
            x -= 1
        elif selection_input == "KEY_RIGHT":
            x += 1
        elif selection_input == "KEY_UP":
            y -= 1
        elif selection_input == "KEY_DOWN":
            y += 1

        # elif selection_input == ord("e"):
        #     break

        # stdscr.clear()
        stdscr.addstr(y, x, "0")
        stdscr.refresh()


curses.wrapper(draw_menu)
