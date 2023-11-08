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


class RotateCommand(Command):

    def __init__(self, component, theta):
        self.component = component
        self.theta = theta

    def execute(self):
        self.component.rotate(self.theta)


class MirrorCommand(Command):

    def __init__(self, component, axis):
        self.component = component
        self.axis = axis

    def execute(self):
        self.component.mirror(self.axis)


class ScaleCommand(Command):

    def __init__(self, component, factor_x, factor_y):
        self.component = component
        self.factor_x = factor_x
        self.factor_y = factor_y

    def execute(self):
        self.component.scale(self.factor_x, self.factor_y)
