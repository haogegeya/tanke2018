import pygame
from pygame.locals import *
from random import randint
from time import sleep
from sys import exit
pygame.init() 
herol=pygame.image.load("./image/tankel.bmp")
heror=pygame.image.load("./image/tanker.bmp")
herou=pygame.image.load("./image/tankeu.bmp")
herod=pygame.image.load("./image/tanked.bmp")
zidan1=pygame.image.load("./image/zidian1.bmp")
zidan2=pygame.image.load("./image/zidian2.bmp")
tanke_image={"l":herol,"r":heror,"u":herou,"d":herod}
screen=pygame.display.set_mode((800,600),0,32)
SCREEN_COLLOR=(255,255,255)
#坦克类
class Tanke():
    def __init__(self,screen,x,y,z):
        self.screen=screen
        self.image=tanke_image
        self.x=x
        self.y=y
        self.z=z

    def show(self):
        if self.z==1:
            self.screen.blit(self.image["u"],(self.x,self.y))
        if self.z==2:
            self.screen.blit(self.image["r"],(self.x,self.y))
        if self.z==3:
            self.screen.blit(self.image["d"],(self.x,self.y))
        if self.z==4:
            self.screen.blit(self.image["l"],(self.x,self.y))

#子弹类
class Zidan():
    def __init__(self,screen,x,y,z):
        self.screen=screen
        self.x=x
        self.y=y
        self.z=z
        self.image=zidan1
    def show(self):
        self.screen.blit(self.image,(self.x,self.y))
    def move (self,speed=1):
        if self.z==1:
            self.y-=speed
        elif self.z==3:
            self.y+=speed
        elif self.z==4:
            self.x-=speed
        else:
            self.x+=speed

    def die(self):
        if self.x<=0:
            return True
        if self.x>=800:
            return True
        if self.y<=0:
            return True
        if self.y>=600:
            return True
#这是个放子弹的列表
zidan_list=[]
def game_main(tanke):
    screen.fill(SCREEN_COLLOR)
    # print(len(tanke))
    for i in tanke:
        x=tanke[i][0]
        y=tanke[i][1]
        z=tanke[i][2]
        e=tanke[i][3]
        t=Tanke(screen,x,y,z)
        t.show()
        if e==1:
            # print(e)
            zidan=Zidan(screen,x,y,z)
            zidan_list.append(zidan)
            # tanke[i][3]=0
        print(len(zidan_list))
        for i in zidan_list:
            if i.die():
                zidan_list.remove(i)
            i.show()
            i.move()

    pygame.display.update()
    # sleep(0.05)

