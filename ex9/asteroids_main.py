from screen import Screen
import sys
from random import randint, uniform
from ship import *
from asteroid import *
from torpedo import *
from vector import *
from speed import *
from position import *
from copy import deepcopy

###############################################################################
# Constants
###############################################################################

# Game defaults
DEFAULT_ASTEROIDS_NUM   = 3
DEFAULT_FRACTIONS_NUM   = 10 # Number of fractions resulting from
                            # torpedo collision

# Constants
CLOCKWISE               =  1
COUNTERCLOCKWISE        = -1
DEGREES_IN_CIRCLE       = 360

# Messages
TITLE_GAMEOVER     = "Game Over!"
TITLE_COLLISION    = "Asteroid Collision!"
MESSAGE_COLLISION  = "Don't drink and drive in space..."
MESSAGE_VICTORY    = "All asteroids were destroyed! Well done."
MESSAGE_EXIT       = "Thanks for playing, come back soon!"
MESSAGE_SHIP_DIED  = "You ran out of lives. Try harder!"

# Ship defaults
SHIP_RADIUS             =  1
SHIP_INITIAL_HEADING    =  0
SHIP_MAX_LIVES          =  3
SHIP_MAX_TORPEDOS       = 15
SHIP_ACCELERATION       =  1
SHIP_MAX_SPEED          =  3
SHIP_TURN_DEGREES       =  7

# Asteroid defaults
ASTEROID_INITIAL_SIZE           =  3
ASTEROID_MAX_SPEED              =  2
ASTEROID_RADIUS_SIZE_FACTOR     = 10
ASTEROID_RADIUS_NORMAL_FACTOR   =  5
ASTEROID_SIZE_DESTROYED         =  0
ASTEROID_SIZES_2_POINTS         = { 1 : 20,
                                    2 : 50,
                                    3 : 100 }


# Torpedo constants
TORPEDO_RADIUS        =   4
TORPEDO_ACCELERATION  =   2
TORPEDO_TURNS_TO_LIVE = 200 # number of main loop interations
                            # until the torpedo is terminated

# Kaboom torpedo
KABOOM_SPEED    = Speed(0, 0, 0)
KABOOM_HEADING  = 0
KABOOM_TORPEDO  = Torpedo(0, 0, 0,
                          KABOOM_SPEED,
                          KABOOM_HEADING,
                          TORPEDO_ACCELERATION)

