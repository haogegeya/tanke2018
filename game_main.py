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
#英雄类
screen=pygame.display.set_mode((800,600),0,32)
SCREEN_COLLOR=(255,255,255)
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


def game_main(tanke):
    screen.fill(SCREEN_COLLOR)
    for i in tanke:
        x=tanke[i][0]
        y=tanke[i][1]
        z=tanke[i][2]
        t=Tanke(screen,x,y,z)
        t.show()
    pygame.display.update()
    # sleep(0.05)

