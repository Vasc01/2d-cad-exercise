from abc import ABC, abstractmethod


class ModelABC(ABC):

    @abstractmethod
    def attach(self, observer):
        raise NotImplementedError

    @abstractmethod
    def detach(self, observer):
        raise NotImplementedError

    @abstractmethod
    def notify(self):
        raise NotImplementedError

    # @abstractmethod
    # def set_transformer(self, transformer):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def move(self, *args):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def rotate(self, *args):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def mirror(self, *args):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def scale(self, *args):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def fill(self, *args):
    #     raise NotImplementedError
