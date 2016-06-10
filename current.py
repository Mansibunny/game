#backup.py

"""
TO DO:

background and map changes, environment when player moves to certain areas
transition!
less awkwardness in enemy movements
automatic enemy movement and tracking...
"""

from pygame import *
from math import *
from random import *
from datetime import datetime

screen=display.set_mode((1200,600))

#---PICTURES---
pic=transform.smoothscale(image.load("bricks.jpg"),(1200,600))
pic2=transform.smoothscale(image.load("back2.jpg"),(1200,600))
sprites=[transform.smoothscale(image.load("me.png"),(40,40)),transform.smoothscale(image.load("me2.png"),(40,40))]
enePic=transform.smoothscale(image.load("enemy.png"),(60,60))
medPic=transform.smoothscale(image.load("object/medkit.png"),(20,20))
gem1Pic=transform.smoothscale(image.load("object/gem1.png"),(30,30))
torchPic=transform.smoothscale(image.load("object/torch.png"),(20,60))

#--------------
    
init()
text=font.SysFont("Courier",20)
torchRects=[]
for i in range(10):
    torchRects.append((i*30,50))

#--SPRITES!--#

#--PLAYER--
class Player: #player object
    "tracks current position, velocity, platform, and health"
    def __init__(char,pic): #takes in picture
        char.pic=pic
        char.vy=0
        char.step=True
        char.health=200
        char.gems=0
        char.rect=Rect(0,500-char.pic.get_height(),pic.get_width(),pic.get_height())
        char.state=["RIGHT","WALK"]
        
    def move(char): #changes player position according to keyboard input        
        keys=key.get_pressed()

        if keys[K_RIGHT]:
            char.rect[0]+=2
            char.rect[0]=min(char.rect[0],screen.get_width())
            char.state[0]="RIGHT"
            print("r")
        if keys[K_LEFT]:
            char.rect[0]-=2
            char.rect[0]=max(0,char.rect[0])
            char.state[0]="LEFT"
            print("l")
        if keys[K_UP] and char.step==True:
            char.vy=-15
            char.step=False
            print("jump")
            
        if char.step==False:
            char.state[1]="JUMP"
        char.rect[1]+=char.vy
        if char.rect[1]>500-char.rect[3]: 
            char.rect[1]=500-char.rect[3]
            char.step=True #on ground
            char.state[1]="WALK"
        char.vy+=1

    def hit(char): #decreases player health
        char.health-=5
        char.health=min(100,char.health)
            
    def draw(char): #draws player on screen
        screen.blit(char.pic,(char.rect[0],char.rect[1]))
       

#--ENEMY--
class Enemy: #enemy object
    "tracks start pos, current pos, speed"
    
    def __init__(self,pic,x,platY,scroll): #takes in picture and position
        self.startX=x
        self.startY=platY-pic.get_height()
        self.rect=Rect(self.startX,self.startY,pic.get_width(),pic.get_height()) #rect position
        self.speed=-2
        self.pic=pic
        self.state=["LEFT","WALK"]
        self.scroll=scroll
        #self.range=100
    def move(self,targ): #takes in target and moves towards it
        if self.scroll==True:
            self.start=self.startX-targ.rect[0]
        else:
            self.start=self.startX
        #cannot move outside range of 100 left and right
        #automated movement->smoother, even as side scrolls
        if targ.rect[0]<self.start-100 or targ.rect[0]>self.start+100: #target not within moving range
            #automated movement within range
            if self.rect[0]<self.start-100: 
                self.speed*=-1
                self.state[0]="RIGHT"
            if self.rect[0]>self.start+100:
                self.speed*=-1
                self.state[0]="LEFT"
            self.rect[0]=int(self.rect[0]+self.speed)
        if self.start-100<=targ.rect[0]<=self.start+100: #target within moving range
            d=max(1,dist(self.rect[0],self.rect[1],targ.rect[0],targ.rect[1])) #distance between self and target
            moveX=(targ.rect[0]-self.rect[0])*self.speed/d #       
            self.rect[0]=int(self.rect[0]-moveX)

    def reset(self): #resets position to starting points
        self.rect[0]=self.startX
        
    def draw(self):
        screen.blit(self.pic,(self.rect[0],self.rect[1]))
        
#--FUNCTIONS!--
def dist(x1,x2,y1,y2): 
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def checkPic(obj1,pic1,obj2,pic2): #takes in two objects and their pictures; checks if positions are further than pic widths
    space=pic2.get_width()//2+pic1.get_width()//2
    if dist(obj1.x,obj2.x,obj1.y,obj2.y)<=space:
        return True
    return False

       
