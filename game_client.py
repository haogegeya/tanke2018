import pygame
from pygame.locals import *
from sys import exit
from socket import socket
from multiprocessing import Process,Pipe,Queue
import random
from time import sleep
from threading import Thread
c=socket()
c.connect(("127.0.0.1",6995))
fa1,fa2=Pipe()
fb1,fb2=Pipe()
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
        data=name+","+str(x)+","+str(y)
        if len(data) !=15:
            n=15-len(data)
            data=data+","+"#"*(n-1)
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
        x=random.randrange(800)
        y=random.randrange(600)
        fa2.send((x,y))
        data=fb1.recv()
        name=data[0]
        x=int(data[1])
        y=int(data[2])
        sleep(0.01)
        



p1=Process(target=shuju_f,args=(c,))
p2=Process(target=shuju_s,args=(c,))
p1.start()
p2.start()

t=Thread(target=shuju)
t.daemon=True
t.start()


# p1.join()
# p2.join()
# p3.join()
