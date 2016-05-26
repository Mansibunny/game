#fonts.py
#goes through font list and gives samples; will look through later

from pygame import *
screen=display.set_mode((800,600))

font.init()

for f in font.get_fonts():
    screen.fill((0,0,0))
    text=font.SysFont(f,50)
    screen.blit(text.render("sample",True,(255,255,255)),(320,250))
    display.flip()
    print(font.get_fonts().index(f))
    time.wait(500)