###############################################################################
# Class definition
###############################################################################
class GameRunner:

    def __init__(self, asteroids_amnt, num_of_fractions):
        self._screen = Screen()

        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y

        self.__score = 0
        self.__kaboom = False
        self.__asteroid_fractions = num_of_fractions

        # Initialize ship, asteroids, torpedoes
        self.__asteroids = set()
        self.__torpedoes = set()
        self.__initialize_ship()
        self.__initialize_asteroids(asteroids_amnt)

        # Initialize collision sets
        self.__asteroids_to_remove      = set()
        self.__asteroids_hit_by_torpedo = set()
        self.__torpedoes_to_remove      = set()
        self.__torpedoes_expired        = set()


    def run(self):
        self._do_loop()
        self._screen.start_screen()


    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop,5)


    def __get_random_position(self):
        # Randomize (x,y)
        y = randint(self.screen_min_y, self.screen_max_y)
        x = randint(self.screen_min_x, self.screen_max_x)

        # Create position object
        return Position(x, y,
                        self.screen_min_x, self.screen_min_y,
                        self.screen_max_x, self.screen_max_y)


    def __get_intersecting_asteroid(self, obj):
        """
        Return the first asteroid that intersects with the given object.
        Return None if no intersections exist.
        :param obj: GameObject - object to check intersections for
        :return:    GameObject - The first intersecting object from
                    game_objects if exists,
                    otherwise None.
        """
        # Check for collisions with every asteroid
        for asteroid in self.__asteroids:
            if obj.has_intersection(asteroid):
                # Collision - break and try another position
                return asteroid

        # No collisions - return
        return None


    def __initialize_ship(self):
        """
        Create the ship at a random position on the screen.
        Does not check for collisions.
        """
        # Ship starts not moving
        speed = Speed(0, 0, SHIP_MAX_SPEED)

        # Spawn at a random location
        pos = self.__get_random_position()

        # Generate the ship
        self.__ship = Ship(SHIP_RADIUS,
                           SHIP_MAX_LIVES,
                           SHIP_MAX_TORPEDOS,
                           pos,
                           SHIP_TURN_DEGREES,
                           SHIP_ACCELERATION,
                           speed,
                           SHIP_INITIAL_HEADING)


    def __initialize_asteroids(self, asteroids_amnt):
        """
        Create a bunch of asteroids at random positions on the screen.
        Asteroids will not be placed on the ship or on each other.
        """
        for asteroid in range(asteroids_amnt):
            # Generate random speed for the asteroid
            x_speed = uniform(-1 * ASTEROID_MAX_SPEED, ASTEROID_MAX_SPEED)
            y_speed = uniform(-1 * ASTEROID_MAX_SPEED, ASTEROID_MAX_SPEED)
            speed = Speed(x_speed, y_speed, ASTEROID_MAX_SPEED)

            # Spawn at new positions until not colliding with anything
            while (True):
                # Pick a random position
                pos = self.__get_random_position()

                # Create a new asteroid there
                new_asteroid = Asteroid(ASTEROID_INITIAL_SIZE,
                                        pos,
                                        speed,
                                        ASTEROID_RADIUS_SIZE_FACTOR,
                                        ASTEROID_RADIUS_NORMAL_FACTOR)

                # Check for collisions with other game objects
                if (new_asteroid.has_intersection(self.__ship) or
                    self.__get_intersecting_asteroid(new_asteroid)):
                    continue

                # If no collisions - break the while
                break

            self.__asteroids.add(new_asteroid)
            self._screen.register_asteroid(new_asteroid, ASTEROID_INITIAL_SIZE)


    def __split_all(self):
        """
        Hidden method: split all asteroids on the screen!
        """
        for asteroid in self.__asteroids:
            self.__kaboom = True


    def __shoot(self):
        """
        Shoots a torpedo from the ship forward if max_torpedoes not exceeded.
        """
        if len(self.__torpedoes) < SHIP_MAX_TORPEDOS:
            ship_pos     = self.__ship.get_pos()
            ship_speed   = self.__ship.get_speed()
            ship_heading = self.__ship.get_heading()
            torpedo = Torpedo(TORPEDO_TURNS_TO_LIVE, TORPEDO_RADIUS, ship_pos,
                              ship_speed, ship_heading, TORPEDO_ACCELERATION)
            self._screen.register_torpedo(torpedo)
            self.__torpedoes.add(torpedo)


    def __draw_all_objects(self):
        """
        Draw all existing game objects on the screen
        """
        # Draw Ship
        self._screen.draw_ship(*self.__ship.get_orientation())

        # Draw Asteroids
        for asteroid in self.__asteroids:
                self._screen.draw_asteroid(asteroid,
                                           *asteroid.get_pos().get_xy())
        # Draw torpedoes
        for torpedo in self.__torpedoes:
                self._screen.draw_torpedo(torpedo,
                                          *torpedo.get_orientation())


    def __handle_keyboard(self):
        """
        Handle key presses from the user
        """
        if (self._screen.is_left_pressed()):
            self.__ship.turn(SHIP_TURN_DEGREES * CLOCKWISE)

        if (self._screen.is_right_pressed()):
            self.__ship.turn(SHIP_TURN_DEGREES * COUNTERCLOCKWISE)

        if (self._screen.is_up_pressed()):
            self.__ship.accelerate()

        if (self._screen.is_space_pressed()):
            self.__shoot()

        if (self._screen.is_special_pressed()):
            self.__split_all()

        if (self._screen.should_end()):
            self.__gameover(MESSAGE_EXIT)


    def __move_all_objects(self):
        """
        Move all existing game objects according to their position and speed
        """
        self.__ship.move()
        for asteroid in self.__asteroids:
            asteroid.move()
        for torpedo in self.__torpedoes:
            torpedo.move()


    def __detect_collisions(self):
        """
        Creates sets for all important types of object collisions,
        or for 'Kaboom' collision if initiated.
        Those object should be removed by a different method.
        """
        self.__asteroids_to_remove.clear()
        self.__asteroids_hit_by_torpedo.clear()
        self.__torpedoes_to_remove.clear()

        # Collect sets of collided objects
        for asteroid in self.__asteroids:

            # If kaboom collision was initiated - all asteroids go KABOOM!
            if (self.__kaboom):
                self.__asteroids_hit_by_torpedo.add((asteroid,
                                                     KABOOM_TORPEDO))

            # Otherwise actually check for collisions and stuff
            else:
                # Asteroids * Torpedoes
                for torpedo in self.__torpedoes:
                    if (torpedo.has_intersection(asteroid)):
                        self.__torpedoes_to_remove.add(torpedo)
                        self.__asteroids_hit_by_torpedo.add((asteroid,
                                                             deepcopy(torpedo)))

                # Asteroids * Ship
                if asteroid.has_intersection(self.__ship) and \
                   asteroid not in self.__asteroids_hit_by_torpedo:
                    self.__asteroids_to_remove.add(asteroid)

        # Turn off kaboom mode
        self.__kaboom = False


    def __handle_collisions(self):
        """
        Updates game according to detected collisions:
            asteroid * ship:
                ship looses life
        <------ game over if ship is dead
            asteroid * torpedo
        <------ game over if this was the last asteroid
                torpedo terminated
                asteroid 'splits' to two smaller ones!
            other:
                ignore
        :return:
        """
        # Get the collision sets ready
        self.__detect_collisions()

        for asteroid in self.__asteroids_to_remove:
            self.__remove_life()
            self.__remove_asteroid(asteroid)

        for asteroid, torpedo_speed in self.__asteroids_hit_by_torpedo:
            self.__split_asteroid(asteroid, torpedo_speed)

        for torpedo in self.__torpedoes_to_remove:
            self.__remove_torpedo(torpedo)


    def __handle_expired_torpedoes(self):
        """
        Advances torpedoes turns and removes expired ones.
        """
        for torpedo in self.__torpedoes:
            if (torpedo.is_expired()):
                self.__torpedoes_expired.add(torpedo)
            else:
                torpedo.decrease_turns_left()

        for torpedo in self.__torpedoes_expired:
            self.__remove_torpedo(torpedo)


    def __remove_life(self):
        """
        Inflict damage to ship (hit by asteroid)
        Game Over if ship dies!
        """
        self._screen.remove_life()
        self.__ship.remove_life()
        if self.__ship.is_dead():
            self.__gameover(MESSAGE_SHIP_DIED)
        else:
            self._screen.show_message(TITLE_COLLISION, MESSAGE_COLLISION)


    def __remove_torpedo(self, torpedo):
        """
        Removes a torpedo from the game (if exists).
        DO NOT USE WHILE ITERATING OVER self.__torpedoes!
        :param torpedo: Torpedo to remove
        """
        if torpedo in self.__torpedoes:
            self._screen.unregister_torpedo(torpedo)
            self.__torpedoes.remove(torpedo)


    def __split_asteroid(self, asteroid, torpedo):
        """
        Adds score according to asteroid size.
        Creates two smaller asteroids if the given asteroid is not too
        small.
        Removes the given asteroid from the game.
        DO NOT USE WHILE ITERATING OVER self.__asteroids!
        :param asteroid:        Asteroid to split from
        :param torpedo:         The hitting torpedo
        """
        # Add score according to asteroid size
        self.__score += ASTEROID_SIZES_2_POINTS[asteroid.get_size()]
        self._screen.set_score(self.__score)

        # Split asteroid to fractions if it's not too small
        fraction_size = asteroid.get_size() - 1
        if fraction_size > ASTEROID_SIZE_DESTROYED:
            # Create fractions of the asteroid
            # Using speed's overloaded '**' operator to calculate collision
            # speed:
            base_fraction_speed = asteroid.get_speed() ** torpedo.get_speed()
            fraction_pos        = asteroid.get_pos()
            for fraction_num in range(self.__asteroid_fractions):
                # Fractions fly in different directions around a circle
                # Calculate the direction of the current fraction and build
                # the fraction speed
                fraction_rotation = ((DEGREES_IN_CIRCLE /
                                      self.__asteroid_fractions)) * fraction_num
                fraction_speed = deepcopy(base_fraction_speed)
                fraction_speed.rotate(fraction_rotation)

                # Create a new fraction of the asteroid
                fraction = Asteroid(fraction_size,
                                    fraction_pos,
                                    fraction_speed,
                                    ASTEROID_RADIUS_SIZE_FACTOR,
                                    ASTEROID_RADIUS_NORMAL_FACTOR)

                # Add the fraction to the game
                self.__asteroids.add(fraction)
                self._screen.register_asteroid(fraction, fraction_size)

        # Remove the asteroid from the game
        self.__remove_asteroid(asteroid)


    def __remove_asteroid(self, asteroid):
        """
        Removes an asteroid from the game.
        DO NOT USE WHILE ITERATING OVER self.__asteroids!
        :param asteroid: Asteroid to remove
        """
        if asteroid in self.__asteroids:
            self.__asteroids.remove(asteroid)
            self._screen.unregister_asteroid(asteroid)

            # if this was the last asteroid - Game Over
            if len(self.__asteroids) == 0:
                self.__gameover(MESSAGE_VICTORY)


    def _game_loop(self):
            # Respond to keyboard presses
            self.__handle_keyboard()

            # Move all objects
            self.__move_all_objects()

            # Do what needs to be done (KABOOM!)
            self.__handle_collisions()

            # Remove expired torpedoes
            self.__handle_expired_torpedoes()

            # Draw all objects
            self.__draw_all_objects()


    def __gameover(self, message):
        """
        Prints game results and exists.
        :param message: game over message to print
        """
        message += "\nScore: {0}".format(self.__score)
        self._screen.show_message(TITLE_GAMEOVER, message)
        self._screen.end_game()
        sys.exit()

def main(amnt, fractions):
    runner = GameRunner(amnt, fractions)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        main( int( sys.argv[1] ), int( sys.argv[2]) )
    elif len(sys.argv) > 1:
        main(int(sys.argv[1]), DEFAULT_FRACTIONS_NUM)
    else:
        main(DEFAULT_ASTEROIDS_NUM, DEFAULT_FRACTIONS_NUM)
