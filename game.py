import turtle
import random
import math
from config import *

def game_screen(title ='Fun with Turtle' ):
    window = turtle.Screen()
    window.title(title)
    window.setup(width = WIDTH, height = HEIGHT)
    window.bgpic(BG_PIC)
    window.addshape(ROCKET)
    window.addshape(DSTAR)
    return window

# get new turtles
def new_turtle(size=(1,1), shape='classic',  angle=0, color=('black','black'), speed=0, pendown=False, pos=(0,0), hide=False):
    t=turtle.Turtle(shape)
    t.turtlesize(*size)
    t.speed(speed)
    t.color(*color)
    t.left( angle)
   
    t.penup()
    t.goto(*pos)
    if  pendown:
        t.pendown()
    if  hide:
        t.hideturtle()

    return t

def rand_pos():
    """return a random position of the deathstar"""
    alpha = random.randint(30,150)
    return math.cos(alpha/60)*100, math.sin(alpha/60)*100

def shoot():
    """turtles serve as cannonballs"""
    global shots
    if  shots > SHOTS_TIL_JAM:
        return
    shots += 1
    t = new_turtle(angle=cannon.heading(), size= CANNONBALL_SIZE, shape='circle', color=('red','yellow'), )
    cannonBalls.append(t)

def reload():
    global shots
    shots=0

def write_score():
    writer.undo()
    writer.write(score, font=FONT)

def is_close(x,y, err=10):
    return abs(x-y) < err

def out_of_square(x,y, dist=BULLETRANGE):
    return math.sqrt(x**2+y**2) > dist

def cannonball_loop():
    """update screen"""
    global score

#    if  block[1]: 
#        print('block 1')
#        return
#    block[1] = True
 
    for t in cannonBalls:
        t.forward(CANNONBALL_SPEED)

        if  is_close(t.pos(),rocket.pos()): # rocket is hit
            score+= SCORE['rocketship']
            rocket.goto(-MAX_X, ALTITUDE)
        if  is_close(t.pos(), deathstar.pos()): # deathstar is hit
            score+= SCORE['deathstar']
            deathstar.goto(rand_pos())
        if  out_of_square(*t.pos()): 
            cannonBalls.remove(t)
            t.clear()
            t.hideturtle()
            del t
   
    write_score()
    screen.update()

    if  running:
        turtle.ontimer(cannonball_loop, DELAY['cannonballs'])

def rocket_loop():
    """move rocketship"""  

    rocket.forward(SHIPSPEED)
    if  rocket.xcor() > MAX_X:
        rocket.goto(-MAX_X, ALTITUDE)
    if  running:
        turtle.ontimer(rocket_loop, DELAY['rocketship'])

    screen.update()

def game_over():
    """ends the game"""
    global running
    running=False 
    t = new_turtle(color=('red',), hide=True)
    t.write('Game over!',font=FONT)

def start_loops(time):
    '''run game loop time seconds'''
    turtle.ontimer(game_over, time *1000)
    cannonball_loop()
    rocket_loop()
###################
#
# Main
#
##################

#global vars
score = 0
shots = 0 
running = True # if runnings becomes false, the game is over
cannonBalls = []

# screen
screen = game_screen()
# write Score: 0
writer     = new_turtle(color=('magenta',), hide=True, pos=SCORE_POS)
writer.write('Score: ', move=True, font=FONT)
writer.write(0, font=FONT)

# create turtles
cannon     = new_turtle(angle=90, color=('red','yellow'))
deathstar  = new_turtle(shape=DSTAR,  pos=rand_pos())
rocket     = new_turtle(shape=ROCKET, pos=(-MAX_X, ALTITUDE))


# keyboard bindings
actions = {'Down': reload, 'Right': lambda: cannon.right(ANGLE), 'Left': lambda: cannon.left(ANGLE), 'space': shoot}
screen.listen()
turtle.tracer(0)

# register callbacks
for key in ['Down', 'Left', 'Right', 'space']:
    screen.onkeypress(actions[key], key)
    
# let game last TIME seconds
start_loops(time=TIME)

    
turtle.mainloop()
