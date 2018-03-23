#!python3
#############################################################
# FILE : hello_turtle.py
# WRITER : Raz Karl , razkarl , 311143127
# EXERCISE : intro2cs ex1 2016-2017
# DESCRIPTION: A set of functions to draw flowers using 
# turtle.
#############################################################

import turtle

def intro_test():
    """This is only a test method for printing hello"""
    print ("hello")

def draw_petal():
    """Draws a single petal. Pen state (up/down) should be set before calling this method."""
    turtle.forward(30)
    turtle.left(45)
    turtle.forward(30)
    turtle.left(135)
    turtle.forward(30)
    turtle.left(45)
    turtle.forward(30)
    turtle.left(135)

def draw_flower():
    """Draws a single flower. Turtle finishes in the bottom of the flower, facing down."""
    turtle.right(45)
    draw_petal()
    turtle.right(90)
    draw_petal()
    turtle.right(90)
    draw_petal()
    turtle.right(90)
    draw_petal()
    turtle.right(135)
    turtle.forward(150)

def draw_flower_advanced():
    """Draws a single flower. Turtle finishes in the correct position for drawing a new flower to the left."""
    draw_flower()
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

if(__name__ == "__main__"):
    """Boilerplate for testing my code from a shell"""
    #intro_test()
    #draw_petal()
    #draw_flower()
    #draw_flower_advanced()
    draw_flower_bed()
