#!usr/bin/env python3
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
c.connect(("127.0.0.1",6999))
# c.connect(("192.168.207.132",6999))
# c.connect(("192.168.43.161",6995))
# c.connect(("172.40.78.146",6999))
#后面收数据，发数据，产生数据模块，游戏主逻辑分为四个进程，下面管道用于进程通信
fa1,fa2=Pipe()
# fb1,fb2=Pipe()
q=Queue()

name=input("输入昵称：")
while True:
    c.send(name.encode())
    data=c.recv(128)
    if data==b"OK":
        NAME=name
        break
    else:
        name=input("重复了，重新输入：")

#发送数据模块
def shuju_f(c):
    while True:
        data=fa1.recv()
        #如果是#则补给被吃了,请求服务端重新生成一个
        if data =="#":
            c.send(b"#")
        else:
            x=data[0]
            y=data[1]
            z=data[2]
            e=data[3]
            #用＠来区别数据是坦克的数据
            data="@"+","+name+","+str(x)+","+str(y)+","+str(z)+","+str(e)
            #用户名最大７个字符
            if len(data) !=20:
                n=15-len(data)
                data=data+","+"#"*(n-1)
            c.send(data.encode())
            # print(data)
            #处理进程退出
            if z==0:
                break

#接受数据模块
def shuju_s(c):
    while True:
        data=c.recv(20)
        # print(data.decode())
        data=data.decode().split(",")
        if data[0]=="@":
            # print(data)
            data_tanke=data.copy()
            name=data_tanke[1]
            x=data_tanke[2]
            y=data_tanke[3]
            z=data_tanke[4]
            e=data_tanke[5]
            q.put(["@",name,int(x),int(y),int(z),int(e)])
            #处理进程退出
            if NAME==name and int(z)==0:
                exit()
        elif data[0]=="#":
            print(data)
            data_buji=data.copy()
            x=data_buji[1]
            y=data_buji[2]
            q.put(["#",int(x),int(y)])

#数据产生及更新模块
def shuju():
    x=random.randrange(800)
    y=random.randrange(600)
    #z用来判断坦克方向
    z=random.randint(1,4)
    #e=1的时候发射一颗子弹
    e=0
    move_speed=5
    move_x=0
    move_y=0
    while True:
        sleep(0.05)
        for event in pygame.event.get():
            if event.type==QUIT:
                z=0
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
                if event.key==K_SPACE:
                    e=1
            if event.type==KEYUP:
                move_x=0
                move_y=0
                # e=0
        x+=move_x
        y+=move_y
        fa2.send((x,y,z,e))
        e=0
        #处理进程退出
        if z==0:
            exit()

#游戏主逻辑模块
def main():
    tanke={}
    die_tanke_list=[]
    while True:
        try:
            data=q.get(False)
        except:
            try:
                data=data_none
            except:
                continue
            else:
                pass
        else:
            if data[0]=="@":
                data_none=data.copy()
                data_none[5]=0

        # if data[0] in die_tanke_list:
        #     continue
        # print(data)
        if data[0]=="@":
            if data[4]==0:
                if data[1] in die_tanke_list:
                    die_tanke_list.remove(data[1])
                    if data[1]==NAME:
                        exit()
                #处理其他坦克退出
                try:
                    tanke.pop(data[1])
                except:
                    continue
                else:
                    print(tanke)
                    # print(tanke)
                        #处理进程退出
                    if data[1]==NAME:
                        exit()
                    # continue
            else:
                if data[1] in die_tanke_list:
                    continue

            #这里数据放入列表方便后面更改数据
            tanke[data[1]]=[data[2],data[3],data[4],data[5]]
        elif data[0]=="#":
            tanke["buji"]=[data[1],data[2]]
        # print(tanke)
        die_tanke,die_buji,tanke_buji=game_main(tanke)
        if die_tanke ==0:
            pass
        else:
            print("sssssssssssssss")
            tanke.pop(die_tanke)
            die_tanke_list.append(die_tanke)
        if die_buji:
            tanke.pop("buji")
            if tanke_buji==NAME:
                fa2.send("#")
        sleep(0.001)


p_list=[]
for i in range(4):
    if i==0:
        p=Process(target=shuju_f,args=(c,))
    elif i==2:    
        p=Process(target=shuju_s,args=(c,))
    elif i==3:
        p=Process(target=main)
    else:  
        p=Process(target=shuju)
    p_list.append(p)
    p.start()

for i in p_list:
    i.join()
# sleep(100)
c.close()