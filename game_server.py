#!/usr/bin/env python3
from socket import *
from os import fork
from multiprocessing import  Pipe,Queue
from time import sleep
from sys import exit
from random import randint
from threading import Thread

s=socket(family=AF_INET,type=SOCK_STREAM,proto=0)
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(("0.0.0.0",6999))
s.listen(5)
socket_l=Queue()
socket_L=Queue()
l={}
fa1,fa2=Pipe(False)
fb1,fb2=Pipe(False)


#发送补给数据
def shuju_b(c):
    while True:
        x=randint(50,750)
        y=randint(50,550)
        data="#"+","+str(x)+","+str(y)
        print(data)
        if len(data) !=20:
            n=15-len(data)
            data=data+","+"#"*(n-1)
        c.send(data.encode())
        data=fb1.recv()
        print(data)
#接受玩家的数据 
def shuju_s(c,name):
    t=Thread(target=shuju_b,args=(c,))
    t.start()
    while True:
        data=c.recv(20)
        if data==b"":
            socket_L.put(name)
            exit()
            c.close()
        else:
            if data ==b"#":
                fb2.send(data)
            else:
                fa2.send(data)
        
#把接受的任意来源的数据发送给所有人
def shuju_f():
    #把退出了的客户端放在一个列表
    exit_c=""
    while True:
        # print("---------------")
        data=fa1.recv()
        if socket_l.empty():
            pass
        else:
            l=socket_l.get()
        
        #下面的这几行代码用来处理某个客户端退出与下面的代码片段2一起作用,简直是艺术
        for i in l:
            try:
                i.send(data)
            except:
                print("断开了链接")
                exit_c=i
        if exit_c != "":
            print("删除了")
            l.pop(exit_c)
            socket_l.put(l)
            exit_c=""

            


p=fork()
if p==0:
#发送数据的进程
    shuju_f()
else:
    while True:
        print("等待连接中．．．．．．")
        c,a=s.accept()
        while True:
            #代码片段2
            if socket_L.empty():
                pass
            else:
                n=socket_L.get()
                for i in l:
                    if l[i]==n:
                        exit_c=i
                l.pop(exit_c)
                socket_l.put(l)
    

            data=c.recv(128)
            name=data.decode()
            if name not in l.values():
                c.send(b"OK")
                l[c]=name
                socket_l.put(l)
                sleep(0.01)
                p=fork()
                if p==0:
#每连接一个玩家就单独创建一个进程接受此玩家的数据
                    shuju_s(c,name)
                else:
                    break
            else:
                c.send(b"NO")
            # print(len(l))
