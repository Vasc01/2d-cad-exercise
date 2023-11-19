from abc import abstractmethod, ABC


class ViewABC(ABC):

    @abstractmethod
    def send_user_input(self):
        raise NotImplemented

    @abstractmethod
    def update_ui(self):
        raise NotImplemented


class UserInterface(ViewABC):

    def send_user_input(self):
        raise NotImplemented

    def update_ui(self):
        raise NotImplemented
