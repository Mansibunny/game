"""
sprite3.py
~~~~~~~~~~
This example demonstrates simple sprite animation without using any "fancy" techniques.

"""
from pygame import *
from random import randint
size = width, height = 800, 500
screen = display.set_mode(size)
init()
backPic = image.load("back.JPG")

def moveDude(dude):
    ''' moveMario controls the location of Mario as well as adjusts the move and frame
        variables to ensure the right picture is drawn.
    '''
    global move, frame
    keys = key.get_pressed()
    

    newMove = -1        
    if keys[K_RIGHT] and dude[X] < 3600:
        newMove = RIGHT
        dude[X] += 5
        if dude[SCREENX] <450:
            dude[SCREENX] += 5
        
    elif keys[K_LEFT] and dude[X] > 450:
        newMove = LEFT
        dude[X] -= 5
        if dude[SCREENX] <450:
            dude[SCREENX] += 5
    elif keys[K_SPACE] and dude[ONGROUND]:
        dude[VY] = -8
        dude[ONGROUND]=False
    else:
        frame = 0

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.1 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1
        
    dude[Y]+=dude[VY]     # add current speed to Y
    if dude[Y] >= 450:
        dude[Y] = 450
        dude[VY] = 0
        dude[ONGROUND]=True
    dude[VY]+=.2     # add current speed to Y
    
        
def checkCollide(dude,plats):
    global rec
    rec = Rect(dude[X],dude[Y],20,31)
    for p in plats:
        if rec.colliderect(p):
            if dude[VY]>0 and rec.move(0,-dude[VY]).colliderect(p)==False:
                dude[ONGROUND]=True
                dude[VY] = 0
                dude[Y] = p.y - 32
                
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
    offset= dude[SCREENX] - dude[X] 
    screen.blit(backPic,(offset,0))
    for pl in plats:
        p = pl.move(offset,0)        
        draw.rect(screen,(111,111,111),p)
    pic = pics[move][int(frame)]
    screen.blit(pic,(dude[SCREENX]-10,dude[Y]-15))

    display.flip()


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
dude=[250,450,0,True,250]

running = True
myClock = time.Clock()

plats = []
for i in range(20):
    plats.append(Rect(randint(100,2000),randint(250,480),60,10))
    
while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
        
    moveDude(dude)
    checkCollide(dude,plats)
    drawScene(screen, dude)
    myClock.tick(50)
    
quit()
