"""A middle layer between the frontend and the backend

This module provides single point of communication with the backend. On the side of the frontend there can be
multiple references to classes in this module. For example a command can be activated with keyboard
shortcut or by pressing a button wit the mouse -  they both will address the same class here.
"""


from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class MoveCommand(Command):

    def __init__(self, component, delta_x, delta_y):
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
