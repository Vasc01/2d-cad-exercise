import curses
from backend.core import Element, Canvas, Group
from frontend.selector import selector

# Elements Palette
element_A = Element(0, 0).set_symbol("A")
element_B = Element(0, 0).set_symbol("B")
element_C = Element(0, 0).set_symbol("C")
elements_palette = Group()
elements_palette.add(element_A)
elements_palette.add(element_B)
elements_palette.add(element_C)


# Elements preexistent on canvas
element_1 = Element(20, 10).set_symbol("@")
element_2 = Element(21, 10).set_symbol("%")
element_3 = Element(0, 0).set_symbol("X")
canvas = Canvas()
canvas.add(element_1)
canvas.add(element_2)


class Application:

    def __init__(self):
        pass

    @staticmethod
    def mainloop(stdscr):

        stdscr.clear()
        # curses.initscr()

        height, width = stdscr.getmaxyx()

        # find window sizes and positions
        menu_nlines = 3
        menu_ncols = width
        menu_begin_x = 0
        menu_begin_y = 0

        tools_nlines = height - (menu_nlines - 1)
        tools_ncols = 15
        tools_begin_x = 0
        tools_begin_y = menu_nlines - 1

        input_nlines = 3
        input_ncols = width - (tools_ncols - 1)
        input_begin_x = tools_ncols - 1
        input_begin_y = height - 3

        prompt_nlines = 3
        prompt_ncols = width - (tools_ncols - 1)
        prompt_begin_x = tools_ncols - 1
        prompt_begin_y = input_begin_y - 2

        ruler_nlines = height - ((prompt_nlines - 1) + (input_nlines - 1)) - (menu_nlines - 1)
        ruler_ncols = width - (tools_ncols - 1)
        ruler_begin_x = tools_ncols - 1
        ruler_begin_y = menu_nlines - 1

        canvas_nlines = ruler_nlines - 2
        canvas_ncols = ruler_ncols - 5
        canvas_begin_x = ruler_begin_x + 5
        canvas_begin_y = ruler_begin_y + 2

        # create windows and initial content
        # curses.newwin(nlines, ncols, begin_y, begin_x)

        menu_window = curses.newwin(menu_nlines, menu_ncols, menu_begin_y, menu_begin_x)
        menu_window.border()
        menu_window.addstr(1, 2, "<Undo")
        menu_window.addstr(1, 9, "Redo>")
        menu_window.addstr(1, 20, "Save")
        menu_window.addstr(1, 27, "Load")
        menu_window.addstr(1, 34, "Help")
        menu_window.addstr(1, 41, "About")
        menu_window.addstr(1, 49, "Donate")
        menu_window.addstr(1, menu_ncols - 6, "Quit")

        menu_window.refresh()

        tools_window = curses.newwin(tools_nlines, tools_ncols, tools_begin_y, tools_begin_x)
        tools_window.border()
        tools_window.addstr(1, 2, "Elements")

        n = 2
        for el in elements_palette.elements:
            tools_window.addstr(2, n, el.symbol)
            n += 2

        tools_window.addstr(3, 2, "@ % X * + _")
        tools_window.addstr(4, 2, "Z ! } = O ?")
        tools_window.addstr(6, 2, "Select")
        tools_window.addstr(7, 2, "Deselect")
        tools_window.addstr(10, 2, "Move")
        tools_window.addstr(11, 2, "Rotate")
        tools_window.addstr(12, 2, "Mirror")
        tools_window.addstr(13, 2, "Scale")
        tools_window.addstr(14, 2, "Fill")
        tools_window.addstr(15, 2, "Union")
        tools_window.addstr(16, 2, "Difference")
        tools_window.addstr(17, 2, "Split")
        tools_window.refresh()

        ruler_window = curses.newwin(ruler_nlines, ruler_ncols, ruler_begin_y, ruler_begin_x)
        ruler_window.border()

        for c in range(0, ruler_ncols - 12, 5):
            number = str(c)
            ruler_window.addstr(1, c + 6, number)
        for r in range(0, ruler_nlines - 6, 1):
            number = str(r)
            ruler_window.addstr(r + 3, 2, number)

        ruler_window.addstr(1, width - 18, "X")
        ruler_window.addch(1, width - 17, curses.ACS_RARROW)
        ruler_window.addstr(height - 9, 2, "Y")
        ruler_window.addch(height - 8, 2, curses.ACS_DARROW)
        ruler_window.refresh()

        canvas_window = curses.newwin(canvas_nlines, canvas_ncols, canvas_begin_y, canvas_begin_x)
        canvas_window.border()
        canvas_window.addstr(0, 1, "Canvas")
        canvas_window.refresh()

        prompt_window = curses.newwin(prompt_nlines, prompt_ncols, prompt_begin_y, prompt_begin_x)
        prompt_window.border()
        prompt_window.addstr(0, 6, "Prompt")
        prompt_window.addstr(1, 2, "Enter delta-x and delta-y in the format '<value x>,<value y>'")
        prompt_window.refresh()

        input_window = curses.newwin(input_nlines, input_ncols, input_begin_y, input_begin_x)
        input_window.border()
        input_window.addstr(0, 6, "Input")
        input_window.refresh()

        donate_window = curses.newwin(5, 50, 10, 45)
        donate_window.border()
        donate_window.addstr(0, 6, "Donate")
        donate_window.addstr(2, 6, "19.99$/month")
        donate_window.addstr(3, 6, "Press any key to accept")

        user_input = None
        while user_input != "q":

            # clear previous input
            for position_x in range(1, input_ncols-1):
                input_window.addstr(1, position_x, " ")
            input_window.refresh()

            # clear previous prompt
            for position_x in range(1, prompt_ncols-1):
                prompt_window.addstr(1, position_x, " ")
            prompt_window.refresh()

            # refresh elements on canvas
            for el in canvas.elements:
                symbol = el.symbol
                x = el.x
                y = el.y
                canvas_window.addstr(y, x, symbol)
            canvas_window.refresh()

            if user_input == "s":
                selector(canvas_window, element_3)



            # new input
            curses.echo()
            curses.nocbreak()
            user_input = input_window.getstr(1, 2).decode(encoding="utf-8")


def main():
    app = Application()

    # curses.wrapper takes care of curses initialization and returns the state of the terminal to default
    # it returns errors to the terminal should they occur during execution
    curses.wrapper(app.mainloop)


if __name__ == "__main__":
    main()
