# Importation
from turtle import *

import time

from random import choice

from freegames import floor, vector

import idk  # Random Maze Code
import numpy as np

# Initialisation

maze = idk.maze
hehe = np.array(maze)
hehe = hehe.flatten()
# print(maze)


# print(hehe)
state = {'score': 0}

path = Turtle(visible=False)
writer = Turtle(visible=False)

# Velocity = {in Pos X} 5px per sec
aim = vector(5, 0)

# Spawn Location
our_user = vector(-180, 180)

# Opponents and their Velocity and Spawn Locations(if req)
opponents = [
    # [vector(-180, 160), vector(5, 0)],
    # [vector(-180, -160), vector(0, 5)],
    # [vector(100, 160), vector(0, -5)],
    # [vector(100, -160), vector(-5, 0)],
]

# updating the spawn location of the user to make sure it is not out of bonds.
hehe[0] = hehe[1] = 1
tiles = hehe  # tiles is the map of our game in 1d (20x20)


'''
Sample Map
tiles = [                                             
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
'''


def world():
    bgcolor('cyan')
    path.color('pink')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)  # Draw Square Path


def square(x, y):
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

# returns the next index in which the pacman / ghosts will be moving.


def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

# returns True if the next tile is valid for movement.


def valid(point):
    index = offset(point)

    try:
        if tiles[index] == 0:
            return False

    # Game Over Screen
    except IndexError:  # Handling the exception since when the user reaches the exit, we face an IndexError
        writer.goto(-150, 100)
        writer.write('Your Score was : ' +
                     str(state['score']), font=("Times New Roman", 30, "italic"))

        writer.goto(-200, -50)
        writer.write('Game Over!', font=(
            "Times New Roman", 60, "bold"))

        done()

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

# used For controlling the movement of the user and opponents.


def move():
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(our_user + aim):
        our_user.move(aim)

    index = offset(our_user)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(our_user.x + 10, our_user.y + 10)
    dot(15, 'black')  # Appearance of our user

    for point, course in opponents:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    # Condition to end game when user collides with the opponents
    for point, course in opponents:
        if abs(our_user - point) < 20:
            return

    ontimer(move, 100)

# Updates while execution by passing direction vectors acc to user
# which we further pass onto move() function


def change(x, y):
    if valid(our_user + vector(x, y)):
        aim.x = x
        aim.y = y


setup(600, 600, 500, 120)  # Size of the GUI

tracer(False)
writer.goto(200, 160)
writer.color('black')

hideturtle()
writer.write(state['score'])

listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()

done()
