############################################################
# Helper class
############################################################
import ship_helper

class Direction:
    """
    Class representing a direction in 2D world.
    You may not change the name of any of the constants (UP, DOWN, LEFT, RIGHT,
     NOT_MOVING, VERTICAL, HORIZONTAL, ALL_DIRECTIONS), but all other
     implementations are for you to carry out.
    """
    UP      = "UP"
    DOWN    = "DOWN"
    LEFT    = "LEFT"
    RIGHT   = "RIGHT"

    NOT_MOVING = "NOT MOVING"

    VERTICAL    = (UP, DOWN)
    HORIZONTAL  = (LEFT, RIGHT)

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

    OPPOSITES = {UP    : DOWN,
                 DOWN  : UP,
                 LEFT  : RIGHT,
                 RIGHT : LEFT}

    POSITIVES = {UP    : DOWN,
                 DOWN  : DOWN,
                 LEFT  : RIGHT,
                 RIGHT : RIGHT}

    STEPS = {UP    : ( 0 ,-1 ),
             DOWN  : ( 0 , 1 ),
             LEFT  : (-1 , 0 ),
             RIGHT : ( 1 , 0 )}

    @staticmethod
    def opposite(direction):
        """
        Return the oppsite direction.
        """
        return Direction.OPPOSITES[direction]

    @staticmethod
    def positive(direction):
        """
        Returns the positive direction in the same axis as the given direction
        Positives: 
            VERTICAL    : DOWN
            HORIZONTAL  : RIGHT
        """
        return Direction.POSITIVES[direction]

    @staticmethod
    def step(direction):
        """
        Return a tuple (dx, dy) represnting the changes in X and Y resulting
        from taking a step in the given direction.
        """
        return Direction.STEPS[direction]


############################################################
# Class definition
############################################################

