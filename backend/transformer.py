from abc import ABC, abstractmethod
from cmath import cos
from math import sin


class TransformerAbc(ABC):

    """
    from wikipedia.org
    B
    Barycentric coordinate system
    Bipolar coordinates
    E
    Elliptic coordinate system
    P
    Parabolic coordinate system
    Polar coordinate system
    R
    Rectangular coordinate system
    """

    @staticmethod
    @abstractmethod
    def move(*args):
        pass

    @staticmethod
    @abstractmethod
    def rotate(*args):
        pass

    @staticmethod
    @abstractmethod
    def mirror(*args):
        pass

    @staticmethod
    @abstractmethod
    def scale(*args):
        pass


class CartesianTransformer(TransformerAbc):

    @staticmethod
    def move(x, y, delta_x, delta_y):
        x += delta_x
        y += delta_y
        print("CartesianTransformer is moving things")
        return x, y

    @staticmethod
    def rotate():
        print("CartesianTransformer is rotating things")
        return None

    @staticmethod
    def mirror():
        print("CartesianTransformer is mirroring things")
        return None

    @staticmethod
    def scale():
        print("CartesianTransformer is scaling things")
        return None


class PolarTransformer(TransformerAbc):

    @staticmethod
    def move(x, y, r, angle):
        x = (x + r) * cos(angle)
        y = (y + r) * sin(angle)
        print("PolarTransformer is moving things")
        return x, y

    @staticmethod
    def rotate():
        print("PolarTransformer is rotating things")
        return None

    @staticmethod
    def mirror():
        print("PolarTransformer is mirroring things")
        return None

    @staticmethod
    def scale():
        print("PolarTransformer is scaling things")
        return None
