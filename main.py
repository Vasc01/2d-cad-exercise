import curses
from frontend.window_creator import WindowCreator
from frontend.ui_function import UIFunction
from frontend.initial_data import (canvas, temporary_group, palette, predefined_square,
                                   predefined_z_shape, predefined_smiley)


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
        window_creator = WindowCreator(height, width)
        window_creator.calculate_split()

        # create windows
        menu_window = curses.newwin(*window_creator.get_menu_window())
        menu_window.border()
        window_creator.populate_window(menu_window, window_creator.position_menu_content())
        menu_window.refresh()

        tools_window = curses.newwin(*window_creator.get_tools_window())
        tools_window.border()
        window_creator.populate_window(tools_window, window_creator.position_tools_content())
        tools_window.refresh()

        ruler_window = curses.newwin(*window_creator.get_ruler_window())
        ruler_window.border()
        window_creator.populate_window(ruler_window, window_creator.position_ruler_content())
        ruler_window.refresh()

        canvas_window = curses.newwin(*window_creator.get_canvas_window())
        canvas_window.border()
        window_creator.populate_window(canvas_window, window_creator.position_canvas_content())
        canvas_window.refresh()

        prompt_window = curses.newwin(*window_creator.get_prompt_window())
        prompt_window.border()
        window_creator.populate_window(prompt_window, window_creator.position_prompt_content())
        prompt_window.refresh()

        input_window = curses.newwin(*window_creator.get_input_window())
        input_window.border()
        window_creator.populate_window(input_window, window_creator.position_input_content())
        input_window.refresh()

        # inner windows
        canvas_in = curses.newwin(*window_creator.get_canvas_in())
        prompt_in = curses.newwin(*window_creator.get_prompt_in())
        input_in = curses.newwin(*window_creator.get_input_in())
        palette_in = curses.newwin(*window_creator.get_palette_in())

        # curses specific window content
        ruler_window.addch(1, window_creator.ruler_ncols - 3, curses.ACS_RARROW)
        ruler_window.addch(window_creator.ruler_nlines - 2, 2, curses.ACS_DARROW)
        ruler_window.refresh()

        # handle functionalities of the user interface
        position_tools = window_creator.position_tools_content()
        ui_function = UIFunction(canvas_in, prompt_in, input_in, palette_in, tools_window, position_tools,
                                 canvas, temporary_group, palette)

        ui_function.load_palette()
        ui_function.load_canvas()

        ui_function.add_predefined_shape("square", predefined_square)
        ui_function.add_predefined_shape("z-shape", predefined_z_shape)
        ui_function.add_predefined_shape("smiley", predefined_smiley)

        # loop during use
        user_input = None
        while user_input != "q":

            input_in.clear()
            input_in.refresh()

            prompt_in.clear()
            prompt_in.addstr(0, 2, "Choose a command. Use keyboard shortcuts.")
            prompt_in.refresh()

            if user_input == "a":
                ui_function.add()
            elif user_input == "d":
                ui_function.delete()
            elif user_input == "m":
                ui_function.move()
            elif user_input == "r":
                ui_function.rotate()
            elif user_input == "mi":
                ui_function.mirror()
            elif user_input == "s":
                ui_function.scale()
            elif user_input == "i":
                ui_function.insert_shape()
            elif user_input == "c":
                ui_function.clear()

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

    # curses.wrapper takes care of curses initialization and returns the state of the terminal to default at the end
    # it returns errors to the terminal should they occur during execution
    curses.wrapper(app.mainloop)


if __name__ == "__main__":
    main()
