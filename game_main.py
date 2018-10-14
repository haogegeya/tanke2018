import pygame
from pygame.locals import *
from random import randint
from time import sleep
from sys import exit
from xiangjiaopanduan import *
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

z_width=zidan1.get_width()
z_height=zidan1.get_height()
t_width=herol.get_width()
t_height=herol.get_height()
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

    def tanke_die(self,zidan_list):
        for zidan_i in zidan_list:
            if ju_ju(zidan_i.x,zidan_i.y,z_width,z_height,self.x,self.y,t_width,t_height):
                return True
            else:
                return False

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
#处理所有坦克的子弹
def zidan_show(tanke):
    global zidan_list
    for i in tanke:
        e=tanke[i][3]
        if e==1:
            x=tanke[i][0]
            y=tanke[i][1]
            z=tanke[i][2]
            zidan=Zidan(screen,x,y,z)
            zidan_list.append(zidan)
            print(len(zidan_list))
    for i in zidan_list:
        if i.die():
            zidan_list.remove(i)
        i.show()
        i.move()


#显示坦克的位置
def tanke_show(tanke):
    for i in tanke:
        x=tanke[i][0]
        y=tanke[i][1]
        z=tanke[i][2]
        t=Tanke(screen,x,y,z)
        if t.tanke_die(zidan_list):
            pass
        else:
            t.show()




def game_main(tanke):
    screen.fill(SCREEN_COLLOR)
    tanke_show(tanke)
    zidan_show(tanke)
    pygame.display.update()