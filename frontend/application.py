import curses


class Application:

    def __init__(self):
        pass

    @staticmethod
    def mainloop(stdscr):

        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for c in range(0, width, 5):
            number = str(c)
            stdscr.addstr(0, c, number)
        for r in range(0, height, 1):
            number = str(r)
            stdscr.addstr(r, 0, number)

        stdscr.addstr(2, 50, " ", curses.A_STANDOUT)
        stdscr.addstr(5, 0, "Write Command: ")

        stdscr.refresh()
        k = 0
        point = 0
        while k != ord('q'):

            if k == ord('m'):
                point += 5
                stdscr.addstr(2, point, " ", curses.A_STANDOUT)
                stdscr.refresh()

            k = stdscr.getch()




def main():
    app = Application()

    # curses.wrapper takes care of curses initialization and returns the state of the terminal to usual
    # it returns errors to the terminal should they occur during execution
    curses.wrapper(app.mainloop)


if __name__ == "__main__":
    main()
