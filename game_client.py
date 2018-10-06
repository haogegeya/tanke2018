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
name=input("输入昵称：")
while True:
    c.send(name.encode())
    data=c.recv(128)
    if data==b"OK":
        break
    else:
        name=input("重复了，重新输入：")

fa1,fa2=Pipe()
fb1,fb2=Pipe()
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
        fb2.send((x,y))
        print((name,x,y))
def game_main():
    background_image_filename="315464.jpg"
    mouse_image_filename="0.png"
    pygame.init()
    screen=pygame.display.set_mode((800,600),0,32)
    pygame.display.set_caption("hello timer")
    # Abackground=pygame.image.load(background_image_filename).convert()
    mouse_cursor=pygame.image.load(mouse_image_filename).convert_alpha()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
        # screen.blit(Abackground,(0,0))
        screen.fill((255,255,255))

        x,y=pygame.mouse.get_pos()
        fa2.send((x,y))
        data=fb1.recv()
        x=int(data[0])
        y=int(data[1])
        x-=mouse_cursor.get_width()/2
        y-=mouse_cursor.get_height()/2

        screen.blit(mouse_cursor,(x,y))

        pygame.display.update()
        sleep(0.05)


p1=Process(target=shuju_f,args=(c,))
p2=Process(target=shuju_s,args=(c,))
p3=Process(target=game_main)
p1.start()
p2.start()
p3.start()
# p1.join()
# p2.join()
# p3.join()
