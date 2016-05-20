#startSeq.py

"""
TO DO:

background and map changes, environment when player moves to certain areas
transition!
less awkwardness in enemy movements
better positioning and blitting of images (collide and health loss)
menu and stuff
"""

from pygame import *
from math import *
from random import *
from datetime import datetime

screen=display.set_mode((800,600))
pic=transform.smoothscale(image.load("backg1.png").convert(),(800,600))
pic2=transform.smoothscale(image.load("background.jpg").convert(),(800,600))
sprites=[transform.smoothscale(image.load("me.jpg").convert(),(40,40)),transform.smoothscale(image.load("me2.png").convert(),(40,40))]
enePic=transform.smoothscale(image.load("enemy.jpg").convert(),(60,60))
medPic=transform.smoothscale(image.load("medkit.png").convert(),(20,20))
char=[0,400,-8,True]
init()
text=font.SysFont("Courier",20)

#--PLAYER--
class Player:
    "tracks current position, velocity, platform, and health"
    def __init__(char,pic):
        char.x=0
        char.y=500
        char.vy=0
        char.step=True
        char.health=100
        char.pic=pic
    def move(char): 
        
        keys=key.get_pressed()

        if keys[K_RIGHT]:
            char.x+=2
            
        if keys[K_LEFT]:
            char.x-=2
            
        if keys[K_SPACE] and char.step==True:
            char.vy=-15
            char.step=False
            
        char.y+=char.vy
        if char.y>500:
            char.y=500
            char.step=True
        char.vy+=0.5
      
    def hit(char):
        char.health-=1
        char.health=min(100,char.health)
            
    def draw(char):
        #draw.circle(screen,(0,0,255),(int(char.x),int(char.y)),10)
        screen.blit(char.pic,(char.x-char.pic.get_width()//2,char.y-char.pic.get_height()//2))
#--ENEMY--
class Enemy:
    "tracks start pos, current pos, speed"
    
    def __init__(self,pic,x,y):
        self.startX=x
        self.startY=y
        self.x=x
        self.y=y
        self.speed=8
        self.pic=pic
    def move(self,targ):
        d=max(1,dist(self.x, self.y, targ.x, targ.y))
        moveX=(targ.x-self.x)*self.speed/d
        moveY=(targ.y-self.y)*self.speed/d
        self.x+=moveX
        #cannot move outside range of 100 left and right
        if self.x<self.startX-100: 
            self.x=self.startX-100
        if self.x>self.startX+100:
            self.x=self.startX+100
        self.y+=moveY
        
    def reset(self):
        self.x,self.y=self.startX, self.startY
        
    def draw(self):
        #draw.circle(screen,(255,0,0),(int(self.x),int(self.y)),10)
        screen.blit(self.pic,(self.x-self.pic.get_width()//2,self.y-self.pic.get_height()//2))
        
#--FUNCTION--
def dist(x1,x2,y1,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def checkPic(obj1,pic1,obj2,pic2):
    space=pic2.get_width()//2+pic1.get_width()//2
    if dist(obj1.x,obj2.x,obj1.y,obj2.y)<=space:
        return True
    return False
def check(obj1,obj2,space):
    if dist(obj1.x,obj2.x,obj1.y,obj2.y)<=space:
        return True
    return False
#--MAP--
       
#--OBJECTS--    
class Torch:
    "tracks time since start, makes torchlight effect"
    def __init__(self):
        self.start=datetime.now()
   
    def torchTime(self,start):
        now=datetime.now()
        if now.hour*3600+now.minute*60+now.second-60>=start.hour*3600+start.minute*60+start.second:
            return True
        return False
    
    def torchCount(self):
        now=datetime.now()
        self.num=60-(now.hour*3600+now.minute*60+now.second-(self.start.hour*3600+self.start.minute*60+self.start.second))
        return self.num
   
    def torch(self,pic,x,y): #takes pic, position and makes transparent black screen with size
                        #of pic and white circle at position        
        if x<0:
            x=0
        if x>pic.get_width():
            x=pic.get_width()
        dark=Surface((pic.get_width(),pic.get_height()))
        world=Surface((pic.get_width()*2,pic.get_height()))
        dark.set_alpha(100)
        dark.fill((0,0,0))
        draw.circle(dark,(111,111,111),(int(x),int(y)),60)
        draw.circle(dark,(200,200,200),(int(x),int(y)),45)
        for i in range(2):
            world.blit(pic,(pic.get_width()*i,0))
        screen.blit(world,(-1*int(x),0))
        screen.blit(dark,(0,0))
        #replace with photoshop and transparent circle pic

class medKit:
    def __init__(self,pic,x,y):
        #self.worth=0
        self.worth=20
        self.x=x
        self.y=y
        self.got=False #False if not collected yet
        self.pic=pic
        
    def gain(self,char):
        if checkPic(self,self.pic,char,char.pic)==True and self.got==False: #collides and not collected
            char.health+=self.worth
            char.health=min(100,char.health)
            self.got=True #True means has been collected
            
    def draw(self):
        if self.got==False: #only draws if not collected
            screen.blit(self.pic,(self.x-self.pic.get_width()//2,self.y-self.pic.get_height()//2))

#--ENDS GAME--
def gameEnd(me):
    if me.health==0: #also count down torches later
        return True
    return False
   
#--MENU--
"""
class Branch:
    def __init__(self):
        self.dude=Enemy(enePic,randint(100,700),500)
"""
def story(me):
    me=Player(me)
    dude=Enemy(enePic,randint(100,700),500)
    t=Torch()
    kit=[[medKit(medPic,i,500)] for i in range(400,601,100)]
    hbar=(50,50,200,20)
    myClock=time.Clock()
    running=True    
    while running:
        for e in event.get():
            if e.type==QUIT:
                running=False
                
        if key.get_pressed()[27]: running=False
        
        me.move()
        dude.move(me)
        for k in kit:
            k[0].gain(me)
            
        if checkPic(me,me.pic,dude,dude.pic)==True:
            dude.x=dude.x-50
            me.hit()
            hbar=(50,50,me.health,20)
                
        if t.torchTime(t.start)!=True:
            t.torch(pic,me.x,me.y)
                
        me.draw()
        dude.draw()
        for k in kit:
            k[0].draw()
        draw.rect(screen,(255,255,255),(50,50,200,20))
        draw.rect(screen,(255,0,0),hbar)
        screen.blit((text.render(str(t.torchCount()),True,(255,255,255))),(50,80))
        display.flip()
            
        if gameEnd(me)==True:
            screen.fill((0,0,0))
            screen.blit((text.render("GAME OVER",True,(255,255,255))),(360,280))
            display.flip()
            time.wait(1000)
            quit()
        myClock.tick(60)
        
    return "menu"    
    
def instructions():
    running = True
    inst = image.load("instructions.jpg")
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
    cred = image.load("credits.jpg")
    cred = transform.smoothscale(cred, screen.get_size())
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"
    
"""
def story():
    running = True
    story = image.load("story.png")
    story = transform.smoothscale(story, screen.get_size())
    screen.blit(story,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False
        display.flip()
    return "menu"
"""    


def menu():
    global text
    running = True
    myClock = time.Clock()
    menuimg = image.load("menucave.jpg")
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
            #draw.circle(screen,(222,55,55),(r.x+50,r.y+20),20)
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

def mfSelect():
    global text
    running=True
    buttons=[Rect(160*i,200,120,50) for i in range(1,4,2)]
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
        screen.blit(text.render(labels[0],True,(255,255,255)),(190,220))
        screen.blit(text.render(labels[1],True,(255,255,255)),(490,220))
        display.flip()
        
# This is the important part of the example.
# The idea is we have a variable (page) that keeps
# track of which page we are one. We give control
# of the program to a function until it is done and
# the program returns the new page it should be on.

running = True
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "story":
        me=sprites[mfSelect()]
        page = story(me)
    if page == "instructions":
        page = instructions()        
    if page == "credits":
        page = credit()    
    
quit()
