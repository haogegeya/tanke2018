import pygame
from pygame.locals import *
from random import randint
from time import sleep
herol=pygame.image.load("./image/tankel.bmp")
heror=pygame.image.load("./image/tanker.bmp")
herou=pygame.image.load("./image/tankeu.bmp")
herod=pygame.image.load("./image/tanked.bmp")
zidan1=pygame.image.load("./image/zidian1.bmp")
zidan2=pygame.image.load("./image/zidian2.bmp")
tanke_image={"l":herol,"r":heror,"u":herou,"d":herod}
#英雄类
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


def game_main():
    pygame.init()
    screen=pygame.display.set_mode((800,600),0,32)
    SCREEN_COLLOR=(255,255,255)
    while True:
        x=randint(0,800)
        y=randint(0,600)
        z=randint(1,4)
        screen.fill(SCREEN_COLLOR)
        tanke=Tanke(screen,x,y,z)
        tanke.show()
        pygame.display.update()
        sleep(0.5)

game_main()

