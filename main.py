"""Starts the program.

This is the file to address from the console to start the program
"""

from frontend.view import View


class Application(object):
    """Receives a user interface and calls its execution
    Attributes:
        user_interface (View): The View module is placed here to be executed.
    """

    def __init__(self, user_interface):
        self.user_interface = user_interface

    def run(self):
        self.user_interface.run_main_loop()


def main():
    view = View()
    application = Application(view)
    application.run()


if __name__ == "__main__":
    main()
