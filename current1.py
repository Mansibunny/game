#game.py
#Mengyu Qi, Mansi Arora
#scavenger platform game that partially scrolls within certain range, keyboard input from user controls Player sprite
#objective is to complete all levels while collecting gems under time limit of light from torch without dying
#cannot fight enemies but can restore health by collecting medkits
#enemies include bats, skeletons, and icicles
#movement limited by masking of backgrounds
"""
TO DO:
-make it work
"""

from pygame import *
from math import *
from random import *
from datetime import datetime

screen=display.set_mode((1000,600))

#---PICTURES---

#--BACKG&MASKS--
shadow=image.load("black.png")
falling=image.load("falling.png")
fallPic=transform.smoothscale(falling,(1000,2484))
back = image.load("back/level2.jpg")
backPic=transform.smoothscale(back,(3000,600))
mask = image.load("mask/masklev2.png")
maskPic=transform.smoothscale(mask,(3000,600))
back2 = image.load("back/level3.jpg")
backPic2=transform.smoothscale(back2,(3000,600))
mask2 = image.load("mask/masklev3.png")
maskPic2=transform.smoothscale(mask2,(3000,600))
back3 = image.load("back/level4.jpg")
backPic3=transform.smoothscale(back3,(3000,600))
mask3 = image.load("mask/masklev4.png")
maskPic3=transform.smoothscale(mask3,(3000,600))
back4 = image.load("back/level5.jpg")
backPic4=transform.smoothscale(back4,(3000,600))
mask4 = image.load("mask/masklev5.png")
maskPic4=transform.scale(mask4,(3000,600))
back5 = image.load("back/level6.jpg")
backPic5=transform.smoothscale(back5,(3000,600))
mask5 = image.load("mask/masklev6.png")
maskPic5=transform.scale(mask5,(3000,600))
back6=image.load("back/level7.jpg")
backPic6=transform.smoothscale(back6,(3000,600))

GREEN=(0,255,0)
BLUE=(0,0,255)
#--OBJECTPICS--
medPic=transform.smoothscale(image.load("object/medkit.png"),(20,20))
gem1Pic=transform.smoothscale(image.load("object/gem1.png"),(50,30))
torchPic=transform.smoothscale(image.load("object/ticon.png"),(50,50))
iciclePic=transform.smoothscale(image.load("object/icicle.png"),(30,60))

#--GAME LOOP PICS--
endPic=transform.smoothscale(image.load("gameover.png"),(666,600))

#--------------
init()
text=font.SysFont("Courier",20)
title=font.SysFont("Times New Roman",100,True)
subtitle=font.SysFont("Times New Roman",50)
torchPos=[]
for i in range(10):
    torchPos.append((i*50,50)) #appends points to list


def makeMove(name,start,end,typ): 
    #returns list of pics in folder "name" and starting with name, of the range start-end, and type ".typ"
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.%s" % (name,name,i,typ)))
    return move
    
def getPixel(mask,x,y): #gets colour at point on mask
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height():
        return mask.get_at((int(x),int(y)))[:3] #returns RGB value of colour
    else:
        return (-1,-1,-1)
                
#--MOVING FUNCTIONS--
def moveUp(self,mask,vy):
    for i in range(vy):
        if getPixel(mask,self.rect[0]+15,self.rect[1]+2) != GREEN:
            self.rect[1] -= 1
        else:
            self.vy = 0

def moveDown(self,mask,vy):
    for i in range(vy):
        if getPixel(mask,self.rect[0]+15,self.rect[1]+45) != GREEN:
            self.rect[1] += 1
        else:
            self.vy = 0
            self.step = True
            
def moveRight(self,mask,vx):
    for i in range(vx):
        if getPixel(mask,self.rect[0]+28,self.rect[1]+15) != GREEN:
            self.rect[0] += 1
            self.rect[0]=min(self.rect[0],3000)

def moveLeft(self,mask,vx):
    for i in range(vx):
        if getPixel(mask,self.rect[0]+2,self.rect[1]+15) != GREEN:
            self.rect[0] -= 1

def moveClimb(self,mask,vy):
    for i in range(vy):
        if getPixel(mask,self.rect[0]+20,self.rect[1]+10)==BLUE:
            self.rect[1]-=1
    