class Ship:
    """
    A class representing a ship in Battleship game.
    A ship is 1-dimensional object that could be laid in either horizontal or
    vertical alignment. A ship sails on its vertical\horizontal axis back and
    forth until reaching the board's boarders and then changes its direction to
    the opposite (left <--> right, up <--> down).
    If a ship is hit in one of its coordinates, it ceases its movement in all
    future turns.
    A ship that had all her coordinates hit is considered terminated.
    """
    
    # Pos constants (x,y)
    X = 0 # pos[X] = pos[0]
    Y = 1 # pos[Y] = pos[1]

    def __init__(self, pos, length, direction, board_size):
        """
        A constructor for a Ship object
        :param pos: A tuple representing The ship's head's (x, y) position
        :param length: Ship's length
        :param direction: Initial direction in which the ship is sailing
        :param board_size: Board size in which the ship is sailing
        """
        self.__pos              = pos
        self.__length           = length
        self.__direction        = direction
        self.__board_size       = board_size
        self.__is_ship_hit      = False
        self.__is_cell_hit_list = [False] * length
        self.__steps_until_edge = self.__calc_steps_until_edge()

    def __calc_steps_until_edge(self):
        """
        Return the number of moves the ship can take until it reaches an edge.
        :param pos: A tuple representing The ship's head's (x, y) position
        :param length: Ship's length
        :param direction: Initial direction in which the ship is sailing
        :param board_size: Board size in which the ship is sailing
        """
        if self.__direction in Direction.VERTICAL:
            if self.__direction == Direction.UP:
                return self.__pos[Ship.Y]
            elif self.__direction == Direction.DOWN:
                return self.__board_size - (self.__pos[Ship.Y] + self.__length)
        
        elif self.__direction in Direction.HORIZONTAL:
            if self.__direction == Direction.LEFT:
                return self.__pos[Ship.X]
            elif self.__direction == Direction.RIGHT:
                return self.__board_size - (self.__pos[Ship.X] + self.__length)


    def get_direction(self):
        """
        Return the Ship's moving direction.
        :return: Ship's moving direction, or NOT_MOVING if the ship was hit.
        """
        if self.__is_ship_hit:
            return Direction.NOT_MOVING
        return self.__direction


    def __repr__(self):
        """
        Return a string representation of the ship.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)).
        The tuple's content should be (in the exact following order):
            1. A list of all the ship's coordinates.
            2. A list of all the ship's hit coordinates.
            3. Last sailing direction.
            4. The size of the board in which the ship is located.
        """
        return str((self.coordinates(), 
                    self.damaged_cells(), 
                    ship_helper.direction_repr_str(Direction,
                                                   self.get_direction()),
                    self.__board_size))


    def move(self):
        """
        Make the ship move one board unit.
        Movement is in the current sailing direction, unless such movement would
        take the ship outside of the board, in which case the ship switches
        direction and sails one board unit in the new direction.
        :return: A direction object representing the current movement direction.
        """

        # Only move if not hit yet
        if not self.__is_ship_hit:
            if self.__steps_until_edge == 0:
                self.__direction = Direction.opposite(self.__direction)
                self.__steps_until_edge = self.__calc_steps_until_edge()

            # Move one step in sailing direction
            dx, dy = Direction.step(self.__direction)
            self.__pos = (self.__pos[Ship.X]+dx, self.__pos[Ship.Y]+dy)
            self.__steps_until_edge -= 1

        return self.get_direction()


    def hit(self, pos):
        """
        Inform the ship that a bomb hit a specific coordinate. The ship updates
         its state accordingly.
        If one of the ship's body's coordinate is hit, the ship does not move
         in future turns. If all ship's body's coordinate are hit, the ship is
         terminated and removed from the board.
        :param pos: A tuple representing the (x, y) position of the hit.
        :return: True if the bomb generated a new hit in the ship, False
         otherwise.

        """
        # Check if the bomb is within the ship
        ship_coordinates = self.coordinates()
        if pos in ship_coordinates:
            hit_cell = ship_coordinates.index(pos)

            # Check if the hit cell was not already hit
            if not self.__is_cell_hit_list[hit_cell]:
                self.__is_ship_hit = True
                self.__is_cell_hit_list[hit_cell] = True
                return True

        # If bomb did not hit a new cell within the ship - False
        return False


    def terminated(self):
        """
        :return: True if all ship's coordinates were hit in previous turns, 
        False otherwise.
        """
        return not (False in self.__is_cell_hit_list)


    def __contains__(self, pos):
        """
        Check whether the ship is found in a specific coordinate.
        :param pos: A tuple representing the coordinate for check.
        :return: True if one of the ship's coordinates is found in the given
        (x, y) coordinate, False otherwise.
        """
        return pos in self.coordinates()

        
    def coordinates(self):
        """
        Return ship's current coordinates on board.
        :return: A list of (x, y) tuples representing the ship's current
        occupying coordinates.
        """
        return self.positions_from(self.__pos,
                                   range(self.__length),
                                   Direction.positive(self.__direction))

    def damaged_cells(self):
        """
        Return the ship's hit positions.
        :return: A list of tuples representing the (x, y) coordinates of the
         ship which were hit in past turns (If there are no hit coordinates,
         return an empty list). There is no importance to the order of the
         values in the returned list.
        """
        hit_indexes = [i for i, is_hit in enumerate(self.__is_cell_hit_list) 
                       if is_hit]
        return self.positions_from(self.__pos,
                                   hit_indexes,
                                   Direction.positive(self.__direction))

    def positions_from(self, pos, steps, direction):
        """
        Return a list of all the positions with the given steps to a specified 
        direction from pos.
        :param pos:         tuple representing the starting coordinate.
        :param steps:       list of steps to take starting from pos
        :param direction:   direction in which the steps should be taken
        :return:            list of position generated from taking the steps in the
                            specified direction starting from pos 
        Examples:
            pos = (0,0)
            steps = [1,2,3,5]
            direction = RIGHT
            --> [(0,1),(0,2),(0,3),(0,5)]

            pos = (3,2)
            steps = [1,3,5]
            direction = UP
            --> [(3,1), (3,-1), (3,-3)]
        """
        # Get the position dif between two steps
        dx, dy = Direction.step(direction)

        # List all steps from the given pos
        return [(pos[Ship.X]+(step*dx) , pos[Ship.Y]+(step*dy)) for step in steps]


    def direction(self):
        """
        Return the ship's current sailing direction.
        :return: One of the constants of Direction class :
         [UP, DOWN, LEFT, RIGHT] according to current sailing direction or
         NOT_MOVING if the ship is hit and not moving.
        """
        if self.__is_ship_hit:
            return Direction.NOT_MOVING
        return self.__direction
        

    def cell_status(self, pos):
        """
        Return the status of the given coordinate (hit\not hit) in current ship.
        :param pos: A tuple representing the coordinate to query.
        :return:
            if the given coordinate is not hit : False
            if the given coordinate is hit : True
            if the coordinate is not part of the ship's body : None 
        """
        if not self.__contains__(pos):
            return None

        dy = pos[Ship.Y] - self.__pos[Ship.Y]
        dx = pos[Ship.X] - self.__pos[Ship.X]
        cell_index = dy + dx  # Since the pos is validated to be contained 
                              # within the ship, either dx or dy is 0 and 
                              # therefore has no effect in the calculation - so 
                              # that only the desired distance is generated 
                              # (depending on the ship's direction).
        return self.__is_cell_hit_list[cell_index]

if __name__ == "__main__":
    s = Ship((3,3), 3, "Down", 5)
    print(s)
