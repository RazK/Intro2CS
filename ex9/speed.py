from vector import *

class Speed(Vector):
    """
    Represents the speed of a GameObject, which is a vector with limits and
    polar representation.
    """
    def __init__(self, x_speed, y_speed, max_speed=0):
        """
        Initialize a Speed object.
        :param x_speed:     Initial x speed
        :param y_speed:     Initial y speed
        :param max_speed:   Maximal speed size an axis get have
        """
        super().__init__(x_speed, y_speed)
        self.__max_speed = max_speed
        self.__min_speed = -1 * max_speed


    def __add__(self, other):
        """
        Return the this vector by linear addition of another vector.
        :param other:   Vector - another vector to add
        """
        x_speed = self.get_x() + other.get_x()
        y_speed = self.get_y() + other.get_y()
        return Speed(x_speed, y_speed, self.get_max_speed())


    def __pow__(self, other):
        """
        Returns self speed after being hit by other's speed:
        speed1 + speed2 (vector addition) divided by
        speed1 - speed2 (size difference)
        :param other:   Speed - speed of hitting object
        :return:        Speed - new speed after collision
        """
        return (self + other) / ((self - other).get_size())


    def __within_limits(self, speed_arg):
        """
        Return the given speed_arg trimmed to the speed limit if exceeding.
         Example:   limit = 10, speed_arg = -12
                    returns -10
        :param speed_arg:   float - speed argument of an axis
        :return:            float - speed argument trimmed to limit
        """
        return min(self.__max_speed, max(self.__min_speed, speed_arg))


    def rotate(self, degrees):
        """
        Rotates the speed vector clockwise by the given degrees
        :param degrees: float - rotation angle in degrees
        """
        angle = self.get_angle_degrees()
        rotated_angle = angle + degrees
        speed_size = self.get_size()
        self._Vector__x = math.cos(rotated_angle) * speed_size
        self._Vector__y = math.sin(rotated_angle) * speed_size


    def get_angle_radians(self):
        """
        Return the vector angle in radians relative to X axis.
        :return: float - vector angle in radians
        """
        return math.atan2(self._Vector__y, self._Vector__x)


    def get_angle_degrees(self):
        """
        Return the vector angle in degrees relative to X axis.
        :return: int - vector angle in degrees
        """
        return math.degrees((self.get_angle_radians()))


    def get_max_speed(self):
        """
        Return the maximal speed
        :return: int - max speed possible for this object
        """
        return self.__max_speed