def climb(self,mask,h):
    y = self.rect[1] + h
    while y > self.rect[1]+17 and getPixel(mask,self.rect[0],y) == GREEN:
        y-=1
    if y > self.rect[1]+17:
        self.rect[1] = y - h

#--ENEMY SPECIFIC MOVEMENT--
def moveDownSkel(self,mask,y):
    for i in range(y):
        if getPixel(mask,self.rect[0]+15,self.rect[1]+54) != GREEN:
            self.rect[1] += 1
            
#--LIST/INDICES OF FRAMES FOR SPRITES--
RIGHT=0 
LEFT=1
CLIMB=2
DEAD=3
mepics=[]
mepics.append(makeMove("hunts",10,18,"png"))      #pictures of Player sprite moving right
mepics.append(makeMove("hunts",142,150,"png"))    #pictures of Player sprite moving left
climbpics=makeMove("hunts",97,108,"png")
#empty pictures
del climbpics[5]
del climbpics[10]
#del climbpics[
mepics.append(climbpics)
mepics.append(makeMove("hunts",116,116,"png"))
meframe=0 #current frame within the move for Player
memove=0 #current move being performed for Player
skelpics=[]
skelpics.append(makeMove("skel",1,6,"png"))
skelpics.append(makeMove("skel",7,12,"png"))
for a in range(2):
    for b in range(6):
        skelpics[a][b]=transform.smoothscale(skelpics[a][b],(30,60)) #changes sixe of all skeleton pics
sframe=0 #current frame within the move for Skeleton
smove=0 #current move being performed for Skeleton
                
#--PLACEHOLDER VARIABLES--
MAPS=[0,1] #placeholder list
MAP=0 #no set map yet
t=0 #holds variable for Torch object
totgems=0 #total number of gems collected during game
                                
#--PLAYER--
class Player: #player object
    "tracks current position, velocity, gems, step, and health"
    def __init__(self,pics,scroll): #takes in picture, direction of scroll
        self.pics=pics
        self.vy=0
        self.step=True #standing on mask
        self.health=200 #PLayer health
        self.gems=0 #number of gems
        self.rect=Rect(0,300,40,50) #Rect area the pic occupies
        self.scroll=scroll #True if horizontal, False if vertical
        
    def move(self): #changes player position according to keyboard input
        global meframe, memove, RIGHT, LEFT, CLIMB, MAP
        keys=key.get_pressed()
        if self.scroll==False: #vertical scroll
            maxX=1000 #max x value is width of screen
        else:
            maxX=3000 #max x value is width of picture
        self.step=False #not stepping on mask
        newMove = -1
        self.vy+= 1 #add gravity to VY
        if self.vy < 0: #velocity going up
            if MAP!=0:
                moveUp(self,MAP.mask,-self.vy)
        elif self.vy > 0: #velocity going down
            if MAP!=0 and memove!=CLIMB:
                moveDown(self,MAP.mask,self.vy)            
        if keys[K_SPACE] and self.step: #jumps when SPACE pressed and stepping on mask
            self.vy = -14    
        elif keys[K_RIGHT] and self.rect[0] < maxX: #moves right when x not greater than max
            newMove = RIGHT
            if MAP!=0:
                moveRight(self,MAP.mask,10)
                climb(self,MAP.mask,27)                
        elif keys[K_LEFT] and self.rect[0] > 0: #moves left when x not less than 0
            newMove = LEFT
            if MAP!=0:
                moveLeft(self,MAP.mask,10)
                climb(self,MAP.mask,27)
        elif keys[K_UP] and self.scroll==False: #vertical scroll, can climb ladder
            newMove=CLIMB
            moveClimb(self,MAP.mask,10)
        else: #no keyboard input; player is standing still
            meframe = 0 #standing pose

        if memove == newMove: #still the same move as before     
            meframe+=0.4 #speeds up switching through frames
            if meframe >= len(self.pics[memove]): #frame is greater than number of pics in list
                meframe = 1 #goes back to first frame
        elif newMove != -1:     #a move was selected
            memove = newMove      #makes it current move
            meframe = 1 #0 is standing pose, so skips it when Player moves
    
    def hit(self): #decreases player health
        self.health-=5
        self.health=max(min(200,self.health),0)
        
    def reset(self): #resets positions and gems before new map
        global MAP
        self.rect[0]=0
        self.rect[1]=0
        self.gems=0
        if MAP.scroll==False: #last map
            self.scroll=False #vertical scroll
        
    def draw(self): #draws player on screen
        global meframe, memove, DEAD
        if self.health<=0: #no health left
                pic=self.pics[DEAD][0] #single frame for death
        else:
            pic = self.pics[memove][int(meframe)] #current pic depending on direction and frame count
            
        if self.scroll==True: #horizontal scroll            
            if 500<=self.rect[0]<=2500: #within scrolling range
                screen.blit(pic,(500,self.rect[1])) #blits at set position
            #out of scrolling range, sprite draws at different x values on screen
            elif self.rect[0]<500:
                screen.blit(pic,(self.rect[0],self.rect[1]))
            elif self.rect[0]>2500:
                screen.blit(pic,(self.rect[0]-2000,self.rect[1]))
        else: #vertical scroll
            if 300<=self.rect[1]<=1500:
                screen.blit(pic,(self.rect[0],300))
            elif self.rect[1]<300:
                screen.blit(pic,(self.rect[0],self.rect[1]))
            elif self.rect[1]>1500:
                screen.blit(pic,(self.rect[0],self.rect[1]-1200))
           

