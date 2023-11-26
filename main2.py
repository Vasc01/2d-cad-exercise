from frontend.view import View


class Application(object):

    def __init__(self, user_interface):                 #ViewABC?
        self.user_interface = user_interface

    def run(self):
        self.user_interface.run_main_loop()


def main():
    view = View()
    application = Application(view)
    application.run()


if __name__ == "__main__":
    main()
