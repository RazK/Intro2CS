import math

class Vector:
    """
    Represents a vector in a 2D space.
    """
    def __init__(self, x=0, y=0):
        """
        Initialize a vector with x,y arguments.
        :param x:   int
        :param y:   int
        """
        self.__x = x
        self.__y = y


    def __mul__(self, scalar):
        """
        Multiply the vector by a scalar.
        ResultVector = (a * x1, a * y1)
        :param scalar:  float - a scalar
        :return:        Vector - result of scalar multiplication
        """
        x = self.get_x() * scalar
        y = self.get_y() * scalar
        return type(self)(x,y)


    def __truediv__(self, scalar):
        """
        Divide the vector by a scalar (multiply by 1/scalar)
        ResultVector = (1/a * x1, 1/a * y1)
        :param scalar:  float - a scalar
        :return:        Vector - result of scalar division
        """
        return self * (1 / scalar)


    def __add__(self, other):
        """
        Linear addition with another vector.
        ResultVector = (x1 + x2, y1 + y2)
        :param other:   Vector - vector to add
        :return:        Vector - result of linear addition
        """
        x = self.get_x() + other.get_x()
        y = self.get_y() + other.get_y()
        return type(self)(x,y)


    def __sub__(self, other):
        """
        Linear subtraction with of another vector.
        ResultVector = (x1 - x2, y1 - y2)
        :param other:   Vector - vector to subtract.
        :return:        Vector - result of linear subtraction.
        """
        return self + (other * -1)


    def __repr__(self):
        """
        Return a nice representation of the position
        :return: string representation of the position
        """
        return "{0}: [{1},{2}]".format(self.__class__.__name__,
                                       self.get_x(),
                                       self.get_y())


    def __eq__(self, other):
        """
        Check if two vectors are equal.
        :param other:   Vector object
        :return:        True if vectors are equal, False otherwise.
        """
        return self.get_x() == other.get_x() and self.get_y() == other.get_y()


    def get_x(self):
        """
        Return the x argument of the vector.
        :return: int - vector x argument
        """
        return self.__x


    def get_y(self):
        """
        Return the y argument of the vector.
        :return: int - vector y argument
        """
        return self.__y


    def get_xy(self):
        """
        Return a tuple (x,y) of the vector arguments
        :return: (x,y) - this vector's arguments
        """
        return (self.__x, self.__y)


    def get_size(self):
        """
        Returns sqrt(x^2 + y^2)
        :return: float - size of the vector
        """
        return math.hypot(self.__x, self.__y)