#--ENEMIES--
class Skeleton: #enemy object
    "tracks position, speed, target"
    #do sprite for walking???
    def __init__(self,pics,x,y,targ,scroll): #takes in picture and position
        self.rect=Rect(x,y,25,50) #rect position
        self.speed=-2
        self.pics=pics
        self.targ=targ
        self.scroll=scroll
        
    def move(self,targ): #takes in target and moves towards it if target inside certain range, else moves within automated range
        global sframe, smove, RIGHT, LEFT, MAP
        #constantly rotates through frames; no standing pose or input required
        newMove=-1
        if self.rect[0]<targ.rect[0]: #player is right of self
            if MAP!=0:
                moveRight(self,MAP.mask,1)
                climb(self,MAP.mask,50)
                newMove=RIGHT
                
        elif self.rect[0]>targ.rect[0]: #player is left of self
            if MAP!=0:
                moveLeft(self,MAP.mask,1)
                climb(self,MAP.mask,29)
                newMove=LEFT
  
        sframe=sframe+0.3 #switching through frames
        if sframe >= len(self.pics[smove]): #frame greater than number of pics
            sframe = 1 #goes back to first frame
        smove = newMove #makes newMove current move      
            
        if MAP!=0:
            moveDownSkel(self,MAP.mask,5) #different from Player moveDown; no vy and step variables
        
    def draw(self):
        pic = self.pics[smove][int(sframe)] #current pic depending on direction and frame count
        if 500<=self.targ.rect[0]<=2500:
            screen.blit(pic,(self.rect[0]-(self.targ.rect[0]-500),self.rect[1]))
        elif self.targ.rect[0]<500:
            screen.blit(pic,(self.rect[0],self.rect[1]))
        elif self.targ.rect[0]>2500:
            screen.blit(pic,(self.rect[0]-2000,self.rect[1]))

class Bat:
    "tracks area of attack, position, frame, target"
    def __init__(self,area,targ,scroll):
        self.area=area #area of attack, rect object       
        self.rect=Rect(area[0],0,30,20)
        self.speed=-1
        self.frame=0
        self.scroll=scroll
        self.targ=targ
        
    def move(self,targ):
        if targ.rect.colliderect(self.area): #target within attack area
            d=max(1,dist(self.rect[0],self.rect[1],targ.rect[0],targ.rect[1])) #distance between self and target
            moveX=(targ.rect[0]-self.rect[0])*self.speed/d       
            self.rect[0]=int(self.rect[0]-moveX) #moves towards target
            self.rect[1]+=2 #continuously moves down     
           
    def draw(self):
        pics=makeMove("batty",1,4,"png") #all frames of bat sprite
        self.frame+=0.2 #gradually adds to frame
        if 500<=self.targ.rect[0]<=2500: #within scrolling range
            screen.blit(pics[int(self.frame)%4],(self.rect[0]-(self.targ.rect[0]-500),self.rect[1])) #draws in relation to Player position
        #outside scrolling range, blits at own x value
        elif self.targ.rect[0]<500:
            screen.blit(pics[int(self.frame)%4],(self.rect[0],self.rect[1]))
        elif self.targ.rect[0]>2500:
            screen.blit(pics[int(self.frame)%4],(self.rect[0]-2000,self.rect[1]))

