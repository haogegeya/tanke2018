#!/usr/bin/env python3
from socket import *
from os import fork,wait
from multiprocessing import  Pipe,Queue,Process
from time import sleep
from sys import exit
from random import randint,choice
from threading import Thread

s=socket(family=AF_INET,type=SOCK_STREAM,proto=0)
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(("0.0.0.0",6999))
s.listen(5)
socket_l=Queue()
socket_L=Queue()
l={}
fa1,fa2=Pipe(False)




#接受玩家的数据 
def shuju_s(c,name):
    while True:
        try:
            data=c.recv(25)
        except:
            print(name,"退出了游戏")
        finally:
            if data==b"@@":
                print(name,"退出了游戏")
                socket_L.put(name)
                c.close()
                exit()
            else:
                fa2.send(data)
        
#把接受的任意来源的数据发送给所有人
def shuju_f():

    #把退出了的客户端放在一个列表
    exit_c=""
    while True:
        # print("---------------")
        try:
            data=fa1.recv()
        except:
            print("服务器退出")
            exit()
        else:
            if socket_l.empty():
                pass
            else:
                l=socket_l.get()
            
            #下面的这几行代码用来处理某个客户端退出与下面的代码片段2一起作用,简直是艺术
            for i in l:
                try:
                    i.send(data)
                except:
                    #这里发生异常说明i退出了游戏
                    exit_c=i
            if exit_c != "":
                print("删除了",l[exit_c])
                l.pop(exit_c)
                socket_l.put(l)
                exit_c=""

def lianjie_c(s):     
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
                        #创造二级子进程处理僵尸进程问题
                        p1=fork()
                        if p1==0:
        #每连接一个玩家就单独创建一个进程接受此玩家的数据
                            shuju_s(c,name)
                        else:
                            exit()
                    else:
                        #阻塞等待一级子进程退出
                        pid,status = wait()
                        print("========",pid)
                        break
                else:
                    c.send(b"NO")


p_list=[]
for i in range(2):
    if i==0:
        p=Process(target=shuju_f)
    elif i==1:
        p=Process(target=lianjie_c,args=(s,))
    p_list.append(p)
    p.start()
