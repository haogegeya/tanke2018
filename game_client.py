import pygame
from pygame.locals import *
from sys import exit
from socket import socket
from multiprocessing import Process,Pipe,Queue
import random
from time import sleep
from threading import Thread
from game_main import *
c=socket()
c.connect(("127.0.0.1",6995))
fa1,fa2=Pipe()
fb1,fb2=Pipe()
fc1,fc2=Pipe()
name=input("输入昵称：")
while True:
    c.send(name.encode())
    data=c.recv(128)
    if data==b"OK":
        # name_shuju=(name,x,y)
        break
    else:
        name=input("重复了，重新输入：")


def shuju_f(c):
    while True:
        data=fa1.recv()
        x=data[0]
        y=data[1]
        z=data[2]
        data=name+","+str(x)+","+str(y)+","+str(z)
        if len(data) !=15:
            n=15-len(data)
            data=data+","+"#"*(n-1)
        c.send(data.encode())
        # sleep(2)
def shuju_s(c):
    while True:
        data=c.recv(15)
        data=data.decode().split(",")
        name=data[0]
        x=data[1]
        y=data[2]
        z=data[3]
        fc2.send((name,int(x),int(y),int(z)))
        # print((name,x,y,z))
def shuju():
    x=random.randrange(800)
    y=random.randrange(600)
    z=random.randint(1,4)
    move_speed=5
    move_x=0
    move_y=0
    while True:
        sleep(0.05)
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            if event.type==KEYDOWN:
                if event.key==K_LEFT:
                    z=4
                    move_x=-move_speed
                if event.key==K_RIGHT:
                    z=2
                    move_x=move_speed
                if event.key==K_UP:
                    z=1
                    move_y=-move_speed
                if event.key==K_DOWN:
                    z=3
                    move_y=move_speed
            if event.type==KEYUP:
                move_x=0
                move_y=0
        x+=move_x
        y+=move_y
        fa2.send((x,y,z))
        # data=fb1.recv()
        # name=data[0]
        # x=int(data[1])
        # y=int(data[2])
        # z=int(data[3])
        # data=(x,y,z)
        # # print(data)
        # fc2.send(data)
def main():
    tanke={}
    while True:
        data=fc1.recv()
        print(data)
        tanke[data[0]]=(data[1],data[2],data[3])
        game_main(tanke)
        sleep(0.01)

p1=Process(target=shuju_f,args=(c,))
p2=Process(target=shuju_s,args=(c,))
p3=Process(target=main)
p1.start()
p2.start()
p3.start()
t=Thread(target=shuju)
t.daemon=True
t.start()



# p1.join()
# p2.join()
# p3.join()