class Icicle:
    "tracks area of attack, position, target"
    def __init__(self,area,targ,scroll):
        self.area=area #area of attack, Rect object        
        self.rect=Rect(area[0],0,30,60)
        self.speed=-1
        self.scroll=scroll
        self.targ=targ
        self.hit=0
        self.count=0 #counter
        
    def move(self,targ):
        if targ.rect.colliderect(self.area): #target within attack area
            self.count+=1 #counter increases
        if self.count>=1: #Player has been in attack area before
            self.rect[1]+=4 #continuously blits down      
           
    def draw(self):
        if 500<=self.targ.rect[0]<=2500: #within scrolling range
            screen.blit(iciclePic,(self.rect[0]-(self.targ.rect[0]-500),self.rect[1])) #blits in relation to target
        #outside of scrolling range, blits at own x value
        elif self.targ.rect[0]<500:
            screen.blit(iciclePic,(self.rect[0],self.rect[1]))
        elif self.targ.rect[0]>2500:
                screen.blit(iciclePic,(self.rect[0]-2000,self.rect[1]))
            
#--OTHER FUNCTIONS--
def dist(x1,x2,y1,y2): #takes in two points, returns distance between them 
    return ((x1-x2)**2 + (y1-y2)**2)**0.5
     
#--OBJECTS--
class Torch: 
    "tracks time, makes torch effect, can reset start time"
    def __init__(self,pic):
        self.start=datetime.now()
        self.pic=pic
    def torchCount(self): #returns count of seconds passed since start
        now=datetime.now()
        return (now.hour*3600+now.minute*60+now.second-(self.start.hour*3600+self.start.minute*60+self.start.second))
   
    def torchLight(self,me): #takes pic with transparent circle, player and blits it so circle origin is at player centre
        if me.rect[0]<500:
            x=me.rect[0]
        elif 500<=me.rect[0]<=2500:
            x=500
        elif me.rect[0]>2500:
            x=me.rect[0]-2000
        x+=me.rect[2]//2
        y=me.rect[1]+me.rect[3]//2
        screen.blit(self.pic,(x-1500,y-1000))
        
    def reset(self):
        self.start=datetime.now()
        
class medKit:
    "tracks worth, position, collection status"
    def __init__(self,pic,x,y,scroll): #takes in pic, x pos, y pos, player
        self.worth=20
        self.rect=Rect(x,y-pic.get_height(),pic.get_width(),pic.get_height())
        self.got=False #False if not collected yet
        self.pic=pic
        self.scroll=scroll
   
    def gain(self,me):
        if self.got==False: #collides and not collected
            me.health+=self.worth
            me.health=min(200,me.health)
            self.got=True #True means has been collected

    def draw(self,me): 
        if self.got==False: #only draws if not collected
            if 500<=me.rect[0]<=2500:
                screen.blit(self.pic,(self.rect[0]-(me.rect[0]-500),self.rect[1]))
            elif me.rect[0]<500:
                screen.blit(self.pic,(self.rect[0],self.rect[1]))
            elif me.rect[0]>2500:
                screen.blit(self.pic,(self.rect[0]-2000,self.rect[1]))



