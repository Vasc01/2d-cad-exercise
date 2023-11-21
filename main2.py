from frontend.view import UserInterface


class Application(object):

    def __init__(self, user_interface):                 #ViewABC?
        self.ui = user_interface

    def run(self):
        self.ui.initiate_windows()
        self.ui.main_loop()


def main():
    application = Application(UserInterface)
    application.run()


if __name__ == "__main__":
    main()
