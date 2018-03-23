from gameobject import *
from position import *

class Ship(GameObject):
    """

    """
    def __init__(self, radius, lives, torpedo_limit, initial_pos, turn_degrees,
                 acceleration_size, initial_speed, initial_heading):
        """
        Initialize a new ship with the given arguments.
        :param radius:              int - ship radius
        :param lives:               int - number of lives
        :param torpedo_limit:       int - maximal number of torpedoes at any
                                    given time.
        :param initial_pos:         Position class - my pos, screen borders
        :param turn_degrees:        int - turn degrees per key press
        :param acceleration_size:   int - acceleration size per key press
        :param time_unit:           int - game loop to real world time units
                                    conversion.
        :param initial_speed:       Vector - starting speed
        :param initial_heading:     float - ship heading angle in degrees
        """
        super().__init__(radius, initial_pos, initial_speed)
        self.__lives                = lives
        self.__heading              = initial_heading
        self.__torpedo_limit        = torpedo_limit
        self.__turn_degrees         = turn_degrees
        self.__acceleration_size    = acceleration_size


    def get_heading(self):
        """
        Return the direction to which the ship is heading (in degrees)
        :return: ship direction in degrees
        """
        return self.__heading

    def get_orientation(self):
        """
        Returns a tuple with the objects's position and heading.
        :return: (x, y, heading)
        """
        x,y     = self.get_pos().get_xy()
        heading = self.__heading
        return (x,y,heading)


    def accelerate(self, acceleration_size=None):
        """
        ":param acceleration_size:
        Increases ship's velocity by it's default acceleration size
        new_speed = current_speed + acceleration * time_unit <= max_speed
        """
        if acceleration_size == None:
            acceleration_size = self.__acceleration_size

        x_accel = math.cos(math.radians(self.__heading)) * (acceleration_size)
        y_accel = math.sin(math.radians(self.__heading)) * (acceleration_size)
        acceleration = Vector(x_accel, y_accel)
        self._GameObject__speed += acceleration #* self._GameObject__time_unit


    def remove_life(self):
        """
        Ship life is reduced from a collision with an asteroid
        """
        self.__lives -= 1

    def is_dead(self):
        """
        Return True if ship is still alive, false otherwise.
        """
        return self.__lives <= 0

    def turn(self, degrees=None):
        """
        Change ship's velocity angle by the given size in degrees
        :param degrees:     integer (positive - clockwise, negative - ccw)
        :return:
        """
        if degrees == None:
            degrees = self.__turn_degrees

        self.__heading += degrees