class Gem:
    "tracks position, collection status"
    def __init__(self,pic,x,y,scroll): #takes in pic, coordinates, player, and if scrolling
        self.rect=Rect(x,y-pic.get_height(),pic.get_width(),pic.get_height())
        self.got=False #False if not collected yet
        self.pic=pic
        self.scroll=scroll
   
    def gain(self,me): #collected by player
        if self.got==False: #collides and not collected
            me.gems+=1
            self.got=True #True means has been collected
            
    def draw(self,me):
        if self.got==False: #only draws if not collected
            if 500<=me.rect[0]<=2500:
                screen.blit(self.pic,(self.rect[0]-(me.rect[0]-500),self.rect[1]))
            elif me.rect[0]<500:
                screen.blit(self.pic,(self.rect[0],self.rect[1]))
            elif me.rect[0]>2500:
                screen.blit(self.pic,(self.rect[0]-2000,self.rect[1]))


#--MAP--                
def changeMap(curMap,MAPS,me,t): #takes in map, list of maps, and player object
    #checks if player falls in gap in mask, and changes to next map
    if me.rect[1]>600: #player below mask level
        fallDown(me) #plays falling animation
        me.reset() #resets player position and gem count        
        if MAPS.index(curMap)!=len(MAPS)-1: #map is not final map
            t.reset()
            return MAPS[MAPS.index(curMap)+1] #returns next map            
    return curMap


def fallDown(me): #animation of falling down hole
    global totgems
    totgems+=me.gems
    falls=makeMove("hunts",34,44,"png")
    frame=0
    offset=0
    selfdown=0
    running=True
    while running:
        for evnt in event.get():
            if evnt.type==QUIT:
                running=False
        screen.blit(fallPic,(0,offset))
        screen.blit(falls[frame%9],(500,selfdown))
        screen.blit(shadow,(-975,selfdown-980))
        screen.blit(screen.copy(),(0,0))
        frame+=1
        offset-=50
        if offset<-1850:
            offset=-1850
            selfdown+=30
            if selfdown==600:
                running=False
        time.wait(100)
        display.flip()
            
"CONSTANTLY GENERATE ENEMIES???"
class Map: #takes in background pic, enemies, other objects, portal, and tracks state of all
    def __init__(self,back,mask,scroll,me,enemies,kits,gems):
        self.pic=back
        self.scroll=scroll
        self.offset=0
        self.me=me
        self.enemies=enemies
        self.kits=kits
        self.gems=gems
        self.mask=mask
        self.gemCount=len(gems)
    def backDraw(self): #draws itself back according to offset
        
        if self.scroll==True: #horizontal scroll
            if 500<=self.me.rect[0]<=2500: #scroll within this range
                self.offset=-1*(self.me.rect[0]-500) #offset
                if self.offset>0: #never blits right to black screen
                    self.offset=0
                if self.offset<-1*(self.pic.get_width()-screen.get_width()): #never blits left to black screen
                    self.offset=-1*(self.pic.get_width()-screen.get_width())
                screen.blit(self.pic,(self.offset,0))
            #stationary displays
            elif self.me.rect[0]<500: #not scroll while in this range
                screen.blit(self.pic,(0,0))
            elif self.me.rect[0]>2500: #not scroll while in this range
                screen.blit(self.pic,(-2000,0))
                
        else:
            if 300<=self.me.rect[1]<=1500: #CHANGEABLE ACCORDING TO PIC
                self.offset=-1*(self.me.rect[1]-300) #offset
                if self.offset>0: #never blits right to black screen
                    self.offset=0
                if self.offset<-1*(self.pic.get_height()-screen.get_height()): #never blits left to black screen
                    self.offset=-1*(self.pic.get_height()-screen.get_height())
                screen.blit(self.pic,(-1000,self.offset)) #CHANGEABLE ACCORDING TO PIC
            #stationary displays
            elif self.me.rect[1]<300: #not scroll while in this range
                screen.blit(self.pic,(-1000,-1200))
            elif self.me.rect[1]>1500: #not scroll while in this range
                screen.blit(self.pic,(-1000,0))
            
    def objectMove(self): #moves all objects of Map        
        #if the lists are not empty, moves objects
        if len(self.enemies)>0:
            for e in self.enemies:
                e.move(self.me) #enemies move depending on target position
        
    def objectCollide(self): #checks collisions between objects       
        #if lists not empty, checks collide between rects
        if len(self.kits)>0:
            for k in self.kits:
                if self.me.rect.colliderect(k.rect): #checks if rects collide
                    k.gain(self.me) #Player gains health
                    
        if len(self.gems)>0:
            for g in self.gems:
                if self.me.rect.colliderect(g.rect): #checks if rects collide
                    g.gain(self.me) #Player gains gem
                    
        if len(self.enemies)>0:
            for e in self.enemies:
                if self.me.rect.colliderect(e.rect): #checks if collide with enemy rect
                    self.me.hit() #decreases player health
                    
    def objectDraw(self):
        #if lists not empty, draws objects
        if len(self.enemies)>0:
            for e in self.enemies:
                e.draw()
        if len(self.kits)>0:
            for k in self.kits:
                k.draw(self.me)                        
        if len(self.gems)>0:
            for g in self.gems:
                g.draw(self.me)


