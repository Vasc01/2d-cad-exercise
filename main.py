import curses
from frontend.screen_splitter import ScreenSplitter
from frontend.window_content import (
    position_menu_content, position_tools_content, position_input_content, position_ruler_content,
    position_canvas_content, position_prompt_content, populate_window)
from frontend.ui_function import UIFunction
from frontend.initial_data import canvas, temporary_group, palette


class Application:

    def __init__(self):
        pass

    @staticmethod
    def mainloop(stdscr):

        stdscr.clear()

        # initialize use of colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

        # define sizes of separate windows
        height, width = stdscr.getmaxyx()
        screen_splitter = ScreenSplitter(height, width)
        screen_splitter.calculate_split()

        # create windows
        menu_window = curses.newwin(*screen_splitter.get_menu_window())
        menu_window.border()
        populate_window(menu_window, position_menu_content(screen_splitter.menu_ncols), )
        menu_window.refresh()

        tools_window = curses.newwin(*screen_splitter.get_tools_window())
        tools_window.border()
        populate_window(tools_window, position_tools_content())
        tools_window.refresh()

        ruler_window = curses.newwin(*screen_splitter.get_ruler_window())
        ruler_window.border()
        populate_window(ruler_window, position_ruler_content(screen_splitter.ruler_ncols, screen_splitter.ruler_nlines))
        ruler_window.refresh()

        canvas_window = curses.newwin(*screen_splitter.get_canvas_window())
        canvas_window.border()
        populate_window(canvas_window, position_canvas_content())
        canvas_window.refresh()

        prompt_window = curses.newwin(*screen_splitter.get_prompt_window())
        prompt_window.border()
        populate_window(prompt_window, position_prompt_content())
        prompt_window.refresh()

        input_window = curses.newwin(*screen_splitter.get_input_window())
        input_window.border()
        populate_window(input_window, position_input_content())
        input_window.refresh()

        # inner windows
        canvas_in = curses.newwin(*screen_splitter.get_canvas_in())
        prompt_in = curses.newwin(*screen_splitter.get_prompt_in())
        input_in = curses.newwin(*screen_splitter.get_input_in())
        palette_in = curses.newwin(*screen_splitter.get_palette_in())

        # curses specific window content
        ruler_window.addch(1, screen_splitter.ruler_ncols - 3, curses.ACS_RARROW)
        ruler_window.addch(screen_splitter.ruler_nlines - 2, 2, curses.ACS_DARROW)
        ruler_window.refresh()

        # handle functionalities of the user interface
        ui_function = UIFunction(canvas_in, prompt_in, input_in, palette_in, tools_window, canvas, temporary_group,
                                 palette)

        ui_function.load_palette()

        # loop during use
        user_input = None
        while user_input != "q":

            input_in.clear()
            input_in.refresh()

            prompt_in.clear()
            prompt_in.addstr(0, 2, "Choose a command. Use keyboard shortcuts.")
            prompt_in.refresh()

            ui_function.load_canvas()

            if user_input == "s":
                ui_function.select()
            elif user_input == "m":
                ui_function.move()
            elif user_input == "a":
                ui_function.add()

            input_in.clear()
            input_in.refresh()

            prompt_in.clear()
            prompt_in.addstr(0, 2, "Choose a command. Use keyboard shortcuts.")
            prompt_in.refresh()

            # new input
            curses.echo()
            curses.nocbreak()
            user_input = input_in.getstr(0, 2).decode(encoding="utf-8")


def main():
    app = Application()

    # curses.wrapper takes care of curses initialization and returns the state of the terminal to default
    # it returns errors to the terminal should they occur during execution
    curses.wrapper(app.mainloop)


if __name__ == "__main__":
    main()
