from frontend.view import UserInterface


class Application(object):

    def __init__(self, user_interface):
        self.ui = user_interface

    def run(self):
        self.ui.create_windows()


def main():
    application = Application(UserInterface)
    application.run()


if __name__ == "__main__":
    main()