#--ENDS GAME!--
def playEnd(me,torch): #ends game loop if no health, torch runs out, or completed last map
    if torch.torchCount()/10>=10: #torches ran out
        torchOut()
        screen.blit((title.render("GAME OVER",True,(255,0,0))),(170,100))
        screen.blit((text.render("[z] to play again                               [x] to go to menu",True,(255,0,0))),(100,500))
        display.flip()
        return True
        
    elif me.health<=0: #no health left in Player
        noHealth()
        screen.blit((title.render("GAME OVER",True,(255,0,0))),(170,100))
        screen.blit((text.render("[z] to play again                               [x] to go to menu",True,(255,0,0))),(100,500))
        display.flip()
        return True
    return False

def torchOut(): #torches ran out
    screen.fill((0,0,0))
    screen.blit(endPic,(167,0))
    screen.blit((subtitle.render("Your light has run out...",True,(255,0,0))),(190,300))
def noHealth(): #no health left in Player
    screen.fill((0,0,0))
    screen.blit(endPic,(167,0))
    screen.blit((subtitle.render("Your life has run out...",True,(255,0,0))),(200,300))

def endGame(gems): #final screen
    screen.fill((0,0,0))
    screen.blit((title.render("CONGRATULATIONS, YOU WIN!",True,(255,0,0))),(200,100))
    screen.blit((subtitle.render("YOU GOT:"+str(gems)+"/7",True,(255,0,0))),(270,350))
    display.flip()
    time.wait(3000)
    return "menu"
    
