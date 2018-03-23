import position as position

class GameObject:
    """

    """
    def __init__(self, radius, initial_pos, initial_speed):
        """
        Initialize a new GameObject with the given arguments.
        :param radius:              int - object radius
        :param initial_pos:         Position class - my pos, screen borders
        :param time_unit:           int - game loop to real world time units
                                    conversion.
        :param initial_speed:       Vector - starting speed
        """
        self.__pos          = initial_pos
        self.__radius       = abs(radius)
        self.__speed        = initial_speed


    def __repr__(self):
        return "<{0}: radius {1} at {2} with {3}>".format(
            self.__class__.__name__, self.__radius, self.__pos, self.__speed)


    def get_pos(self):
        """
        Returns the object's position on the screen.
        :return: Position object
        """
        return  self.__pos


    def get_radius(self):
        """
        Return the object's radius.
        :return: positive int - object's radius
        """
        return self.__radius

    def get_speed(self):
        """
        Returns the object's speed.
        :return: Speed object
        """
        return  self.__speed

    def move(self):
        """
        Changes object's position according to it's current position and
        velocity.
        """
        self.__pos += self.__speed


    def has_intersection(self, obj):
        """
        Checks if the object collides with another GameObject.
        :param obj: GameObject
        :return:    True if objects collide, False otherwise
        """
        distance = self.get_pos() - obj.get_pos()
        return distance <= self.get_radius() + obj.get_radius()