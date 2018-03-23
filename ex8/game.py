############################################################
# Imports
############################################################
import game_helper as gh


############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    # Bomb constants
    BOMB_LIFESPAN = 3  # Turns before bomb is removed


    class TurnStats:
        """
        A class representing statistics of a single turn in battlship game.
            hit_positions   - list of positions hit in this turn
            num_terminated  - number of ships terminated in this turn
        """
        def __init__(self):
            """
            Initializes a new TurnStatistics object.
            All statistics begin cleared.
            """
            self.clear()

        def clear(self):
            """
            clear hit positions and terminated ships counter
            """
            self.__hit_positions = []
            self.__num_terminated = 0

        def record_explosion(self, pos):
            """
            Add a new hit location (pos) to turn statistics
            :param pos: A tuple (x,y) representing the position bomb that
            exploded.
            """
            self.__hit_positions.append(pos)

        def record_termination(self):
            """
            Count another ship termination
            """
            self.__num_terminated += 1

        def get_explosion_positions(self):
            """
            Return the list of positions of bombs exploded this turn
            :return: list of exploded bomb positions
            """
            return self.__hit_positions

        def get_stats(self):
            """
            Returns a tuple with the numbers of terminated ships and bomb hits.
            :return: (terminated count, bomb hit count)
            """
            return (self.__num_terminated, len(self.__hit_positions))

        def report(self):
            """
            Report turn statistics to the user
            """
            gh.report_turn(len(self.__hit_positions), self.__num_terminated)


    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board.
        :param ships: A list of ships (of type Ship) that participate in the
            game.
        :return: A new Game object.
        """
        self.__board_size               = board_size
        self.__ships                    = ships
        self.__turn_stats               = Game.TurnStats()
        self.__hit_cells                = {} # {cell_position : number_of_ships}
        self.__bombs_pos_2_turns_left   = {} # {position : turns_left}


    def __place_bomb(self):
        """
        Asks the user for bomb coordinates and places a new bomb on the board.
        """
        # Get bomb coordinates from the user
        new_bomb_pos = gh.get_target(self.__board_size)

        # Place the new bomb on the board (+1 to lifespan because
        # it's decremented once by the end of this turn before it does anything)
        self.__bombs_pos_2_turns_left[new_bomb_pos] = Game.BOMB_LIFESPAN + 1


    def __move_ships(self):
        """
        Move all the ships and check if they bumped into bombs.
        Records all hits for statistics.
        """
        for ship in self.__ships:
            # All hail captain Sparrow!
            ship.move()

            # Check if the ship bumped into any of the existing bombs
            for bomb_pos in self.__bombs_pos_2_turns_left.keys():
                if ship.hit(bomb_pos):
                    # Record explosion for statistics
                    self.__turn_stats.record_explosion(bomb_pos)

                    # Record a new hit cell or add another hit on the same cell
                    if not bomb_pos in self.__hit_cells:
                        self.__hit_cells[bomb_pos] = 1
                    else:
                        self.__hit_cells[bomb_pos] += 1


    def __kaboom(self):
        """
        Update all bombs on the board to do one of the following:
            Get older   (nothing happened   - decrease turns left)
            Expire      (no turns left      - removed from the board)
            Explode     (hit with a ship    - removed from the board)
        :return:
        """
        # Update bombs
        for bomb_pos in list(self.__bombs_pos_2_turns_left.keys()):
            # Decrease turns left for all bombs
            self.__bombs_pos_2_turns_left[bomb_pos] -= 1

            # Remove expired and exploded bombs
            if self.__bombs_pos_2_turns_left[bomb_pos] == 0 or \
               bomb_pos in self.__turn_stats.get_explosion_positions():
                del self.__bombs_pos_2_turns_left[bomb_pos]


    def __clear_terminated(self):
        """
        Remove terminated ships from the board and update terminated count
        """
        for ship in self.__ships:
            if ship.terminated():
                # Remove the ship from the game
                self.__ships.remove(ship)

                # Clean the board hits list from all cells in this ship
                for pos in ship.coordinates():
                    self.__hit_cells[pos] -= 1

                    # If no hits remains in a certain cell - remove it
                    if self.__hit_cells[pos] == 0:
                        del self.__hit_cells[pos]

                # Increment terminations
                self.__turn_stats.record_termination()


    def __play_one_round(self):
        """
        The function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits and
             terminated ships)
        :return:
            (some constant you may want implement which represents) Game status :
            GAME_STATUS_ONGOING if there are still ships on the board or
            GAME_STATUS_ENDED otherwise.
        """
        # Clear turn statistics
        self.__turn_stats.clear()

        # User places a new bomb
        self.__place_bomb()

        # All ships move
        self.__move_ships()

        # All bombs get older, expire or explode
        self.__kaboom()

        # Print game state to the user
        self.__print_board()

        # Remove terminated ships from the board
        self.__clear_terminated()

        # Report turn statistics to the user
        self.__turn_stats.report()


    def __print_board(self):
        """
        Prints the game board to the user
        """
        print(gh.board_to_string(self.__board_size,
                                 self.__turn_stats.get_explosion_positions(),
                                 self.__bombs_pos_2_turns_left,
                                 self.__hit_cells.keys(),
                                 [coordinate for ship in self.__ships for
                                 coordinate in ship.coordinates()]))

    def __repr__(self):
        """
        Return a string representation of the board's game.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)). The tuple should contain (maintain
        the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board, mapping their
                coordinates to the number of remaining turns:
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        return repr((self.__board_size,
                    self.__bombs_pos_2_turns_left,
                    self.__ships))

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # Print the board legend
        gh.report_legend()

        # Print the initial board
        self.__print_board()

        # Play until all ships are terminated
        while self.__ships:
            self.__play_one_round()

        # Report the game is over
        gh.report_gameover()


############################################################
# An example usage of the game
############################################################
if __name__=="__main__":
    game = Game(5, gh.initialize_ship_list(4, 2))
    game.play()
