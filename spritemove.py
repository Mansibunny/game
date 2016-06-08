"""
sprite3.py
~~~~~~~~~~
This example demonstrates simple sprite animation without using any "fancy" techniques.

"""
from pygame import *
from math import *
from random import randint
size = width, height = 800, 500
screen = display.set_mode(size)
init()
backPic = image.load("back.jpg")
maskPic = image.load("mask.png")
GREEN = (0,255,0)

def moveDude(dude):
    ''' moveMario controls the location of Mario as well as adjusts the move and frame
        variables to ensure the right picture is drawn.
    '''
    global move, frame
    keys = key.get_pressed()
    dude[ONGROUND]=False
    newMove = -1
    dude[VY] += 1         # add gravity to VY
    if dude[VY] < 0:
        moveUp(dude,-dude[VY])
    elif dude[VY] > 0:
        moveDown(dude,dude[VY])
        
    if keys[K_RIGHT] and dude[X] < 3400:
        newMove = RIGHT
        moveRight(dude,10)
        climb(dude)
        
    elif keys[K_LEFT] and dude[X] > 250:
        newMove = LEFT
        moveLeft(dude,10)
        climb(dude)
    elif keys[K_SPACE] and dude[ONGROUND]:
        dude[VY] = -14

    else:
        frame = 0

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame +0.1 # adding 0.2 allows us to speed up the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1
    
        

def makeMove(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))
    return move


def drawScene(screen,dude):
    offset= 250 - dude[X] 
    screen.blit(backPic,(offset,0))
    pic = pics[move][int(frame)]
    screen.blit(pic,(250,dude[Y]))

    display.flip()

    
def getPixel(mask,x,y):
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height():
        return mask.get_at((int(x),int(y)))[:3]
    else:
        return (-1,-1,-1)

def moveUp(dude,vy):
    for i in range(vy):
        if getPixel(maskPic,dude[X]+15,dude[Y]+2) != GREEN:
            dude[Y] -= 1
        else:
            dude[VY] = 0

def moveDown(dude,vy):
    
    for i in range(vy):
        #print("FALLING",getPixel(backPic,guy[X]+15,guy[Y]+28))
        if getPixel(maskPic,dude[X]+15,dude[Y]+45) != GREEN:
            dude[Y] += 1
        else:
            dude[VY] = 0
            dude[ONGROUND] = True
            
def moveRight(dude,vx):
    for i in range(vx):
        if getPixel(maskPic,dude[X]+28,dude[Y]+15) != GREEN:
            dude[X] += 0.8

def moveLeft(dude,vx):
    for i in range(vx):
        if getPixel(maskPic,dude[X]+2,dude[Y]+15) != GREEN:
            dude[X] -= 0.8
def climb(dude):
    y = dude[Y] + 27
    while y > dude[Y]+17 and getPixel(maskPic,dude[X],y) == GREEN:
        y-=1
    if y > dude[Y]+17:
        dude[Y] = y - 27

RIGHT = 0 # These are just the indices of the moves
LEFT = 1

 
pics = []
pics.append(makeMove("hunts",10,18))      # RIGHT
pics.append(makeMove("hunts",142,150))    # LEFT

frame=0     # current frame within the move
move=0      # current move being performed

X=0
Y=1
VY=2
ONGROUND=3
SCREENX = 4
dude=[250,50,0,True,250]

running = True
myClock = time.Clock()

    
while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
        
    moveDude(dude)
    drawScene(screen, dude)
    myClock.tick(55)
    
quit()
