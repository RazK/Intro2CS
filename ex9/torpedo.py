from gameobject import *
from position import *

class Torpedo(GameObject):
    """
    Represents a Torpedo Game Object.
    """
    def __init__(self, tuns_left, radius, initial_pos, ship_speed, heading,
                 acceleration_size):
        """
        Initialize a new torpedo with the given arguments.
        :param heading:       int - torpedo heading in degrees
        :param initial_pos:   Position class - my pos, screen borders
        :param time_unit:     int - game loop to real world time units
                              conversion.
        :param initial_speed: Vector - starting speed
        """
        x_accel = math.cos(math.radians(heading)) * (acceleration_size)
        y_accel = math.sin(math.radians(heading)) * (acceleration_size)
        shooting_acceleration = Vector(x_accel, y_accel)
        torpedo_speed = ship_speed + shooting_acceleration

        super().__init__(radius, initial_pos, torpedo_speed)

        self.__turns_left = tuns_left
        self.__heading    = heading


    def get_orientation(self):
        """
        Returns a tuple with the objects's position and heading.
        :return: (x, y, heading)
        """
        x,y     = self.get_pos().get_xy()
        heading = self.__heading
        return (x,y,heading)


    def decrease_turns_left(self):
        """
        A turn had passed and this torpedo is one step closer to hell.
        """
        self.__turns_left -= 1

    def is_expired(self):
        """
        Returns the number of turns left for the torpedo in the game
        :return: int - number of turns
        """
        return self.__turns_left <= 0