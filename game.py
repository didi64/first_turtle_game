import turtle
import random
import math

# constants
BG_PIC  = 'space.gif'
ROCKET = 'rocketship.gif'
DSTAR  = 'deathstar.gif'
WIDTH  = 1000
HEIGHT = 500
FONT = ('Arial', 14, 'bold')
SCORE_POS = (100,160)
ANGLE = 4
SHOTS_TIL_JAM = 5
CANNONBALL_SIZE = (0.2,0.2)
CANNONBALL_SPEED = 20 
BULLETRANGE = 200
SHIPSPEED = 5
ALTITUDE = 80
MAX_X = 120
DELAY = {'rocketship': 20,  'cannonballs': 20} #milliseconds
SCORE = {'rocketship': 1, 'deathstar':10}

#global vars
score = 0
shots = 0 
running = True #if runnings becomes false, the game is over
# screen
screen = turtle.Screen()
screen.title('Fun with Turtle')
screen.setup(width = WIDTH, height = HEIGHT)
screen.bgpic(BG_PIC)
screen.addshape(ROCKET)
screen.addshape(DSTAR)

# get new turtles
def new_turtle(size=(1,1), shape='classic', alpha=0, color=('black','black'), speed=0, pendown=False, pos=(0,0), hide=False):
    t=turtle.Turtle(shape)
    t.turtlesize(*size)
    t.speed(speed)
    t.color(*color)
    t.left(alpha)
   
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
    t=ct.clone()
    t.turtlesize(*CANNONBALL_SIZE)
    t.shape('circle')
    cts.append(t)

def unjam():
    global shots
    shots=0

def write_score():
    wt.undo()
    wt.write(score,font=FONT)

def is_close(x,y, err=10):
    return abs(x-y) < err

def out_of_square(x,y, width=BULLETRANGE):
    return max(abs(x),abs(y)) > width/2

def move_cannonballs():
    """update screen"""
    global score
    for t in cts:
        t.forward(CANNONBALL_SPEED)
        if  is_close(t.pos(),rt.pos()): # rocketship hit
            score+= SCORE['rocketship']
            rt.goto(-MAX_X,ALTITUDE)
        if  is_close(t.pos(), dt.pos()):
            score+= SCORE['deathstar']
            dt.goto(rand_pos())
        if  out_of_square(*t.pos()):
            cts.remove(t)
            del t
   
    write_score()
    if  running:
        turtle.ontimer(move_cannonballs,DELAY['cannonballs'])
   
def move_rocket():
    """move rocketship"""
    rt.forward(SHIPSPEED)
    if  rt.xcor() > MAX_X:
        rt.goto(-MAX_X, ALTITUDE)
    if  running:
        turtle.ontimer(move_rocket,DELAY['rocketship'])

def game_over():
    """ends the game"""
    global running
    running=False
    ct.write('Game over!',font=FONT)

# cannon turtle, deathstar turtle, rocketship turtle, writer turtle
ct = new_turtle(alpha=90, color=('red','yellow'))
dt = new_turtle(shape=DSTAR, pos=rand_pos())
rt = new_turtle(shape=ROCKET, pos=(-MAX_X, ALTITUDE))
wt = new_turtle(color=('magenta',), hide=True, pos=SCORE_POS)

wt.write('Score:',font=FONT)
wt.forward(60)
wt.write(0, font=FONT)

# list of cannonballturtles
cts=[]
running = True
# keyboard bindings
actions = {'Down': unjam, 'Right': lambda: ct.right(ANGLE), 'Left': lambda: ct.left(ANGLE), 'space': shoot}
screen.listen()
for key in ['Down', 'Left', 'Right', 'space']:
    screen.onkeypress(actions[key], key)
    

move_cannonballs()
move_rocket()

turtle.ontimer(game_over,10000)
turtle.mainloop()