#--OBJECTS!--    
class Torch:
    "tracks time since start, makes torchlight effect"
    def __init__(self):
        self.start=datetime.now()

    def torchCount(self): #returns count of  second intervals passed since start
        now=datetime.now()
        return (now.hour*3600+now.minute*60+now.second-(self.start.hour*3600+self.start.minute*60+self.start.second))
        #return floor(num)
   
    def torch(self,pic,x,y): #takes pic with transparent circle, position and blits it so circle origin is at position
        #HAVE SEPARATE BACKGROUND FUNCTION MAN, NEED TO MAKE MAPS!!!
        if x<0:
            x=0
        if x>pic.get_width():
            x=pic.get_width()
        dark=Surface((pic.get_width(),pic.get_height()))
        #world=Surface((pic.get_width()*2,pic.get_height()))
        dark.set_alpha(100)
        dark.fill((0,0,0))
        draw.circle(dark,(111,111,111),(int(x),int(y)),60)
        draw.circle(dark,(200,200,200),(int(x),int(y)),45)
        #for i in range(2):
            #world.blit(pic,(pic.get_width()*i,0))
        #screen.blit(world,(-2*int(x),0))
        screen.blit(dark,(0,0))
        #replace with photoshop and transparent circle pic

class medKit:
    def __init__(self,pic,x,platY,char,scroll): #takes in pic, x pos, y pos, player
        self.worth=20
        self.startX=x
        self.rect=Rect(x,platY-pic.get_height(),pic.get_width(),pic.get_height())
        self.got=False #False if not collected yet
        self.pic=pic
        self.scroll=scroll
        
    def move(self,char): #moves posirion across screen if it is scrolling
        if self.scroll==True:
            self.rect[0]=self.startX-char.rect[0]
        
    def gain(self,char):
        if self.got==False: #collides and not collected
            char.health+=self.worth
            char.health=min(200,char.health)
            self.got=True #True means has been collected
            
    def draw(self): 
        #self.newx=self.x-char.rect[0]
        if self.got==False: #only draws if not collected
            screen.blit(self.pic,(self.rect[0],self.rect[1]))

class Gem:
    def __init__(self,pic,x,platY,char,scroll): #takes in pic, coordinates, player, and if scrolling
        self.startX=x
        self.rect=Rect(x,platY-pic.get_height(),pic.get_width(),pic.get_height())
        self.got=False #False if not collected yet
        self.pic=pic
        self.scroll=scroll
        
    def move(self,char): #changes position if scrolling
        if self.scroll==True:
            self.rect[0]=self.startX-char.rect[0]
        
    def gain(self,char): #collected by player
        if self.got==False: #collides and not collected
            char.gems+=1
            self.got=True #True means has been collected
            
    def draw(self):
        if self.got==False: #only draws if not collected
            screen.blit(self.pic,(self.rect[0],self.rect[1]))

#--MAP--

def checkMap(curMap,MAPS,me): #which portal and map place to go to (change structure later)
    bar=key.get_pressed()    
    for p in curMap.ports:
        if me.rect.colliderect(p) and bar[K_SPACE]:
            return (MAPS.index(curMap)+1)%2
    return MAPS.index(curMap)


class Map:
    def __init__(self,pic,scroll,me,enemies,kits,gems,ports):
        self.pic=pic
        self.scroll=scroll
        self.x=0
        self.me=me
        self.enemies=enemies
        self.kits=kits
        self.gems=gems
        self.ports=ports
        
    def backDraw(self):
        screen=display.set_mode((self.pic.get_width(),self.pic.get_height()))
        if self.scroll==True:            
            self.x=-2*self.me.rect[0]
            if self.x<0:
                self.x=0
            if self.x>self.pic.get_width():
                self.x=self.pic.get_width()
            screen.blit(self.pic,(self.x,0))
        else:
            screen.blit(self.pic,(0,0))
            
    def objectMove(self):
        
        self.me.move()
        
        if len(self.enemies)>0:
            for e in self.enemies:
                e.move(self.me)
                    
        if len(self.kits)>0:
            for k in self.kits:
                #if self.scroll==True:
                k.move(self.me)
                    
        if len(self.gems)>0:
            for g in self.gems:
                #if self.scroll==True:
                g.move(self.me) #moves kits on screen and in rects

    def objectDraw(self):
        self.me.draw()
        if len(self.enemies)>0:
            for e in self.enemies:
                e.draw()
        if len(self.kits)>0:
            for k in self.kits:
                k.draw()
                    
        if len(self.gems)>0:
            for g in self.gems:
                 g.draw()
                 
    def objectCollide(self):
        keys=key.get_pressed()
        
        if len(self.kits)>0:
            for k in self.kits:
                if self.me.rect.colliderect(k.rect): #checks if rects collide
                    k.gain(self.me)
                    
        if len(self.gems)>0:
            for g in self.gems:
                if self.me.rect.colliderect(g.rect): #checks if rects collide
                    g.gain(self.me)
                    
        if len(self.enemies)>0:
            for e in self.enemies:
                if self.me.rect.colliderect(e.rect): #checks if collide with enemy rect
                    self.me.hit() #decreases player health





