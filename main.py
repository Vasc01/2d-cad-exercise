"""The main eventloop is started in this module.
"""

import curses

# FIXME: The place of WindowCreator is not here, it shall be part of the presentation layer
from frontend.window_creator import WindowCreator
from frontend.ui_function import UIFunction

# FIXME: The place of the initial data is not here, it shall be part of the data layer
from frontend.initial_data import (canvas, temporary_group, palette, predefined_square,
                                   predefined_z_shape, predefined_smiley)


class Application:
    """Creator of the frontend.
    This class creates the appearance of the user interface and listens for user input.
    For the creation of the interface it depends on the class WindowCreator.
    For the response to user input it relays on UIFunction.
    """

    # FIXME: The application is the combination of the different layers.
    #
    #  Popular names for the layers are:
    #   - Presentation Layer    (presenter, view)
    #   - Business Layer        (view, controller)
    #   - Data Layer            (model)

    def __init__(self):
        # FIXME: Missing aggregation relationship to the command interface
        pass

    @staticmethod
    def mainloop(stdscr):
        # FIXME: Describe the parameter stdscr, shall not be a mystery
        # FIXME: This function is not stuctured enough, too long
        # FIXME: The application knows about curses, it shall know about our own interface, not curses

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

        # create inner windows
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

        # FIXME: This composition relationship is missing in the UML diagram
        # Improve the user interface for the presentation layer (Builder Pattern)
        # The name shall not be UIFunction, too generic. Use a more specific name, like
        # UserInterface, Presenter, or something like that.
        #
        # presenter = (
        #   Presenter(...)
        #   .add_window(canvas_in)
        #   .add_window(prompt_in)
        #   .add_window(input_in)
        #   .add_shape("square", predefined_square)
        #   ....
        #   .load_palette()
        #   .load_canvas()
        #   )

        ui_function = UIFunction(canvas_in, prompt_in, input_in, palette_in, tools_window, position_tools,
                                 canvas, temporary_group, palette)

        # load content
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

    # FIXME: Why is this necessary? Why the user must use curses.wrapper? Why is it not packed into a class?
    # The application shall have several layers, each layer shall be a class. One of the classes must use the
    # curses.wrapper. The other classes must not know about curses.wrapper.


if __name__ == "__main__":
    main()
