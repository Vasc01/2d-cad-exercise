from abc import ABC, abstractmethod

from math import sin, cos, radians
import numpy as np

# TODO: Use the Google docstring format to document classes, methods and functions


class TransformerAbc(ABC):

    @abstractmethod
    def move(self, *args):
        pass

    @abstractmethod
    def rotate(self, *args):
        pass

    @abstractmethod
    def mirror(self, *args):
        pass

    @abstractmethod
    def scale(self, *args):
        pass


class CartesianTransformer(TransformerAbc):
    """
    use of homogeneous transformation rules
    """

    def __init__(self):
        self.reference_x = 0
        self.reference_y = 0

    def set_reference(self, x, y):
        self.reference_x = x
        self.reference_y = y
        return self

    def transform(self, x, y, matrix):

        transformation_matrix_np = np.array(matrix)
        old_coordinates = np.array([x, y, 1])
        reference_coordinates = np.array([self.reference_x, self.reference_y, 0])
        old_coordinates_adjusted = old_coordinates - reference_coordinates

        transformation_result = (transformation_matrix_np @ old_coordinates_adjusted) + reference_coordinates
        new_x, new_y, rest = transformation_result

        return new_x, new_y

    def move(self, x, y, delta_x, delta_y):
        """
        relative movement by delta value
        direction determined by positive/negative value
        """
        translation_matrix = [[1, 0, delta_x],
                              [0, 1, delta_y],
                              [0, 0, 1]]

        return self.transform(x, y, translation_matrix)

    def rotate(self, x, y, theta):
        """
        theta in deg
        counterclockwise for positive values of theta
        """
        c = np.cos(radians(theta))
        s = np.sin(radians(theta))
        rotation_matrix = [[c, -s, 0],
                           [s,  c, 0],
                           [0, 0, 1]]

        return self.transform(x, y, rotation_matrix)

    def mirror(self, x, y, axis):

        mirror_matrix_center = [[-1, 0, 0],
                                [0, -1, 0],
                                [0, 0, 1]]

        mirror_matrix_x = [[1,  0, 0],
                           [0, -1, 0],
                           [0, 0, 1]]

        mirror_matrix_y = [[-1, 0, 0],
                           [0,  1, 0],
                           [0, 0, 1]]

        if axis == "xy":
            return self.transform(x, y, mirror_matrix_center)

        elif axis == "x":
            return self.transform(x, y, mirror_matrix_x)

        elif axis == "y":
            return self.transform(x, y, mirror_matrix_y)

        else:
            return x, y

    def scale(self, x, y, factor_x, factor_y):

        scale_matrix = [[factor_x, 0, 0],
                        [0, factor_y, 0],
                        [0, 0, 1]]

        return self.transform(x, y, scale_matrix)
