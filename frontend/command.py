"""A middle layer between the presenter and the backend

This module provides single point of communication with the backend. It returns information to the presenter
after execution of the command.
"""


from abc import ABC, abstractmethod


class Command(ABC):

    SUBSCRIBERS = []

    @staticmethod
    def attach(observer):
        if observer not in Command.SUBSCRIBERS:
            Command.SUBSCRIBERS.append(observer)

    @staticmethod
    def detach(observer):
        Command.SUBSCRIBERS.remove(observer)

    @staticmethod
    def notify(x, y):
        for subscriber in Command.SUBSCRIBERS:
            subscriber.update(x, y)

    @abstractmethod
    def execute(self):
        raise NotImplemented


class MoveCommand(Command):
    """Executes the move transformation.

    Attributes:
        component (Element/Group): Transformation is performed on this Element/Group
        delta_x (int): Relative movement in x-direction.
        delta_y (int): Relative movement in y-direction.
    """

    def __init__(self, component, delta_x, delta_y):
        self.component = component
        self.delta_x = delta_x
        self.delta_y = delta_y

    def execute(self):
        self.component.move(self.delta_x, self.delta_y)
        self.notify(self.component.x, self.component.y)


class RotateCommand(Command):
    """Executes the rotate transformation.

    Attributes:
        component (Element/Group): Transformation is performed on this Element/Group
        theta (int): Angle of rotation.
    """

    def __init__(self, component, theta):
        self.component = component
        self.theta = theta

    def execute(self):
        self.component.rotate(self.theta)
        self.notify(self.component.x, self.component.y)


class MirrorCommand(Command):
    """Executes the mirror transformation.

    Attributes:
        component (Element/Group): Transformation is performed on this Element/Group
        axis (int): Mirror direction.
    """

    def __init__(self, component, axis):
        self.component = component
        self.axis = axis

    def execute(self):
        self.component.mirror(self.axis)
        self.notify(self.component.x, self.component.y)


class ScaleCommand(Command):
    """Executes the scale transformation.

    Attributes:
        component (Element/Group): Transformation is performed on this Element/Group
        factor_x (int): Scale factor in x direction.
        factor_y (int): Scale factor in y direction.
    """

    def __init__(self, component, factor_x, factor_y):
        self.component = component
        self.factor_x = factor_x
        self.factor_y = factor_y

    def execute(self):
        self.component.scale(self.factor_x, self.factor_y)
        self.notify(self.component.x, self.component.y)
