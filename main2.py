from frontend.view import View


class Application(object):

    def __init__(self, user_interface):                 #ViewABC?
        self.ui = user_interface

    def run(self):
        self.ui.run_main_loop()


def main():
    view = View()
    application = Application(view)
    application.run()


if __name__ == "__main__":
    main()
