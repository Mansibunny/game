#torchCount.py
#decreases torches during countdown
#tracks character health after colliding with enemy

from pygame import *
from math import *
from random import *
from datetime import datetime

screen=display.set_mode((800,600))
pic=transform.smoothscale(image.load("background.jpg").convert(),(800,600))
char=[0,400,-8,True]
init()
text=font.SysFont("Times New Roman",20)

#--PLAYER--
class Player:
    "tracks current position, velocity, platform, and health"
    def __init__(char):
        char.x=0
        char.y=400
        char.vy=0
        char.step=True
        char.health=100

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
        if char.y>400:
            char.y=400
            char.step=True
        char.vy+=0.5
    """    
    def check(char,obj2):
        space=20 
        if dist(char.x,obj2.x,char.y,obj2.y)<space:
            return True
    """    
    def hit(char):
        char.health-=1
        return char.health
    
    #--DRAWING STUFF--        
    def draw(char):
        draw.circle(screen,(0,0,255),(int(char.x),int(char.y)),10)
        
#--ENEMY--
class Enemy:
    "tracks start pos, current pos, speed"
    
    def __init__(self,x,y):
        self.startX=x
        self.startY=y
        self.x=x
        self.y=y
        self.speed=8

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
        draw.circle(screen,(255,0,0),(int(self.x),int(self.y)),10)
        
#--FUNCTION--
def dist(x1,x2,y1,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def checkCollide(obj1,pic1,obj2,pic2):
    space=pic2.get_width()//2+pic1.get_width()//2
    if dist(obj1.x,obj2.x,obj1.y,obj2.y)<space:
        return True

def check(char,obj2,space):
    if dist(char.x,obj2.x,char.y,obj2.y)<space:
        return True
    
#--OBJECTS--    
class Torch:
    def __init__(self):
        self.start=datetime.now()
   
    def torchTime(self,start):
        now=datetime.now()
        if now.hour*3600+now.minute*60+now.second-10>=start.hour*3600+start.minute*60+start.second:
            return True
        else:
            return False
    
    def torchCount(self):
        now=datetime.now()
        self.num=10-(now.hour*3600+now.minute*60+now.second-(self.start.hour*3600+self.start.minute*60+self.start.second))
        return self.num
   
    def torch(self,pic,x,y): #takes pic, position and makes transparent black screen with size
                        #of pic and white circle at position
        dark=Surface((pic.get_width(),pic.get_height()))
        dark.set_alpha(100)
        dark.fill((0,0,0))
        draw.circle(dark,(111,111,111),(int(x),int(y)),60)
        draw.circle(dark,(200,200,200),(int(x),int(y)),45)
        #draw.circle(dark,(255,255,255),(int(x),int(y)),25)
        screen.blit(pic,(0,0))
        screen.blit(dark,(0,0))
        #replace with photoshop and transparent circle pic

#--ENDS GAME--
def gameEnd():
    if t.torchCount()==0 or me.hit()==0:
        return True
    else:
        return False
    
dude=Enemy(randint(100,700),400)
me=Player()
t=Torch()
running=True
myClock=time.Clock()
hbar=(50,50,100,20)

while running:
    for e in event.get():
        if e.type==QUIT:
            running=False
    me.move()
    dude.move(me)
    
    if check(me,dude,20)==True:
        dude.x=dude.x-50
        me.hit()
        hbar=(50,50,me.hit(),20)
    
    if t.torchTime(t.start)!=True:
        t.torch(pic,me.x,me.y)
    else:
        break
        
    me.draw()
    dude.draw()
    draw.rect(screen,(255,255,255),(50,50,100,20))
    draw.rect(screen,(255,0,0),hbar)
    screen.blit((text.render(str(t.torchCount()),True,(255,255,255))),(50,80))
    display.flip()

    #if gameEnd()==True:
        #break      
    myClock.tick(60)


screen.fill((0,0,0))
screen.blit((text.render("GAME OVER",True,(255,255,255))),(360,280))
display.flip()
time.wait(2000)
quit()