#--MENU--
def story(pics): #actual game loop
    global MAP, totgems
    me=Player(mepics,True) 
    #KEEP INFO IN SEPARATE TEXT FILES LATER-LESS CLUTTER
    enemy=[[Skeleton(skelpics,randint(400,1000),400,me,True),Bat(Rect(300,0,1000,600),me,True),Icicle(Rect(400,0,1000,600),me,True)],
           [Skeleton(skelpics,1000,500,me,True)],[Skeleton(skelpics,900,400,me,True)],[Skeleton(skelpics,500,500,me,True)],
           [Skeleton(skelpics,300,500,me,True)]]    
    kits=[[medKit(medPic,i,500,True) for i in range(400,601,100)],[medKit(medPic,600,400,True)],[medKit(medPic,700,400,True)],
          [medKit(medPic,700,400,True)],[medKit(medPic,1000,400,True)]] #all medkits
    gems=[[Gem(gem1Pic,900,500,True),Gem(gem1Pic,1200,500,True),Gem(gem1Pic,2000,500,True)],
          [Gem(gem1Pic,800,500,True),Gem(gem1Pic,1500,200,True),Gem(gem1Pic,2200,500,True)],
          [Gem(gem1Pic,600,300,True),Gem(gem1Pic,1800,300,True),Gem(gem1Pic,2000,300,True)],
          [Gem(gem1Pic,200,400,True),Gem(gem1Pic,2500,100,True),Gem(gem1Pic,1700,200,True)],
          [Gem(gem1Pic,1200,200,True),Gem(gem1Pic,1900,400,True),Gem(gem1Pic,1900,400,True)]] #all gems
    MAPS=[Map(backPic,maskPic,True,me,enemy[0],kits[0],gems[0]),Map(backPic2,maskPic2,True,me,enemy[1],kits[1],gems[1]),
          Map(backPic3,maskPic3,True,me,enemy[2],kits[2],gems[2]),Map(backPic4,maskPic4,True,me,enemy[3],kits[3],gems[3]),
          Map(backPic5,maskPic5,True,me,enemy[4],kits[4],gems[4])] #list of all maps
    MAP=MAPS[0] #starts with first map
    t=Torch(shadow) #Torch
    hbar=(560,50,me.health,20) #healthbar
    backh=hbar #full healthbar outline
    myClock=time.Clock()
    oTime=datetime.now()
    running=True    
    while running:
        for e in event.get():
            if e.type==QUIT:
                running=False
                
        if key.get_pressed()[27]: running=False
        nTime=datetime.now() #new time
        
        #---MAP CHANGE--
        MAP=changeMap(MAP,MAPS,me,t)
        if MAPS.index(MAP)==len(MAPS)-1:
            if me.rect[1]==1800: #final map done
                endgame(totgems)
            
        
        #---MOVES OBJECTS, CHECKS COLLIDE---
        me.move()
        MAP.objectMove()
        if (nTime.hour*3600+nTime.minute*60+nTime.second-(oTime.hour*3600+oTime.minute*60+oTime.second))==1: #full second interval passed
            MAP.objectCollide() #checks collide between objects (enemy will not drain health as fast)
            oTime=nTime #new time becomes old time

        #-----------------------------------
            
        hbar=(760,50,me.health,20) #draws amount of health Player has left                
        
        #---DRAWS ON SCREEN---
        MAP.backDraw()
        me.draw()
        MAP.objectDraw()
        t.torchLight(me)
        
        for i in range(10-t.torchCount()//10): #number of torches left out of ten
            screen.blit(torchPic,torchPos[i]) 
            
        draw.rect(screen,(255,255,255),backh,6)
        draw.rect(screen,(255,0,0),hbar)
        screen.blit((text.render(str(10-t.torchCount()%10),True,(255,255,255))),(940,80)) #displays count down in seconds to when a torch is used up
        screen.blit((text.render("GEMS: "+str(me.gems)+"/"+str(MAP.gemCount),True,(255,255,255))),(850,100)) #displays number of gems collected
        display.flip()
        
        #---------------------
        
        #---CHECKS FOR ENDING GAME---
        if playEnd(me,t)==True:
            running2 = True
            while running2: #MORE OPTIONS LOOP
                for evnt in event.get():          
                    if evnt.type == QUIT:
                        running2= False
                if key.get_pressed()[27]: quit()
                keys=key.get_pressed()
                if keys[K_z]: #play again
                    return "story" #resets game loop
                if keys[K_x]: #go to menu
                    return "menu"

        #---------------------
        myClock.tick(60)
        
    return "menu"    
    
def instructions(): #instructions page
    running = True
    inst = image.load("instructions.jpg").convert()
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"
        
def credit(): #credit page
    running = True
    cred = image.load("credits.jpg").convert()
    cred = transform.smoothscale(cred, screen.get_size())
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"
       

def menu(): #main menu, holds and leads to screens
    global text
    running = True
    myClock = time.Clock()
    menuimg = image.load("menucave.jpg").convert()
    menuimg= transform.smoothscale(menuimg, screen.get_size())
    buttons = [Rect(200,y*60+200,150,40) for y in range(3)]
    vals = ["story","instructions","credits"]
    nlabel1=text.render("Start", 1, (0, 0, 0,))
    nlabel2=text.render("Instructions", 1, (0, 0, 0,))
    nlabel3=text.render("Credits", 1, (0, 0, 0,))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(menuimg,(0,0))
        for r,v in zip(buttons,vals):
            draw.rect(screen,(222,55,55),r)
            if r.collidepoint(mpos):
                draw.rect(screen,(0,255,0),r,2)
                if mb[0]==1:
                    return v
            else:
                draw.rect(screen,(255,255,0),r,2)
        screen.blit(nlabel1,(250,210))
        screen.blit(nlabel2,(205,270))
        screen.blit(nlabel3,(235,330))
                
        display.flip()

#--PAGE LOOP--
running = True
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "story":
        time.wait(50)
        page = story(mepics)
    if page == "instructions":
        page = instructions()        
    if page == "credits":
        page = credit()    
    
quit()