#--ENDS GAME!--
def gameEnd(me,torch):
    if me.health==0 or torch.torchCount()/10>10: 
        return True
    return False
   
#--MENU!--

def story(me):
    me=Player(me)
    dude=[[Enemy(enePic,randint(400,1000),500,True)],[Enemy(enePic,1000,500,False)]]
    t=Torch()
    kits=[[medKit(medPic,i,500,me,True) for i in range(400,601,100)],[medKit(medPic,600,500,me,False)]] #all medkits
    gems=[[Gem(gem1Pic,900,500,me,True)],[Gem(gem1Pic,800,500,me,False)]] #all gems
    ports=[[Rect(0,460,40,40)],[Rect(560,460,40,40)]]
    back1=Surface((pic.get_width(),pic.get_height()))
    back2=Surface((pic.get_width(),pic.get_height()))
    for i in range(2):
        back1.blit(pic,(i*pic.get_width(),0))
    back2.blit(pic2,(0,0))
    MAPS=[Map(back1,True,me,dude[0],kits[0],gems[0],ports[0]),Map(back2,False,me,dude[1],kits[1],gems[1],ports[1])]
    mapNUM=0
    MAP=MAPS[mapNUM]
    hbar=(560,50,me.health,20)
    backh=hbar #full healthbar outline
    myClock=time.Clock()
    running=True    
    while running:
        for evnt in event.get():
            if evnt.type==QUIT:
                running=False
                
        if key.get_pressed()[27]: running=False
        
        #---MAP CHANGE--
        if checkMap(MAP,MAPS,me)!=MAPS.index(MAP):
            MAP=MAPS[checkMap(MAP,MAPS,me)]
        screen=display.set_mode((MAP.pic.get_width(),MAP.pic.get_height()))
        
        #---MOVES OBJECTS, CHECKS COLLIDE---
        MAP.objectMove()
        MAP.objectCollide()

        #-----------------------------------
            
        hbar=(560,50,me.health,20)                
        
        #---DRAWS ON SCREEN---
        MAP.backDraw()
        MAP.objectDraw()
        t.torch(pic,me.rect[0]+me.rect[2]//2,me.rect[1]+me.rect[3]//2)
        
        for i in range(10-t.torchCount()//10):
            screen.blit(torchPic,torchRects[i])
            
        draw.rect(screen,(255,255,255),backh,4)
        draw.rect(screen,(255,0,0),hbar)
        screen.blit((text.render(str(10-t.torchCount()%10),True,(255,255,255))),(740,80)) #displays count down in seconds to when a torch is used up
        screen.blit((text.render(str(me.gems)+"/10",True,(255,255,255))),(735,100)) #displays number of gems collected
        display.flip()
        
        #---------------------
        
        #---CHECKS FOR ENDING GAME---
        if gameEnd(me,t)==True:
            screen.fill((0,0,0))
            screen.blit((text.render("GAME OVER",True,(255,255,255))),(360,280))
            display.flip()
            time.wait(1000)
            quit()
        #---------------------
        myClock.tick(30)
        
    return "menu"    
    
def instructions():
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
        
def credit():
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

def mfSelect(): #player can select gender for sprite after start on menu, before actual game loop
    global text
    running=True
    buttons=[Rect(screen.get_width()//5*i,200,120,50) for i in range(1,4,2)]
    labels=["FEMALE","MALE"]

    while running:
        for e in event.get():
            if e.type==QUIT:
                return "menu"
        screen.fill((0,0,0))
        pos=mouse.get_pos()
        mb=mouse.get_pressed()
        for b,l in zip(buttons,labels):
            draw.rect(screen,(255,255,255),b,2)
            if b.collidepoint(pos):
                draw.rect(screen,(255,0,0),b,2)
                if mb[0]==1:
                    return labels.index(l)
        screen.blit(text.render(labels[0],True,(255,255,255)),(buttons[0][0],buttons[0][1]))
        screen.blit(text.render(labels[1],True,(255,255,255)),(buttons[1][0],buttons[1][1]))
        display.flip()

#--PAGE LOOP!--
running = True
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "story":
        time.wait(500)
        me=sprites[mfSelect()]
        page = story(me)
    if page == "instructions":
        page = instructions()        
    if page == "credits":
        page = credit()    
    
quit()
