#!python3
import turtle

def intro_test():
    """This is only a test method for printing hello"""
    print("hello")

def draw_petal(petal_thickness=0.5, petal_length=30):
    """Draws a single rectangular petal with the given length and thickness.
    Pen state (up/down) should be set before calling this method.
    @petal_thickness: between 1 to 0, 1 = square, 0 = line. default is 0.5.
    @petal_length: number specifying petal vertices length."""
    sharp_angle = 90 * petal_thickness
    blunt_angle = 180 - sharp_angle
    for side in range(2):
        turtle.left(blunt_angle)
        turtle.forward(petal_length)
        turtle.left(sharp_angle)
        turtle.forward(petal_length)

def draw_flower(petals=4, stem_length=150, petal_thickness=0.5, petal_length=30):
    """Draws a single flower with the given amount of petals and stem length.
    Turtle finishes in the bottom of the flower, facing down.
    @petals: amount of flowers (natural number).
    @stem_length: number specifying stem length.
    @petal_thickness: between 1 to 0, 1 = square, 0 = line. default is 0.5.
    @petal_length: number specifying petal vertices length."""
    start_angle = 90 * petal_thickness#360 / (petals * 2)
    end_angle = 90 - 90*petal_thickness#90 + start_angle
    turtle.right(start_angle)
    for petal in range(petals):
        draw_petal(petal_thickness, petal_length)
        turtle.right(360 / petals)
    turtle.right(end_angle)
    turtle.forward(stem_length)

def draw_flower_advanced():
    """Draws a single flower. Turtle finishes in the correct position for drawing a new flower to the left."""
    draw_flower(8,150,0.9,30)
    turtle.left(90)
    turtle.up()
    turtle.forward(150)
    turtle.left(90)
    turtle.forward(150)
    turtle.right(90)
    turtle.down()

def draw_flower_bed():
    """Draw 3 flowers side by side. Turtle finishes in the correct position for drawing another flower to the left."""
    turtle.up()
    turtle.left(180)
    turtle.forward(200)
    turtle.right(180)
    turtle.down()
    for flower in range(3):
        draw_flower_advanced()

if (__name__ == "__main__"):
    """Boilerplate for testing my code from a shell"""
    # intro_test()
    # draw_petal()
    # draw_flower()
    # draw_flower_advanced()
    draw_flower_bed()
