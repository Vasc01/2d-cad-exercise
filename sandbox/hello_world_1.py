import curses
from curses import wrapper


def main(stdscr):
    stdscr.clear()

    for c in range(0, 101, 5):
        number = str(c)
        stdscr.addstr(0, c, number)
    for r in range(0, 21, 5):
        number = str(r)
        stdscr.addstr(r, 0, number)

    stdscr.addstr(2, 2, "hello world", curses.A_STANDOUT)
    stdscr.addstr(10, 10, "1234")
    stdscr.refresh()
    stdscr.getch()


wrapper(main)
