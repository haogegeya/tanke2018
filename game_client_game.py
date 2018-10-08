import pygame
from pygame.locals import *
from sys import exit
from socket import socket
from multiprocessing import Process,Pipe,Queue
import random
from time import sleep
from threading import Thread
c=socket()
c.connect(("127.0.0.1",6996))
fa1,fa2=Pipe()
fb1,fb2=Pipe()
x=random.randint(0,800)
y=random.randint(0,600)
name=input("输入昵称：")
while True:
    c.send(name.encode())
    data=c.recv(128)
    if data==b"OK":
        name_shuju=(name,x,y)
        break
    else:
        name=input("重复了，重新输入：")


# background_image_filename="315464.jpg"
mouse_image_filename="0.png"
pygame.init()
screen=pygame.display.set_mode((800,600),0,32)
pygame.display.set_caption("hello timer")
SCREEN_COLLER=(255,255,255)
# Abackground=pygame.image.load(background_image_filename).convert()
mouse_cursor=pygame.image.load(mouse_image_filename).convert_alpha()


def shuju_f(c):
    while True:
        # x=random.randrange(100)
        # y=random.randrange(100)
        data=fa1.recv()
        x=data[0]
        y=data[1]
        data=name+","+str(x)+","+str(y)
        c.send(data.encode())
        # sleep(2)
def shuju_s(c):
    while True:
        data=c.recv(128)
        data=data.decode().split(",")
        name=data[0]
        x=data[1]
        y=data[2]
        fb2.send((name,x,y))
        print((name,x,y))
def shuju():
    while True:
        global x,y,name_shujue
        x,y=pygame.mouse.get_pos()
        fa2.send((x,y))
        data=fb1.recv()
        name=data[0]
        x=int(data[1])
        y=int(data[2])
        


def game_main():
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
        
        screen.blit(mouse_cursor,(x,y))
        sleep(0.05)


p1=Process(target=shuju_f,args=(c,))
p2=Process(target=shuju_s,args=(c,))
p1.start()
p2.start()

t=Thread(target=shuju)
t.daemon=True
t.start()
t1=Thread(target=game_main)
t1.daemon=True
t1.start()

while True:
    # e.wait()
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
    pygame.display.update()
    screen.fill(SCREEN_COLLER)
    sleep(0.05)

# p1.join()
# p2.join()
# p3.join()
