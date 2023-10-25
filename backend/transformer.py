""" Transformer for coordinates in 2-dimensional space

There are multiple two-dimensional coordinate systems. Among them are:
    Barycentric coordinates
    Bipolar coordinates
    Elliptic coordinates
    Parabolic coordinates
    Polar coordinates
    Rectangular/Cartesian coordinates
    ...

At this stage implemented is the transformation with cartesian coordinates for the most basic
operations move, rotate, mirror and scale.

"""

from abc import ABC, abstractmethod

from math import radians
import numpy as np


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
    """ Transformer for rectangular coordinate system

    The class makes use of the homogeneous transformation rules - translation, rotation, reflection and scale
    are all represented by a 3x3 matrix multiplied by vector containing the point coordinates. It is
    also possible to execute transformations with user defined matrix.

    Attributes:
        reference_x (int/float): Allows transformation based on this point instead on coordinate system origin.
        reference_y (int/float): Allows transformation based on this point instead on coordinate system origin.
    """

    def __init__(self):
        self.reference_x = 0
        self.reference_y = 0

    def set_reference(self, x, y):
        self.reference_x = x
        self.reference_y = y
        return self

    def transform(self, x, y, matrix):
        """ Calculator for transformation

        Note:
            The calculator adjusts the original coordinates for transformation using the reference coordinates.

        Args:
            x (int/float): Original location of the point that will be transformed.
            y (int/float): Original location of the point that will be transformed.
            matrix (List): 3x3 transformation matrix.

        Returns:
            Tuple with two entries representing x and y coordinates of the new position.

        """
        transformation_matrix = np.array(matrix)
        old_coordinates = np.array([x, y, 1])
        reference_coordinates = np.array([self.reference_x, self.reference_y, 0])
        old_coordinates_adjusted = old_coordinates - reference_coordinates

        transformation_result = (transformation_matrix @ old_coordinates_adjusted) + reference_coordinates
        new_x, new_y, rest = transformation_result

        return new_x, new_y

    def move(self, x, y, delta_x, delta_y):
        """Planar translation

        The translation is relative to the original coordinates. Distance and direction of the translation
        are determined by the value and sign of the delta_x and delta_y parameters.

        Args:
            x (int/float): Original location of the point that will be transformed.
            y (int/float): Original location of the point that will be transformed.
            delta_x (int/float): Value for translation in x direction.
            delta_y (int/float):Value for translation in y direction.

        Returns:
            Call of the transform() function.
        """
        translation_matrix = [[1, 0, delta_x],
                              [0, 1, delta_y],
                              [0, 0, 1]]

        return self.transform(x, y, translation_matrix)

    def rotate(self, x, y, theta):
        """Planar rotation

        Args:
            x (int/float): Original location of the point that will be transformed.
            y (int/float): Original location of the point that will be transformed.
            theta (int/float): Value for rotation in degrees. Positive values cause counterclockwise rotation
        Returns:
            Call of the transform() function.
        """
        c = np.cos(radians(theta))
        s = np.sin(radians(theta))
        rotation_matrix = [[c, -s, 0],
                           [s,  c, 0],
                           [0, 0, 1]]

        return self.transform(x, y, rotation_matrix)

    def mirror(self, x, y, axis):
        """ Mirror coordinates with three options

        Available are three transformational matrices for mirroring around x-axis, y-agis and a point.

        Args:
            x (int/float): Original location of the point that will be transformed.
            y (int/float): Original location of the point that will be transformed.
            axis (str): Available options are "x", "y", "xy", which will activate the corresponding transformation.

        Returns:
            Call of the transform() function.

        """
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
        """Scale position in 2D-plane

        Scale the coordinates of a point based on their distance to a set point(by default the origin 0,0).
        For uniform scaling the factor in x-direction must be equal to the factor in y-direction. Otherwise the
        transformation results in distortion.

         Args:
            x (int/float): Original location of the point that will be transformed.
            y (int/float): Original location of the point that will be transformed.
            factor_x (int/float): Scaling factor in x-direction.
            factor_y (int/float): Scaling factor in y-direction.
         Returns:
            Call of the transform() function.
        """
        scale_matrix = [[factor_x, 0, 0],
                        [0, factor_y, 0],
                        [0, 0, 1]]

        return self.transform(x, y, scale_matrix)
