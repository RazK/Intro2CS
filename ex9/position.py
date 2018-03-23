from vector import *

class Position(Vector):
    """
    Represents a location on the screen that can be changed by adding vectors.
    The position knows the screen limits and will overlap instead of exceeding.
    :param initial_x:       my initial x
    :param initial_y:       my initial y
    :param screen_min_x:    screen minimal x
    :param screen_min_y:    screen minimal y
    :param screen_max_x:    screen maximal x
    :param screen_max_y:    screen maximal y
    """
    def __init__(self, initial_x, initial_y,
                 screen_min_x=None, screen_min_y=None,
                 screen_max_x=None, screen_max_y=None):
        super(Position, self).__init__(initial_x, initial_y)
        self.__screen_min_x = screen_min_x
        self.__screen_min_y = screen_min_y
        self.__screen_max_x = screen_max_x
        self.__screen_max_y = screen_max_y

        # If initialized with screen limits - overlap
        if not (self.__screen_min_x == None and self.__screen_max_x == None and
                self.__screen_min_y == None and self.__screen_max_y == None):
            self.__screen_x_size = screen_max_x - screen_min_x
            self.__screen_y_size = screen_max_y - screen_min_y
            self.__overlap()


    def __add__(self, vector):
        """
        Linear addition with another vector.
        ResultPosition = (x1 + x2, y1 + y2)
        :param other:   Vector - vector to add
        :return:        Position - result of linear addition
        """
        new_pos_vector = super(Position, self).__add__(vector)
        return Position(new_pos_vector.get_x(),
                        new_pos_vector.get_y(),
                        self.__screen_min_x, self.__screen_min_y,
                        self.__screen_max_x, self.__screen_max_y)


    def __sub__(self, other):
        """
        Return the distance between two points.
        :param other:   Position object
        :return:        Positive float - distance between the two points
        """
        distance_vector = super(Position, self).__sub__(other)
        return distance_vector.get_size()


    def __overlap(self):
        """
        Change the position to be within the screen if exceeding it.
        """
        self._Vector__x = (self._Vector__x - self.__screen_min_x) % \
                   self.__screen_x_size + \
                   self.__screen_min_x
        self._Vector__y = (self._Vector__y - self.__screen_min_y) % \
                   self.__screen_y_size + \
                   self.__screen_min_y