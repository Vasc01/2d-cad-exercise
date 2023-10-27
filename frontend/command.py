from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class MoveCommand(Command):

    def __init__(self, component, delta_x, delta_y):
        """
        Receivers are Group or Canvas
        """
        self.component = component
        self.delta_x = delta_x
        self.delta_y = delta_y

    def execute(self):
        self.component.move(self.delta_x, self.delta_y)
