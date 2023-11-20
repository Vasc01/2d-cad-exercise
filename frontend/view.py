from abc import abstractmethod, ABC


class ViewABC(ABC):

    @abstractmethod
    def send_user_input(self):
        raise NotImplemented

    @abstractmethod
    def update_ui(self):
        raise NotImplemented


class UserInterface(ViewABC):

    def __init__(self, canvas_in):
        self.canvas_in = canvas_in

    def send_user_input(self):
        raise NotImplemented

    def update_ui(self):
        raise NotImplemented

    def load_canvas(self):
        self.canvas_in.clear()

        self.canvas_in.refresh()
