from gameobject import *
from position import *

class Asteroid(GameObject):
    """
    Represents an Asteroid Game Object.
    """
    def __init__(self, size, initial_pos, initial_speed,
                 radius_size_factor, radius_normal_factor):
        """
        Initialize a new asteroid with the given arguments.
        :param size:                    int - asteroid size from [1,2,3]
        :param initial_pos:             Position class - my pos, screen borders
        :param initial_speed:           Vector - starting speed
        :param radius_size_factor:      int - radius multiplication factor
        :param radius_normal_factor:    int - radius addition factor
        """
        radius = size * radius_size_factor + radius_normal_factor
        super().__init__(radius, initial_pos, initial_speed)
        self.__size = size


    def get_size(self):
        """
        Returns the asteroid size - one of [1,2,3]
        :return: int - asteroid size from [1,2,3]
        """
        return self.__size