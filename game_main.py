import pygame
from pygame.locals import *
from random import randint,choice
from time import sleep
from sys import exit
from xiangjiaopanduan import*
pygame.init() 
screen=pygame.display.set_mode((800,600),0,32)

beijin=pygame.image.load("./image/Beijin.jpg")
herol=pygame.image.load("./image/tanke_l.png").convert()
heror=pygame.image.load("./image/tanke_r.png").convert()
herou=pygame.image.load("./image/tanke_u.png").convert()
herod=pygame.image.load("./image/tanke_d.png").convert()
herour=pygame.image.load("./image/tanke_ur.png").convert()
zidan1=pygame.image.load("./image/zidan1.png").convert()
buji1=pygame.image.load("./image/buji1.png").convert()
buji2=pygame.image.load("./image/buji2.png").convert()
tanke_image={"l":herol,"r":heror,"u":herou,"d":herod}
buji_image={1:buji1,2:buji2}

font=pygame.font.SysFont("Arial",16)

SCREEN_COLLOR=(255,255,255)

z_width=zidan1.get_width()
z_height=zidan1.get_height()
t_width=herol.get_width()
t_height=herol.get_height()
b_width=zidan1.get_width()
b_height=zidan1.get_height()
#这是个放子弹的列表
zidan_list=[]
#解决机器差异存在子弹不同步问题
clock=pygame.time.Clock()
n=0


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
                return True,zidan_i
        return False,0
    def tanke_eat(self,buji):
        if ju_ju(buji_i.x,buji_i.y,b_width,b_height,self.x,self.y,t_width,t_height):
            return True


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
    def move (self,time,speed=200):
        if self.z==1:
            self.y-=speed*time
        elif self.z==3:
            self.y+=speed*time
        elif self.z==4:
            self.x-=speed*time
        else:
            self.x+=speed*time

    def die(self):
        if self.x<=0:
            return True
        if self.x>=800:
            return True
        if self.y<=0:
            return True
        if self.y>=600:
            return True

#补给类
class Buji():
    def __init__(self,screen,x,y,z):
        self.screen=screen
        self.image=buji_image
        self.x=x
        self.y=y
        self.z=z
    def show(self):
        self.screen.blit(self.image[self.z],(self.x,self.y))
    def eat_buji(self,tanke):
        for i in tanke:
            if i !="buji":
                x=tanke[i][0]
                y=tanke[i][1]
                if ju_ju(x,y,t_width,t_height,self.x,self.y,b_width,b_height):
                    return True,i
        return False,0

#处理所有坦克的子弹
def zidan_show(tanke):
    global zidan_list,n
    for i in tanke:
        if i !="buji":
            e=tanke[i][3]
            if e==1:
                x=tanke[i][0]
                y=tanke[i][1]
                z=tanke[i][2]
                if z==1:
                    zidan=Zidan(screen,x+(t_width-z_width)/2,y-z_height-5,z)
                elif z==2:
                    zidan=Zidan(screen,x+t_width+5,y+(t_height-z_height)/4,z)
                elif z==3:
                    zidan=Zidan(screen,x+(t_width-z_width)/2,y+t_height+5,z)
                elif z==4:
                    zidan=Zidan(screen,x-z_width-5,y+(t_height-z_height)/4,z)


                zidan_list.append(zidan)
            #打印子弹个数(测试)
            # print(len(zidan_list))
    time=0
    for i in zidan_list:
        if i.die():
            zidan_list.remove(i)
        i.show()
        if n==0:
            time_passed=clock.tick()
            n+=1
        else:
            time_passed=clock.tick()
            time_passed_seconds=time_passed/1000.0
            if time!=0:
                pass
            else:
                time=time_passed_seconds
            i.move(time)


#显示坦克的位置
def tanke_show(tanke):
    global zidan_list
    # print(tanke)
    for i in tanke:
        if i !="buji":
            x=tanke[i][0]
            y=tanke[i][1]
            z=tanke[i][2]
            t=Tanke(screen,x,y,z)
            tanke_die,zidan_die=t.tanke_die(zidan_list)
            if tanke_die:
                zidan_list.remove(zidan_die)
                if tanke[i][5]>=2:
                    t.show()
                    return i
                else:
                    return i
            else:
                t.show()


    return 0

#处理补给
def buji_show(tanke):
    if "buji" in tanke:
        x=tanke["buji"][0]
        y=tanke["buji"][1]
        z=tanke["buji"][2]
        buji=Buji(screen,x,y,z)
        buji.show()
        return buji.eat_buji(tanke)
    else:
        return False,0


#显示分数等信息
def wenzi(tanke,NAME):
    for i in tanke:
        if i==NAME:
            print(tanke[i])
            text_f=str(tanke[i][4])
            text_l=str(tanke[i][5])
            font_f=font.render(text_f,True,(255,255,255))
            font_l=font.render(text_l,True,(255,255,255))
            screen.blit(font_f,(730,50))
            screen.blit(font_l,(730,80))
            break



#刷新显示桌面

def game_main(tanke,NAME):
    # screen.fill(SCREEN_COLLOR)
    screen.blit(beijin,(0,0))
    #tanke_die有坦克打死返回坦克名,没有返回0
    tanke_die=tanke_show(tanke)
    zidan_show(tanke)
    #buji_die是补给是否被吃了,buji_tanke是谁吃了
    buji_die,buji_tanke=buji_show(tanke)

    wenzi(tanke,NAME)
    pygame.display.update()
    return tanke_die,buji_die,buji_tanke