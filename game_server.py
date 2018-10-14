from socket import *
from os import fork
from multiprocessing import  Pipe,Queue
from time import sleep
from sys import exit


s=socket(family=AF_INET,type=SOCK_STREAM,proto=0)
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(("0.0.0.0",6999))
s.listen(3)
socket_l=Queue()
socket_L=Queue()
l={}
fa1,fa2=Pipe(False)
#接受玩家的数据 
def shuju_s(c,name):
    while True:
        data=c.recv(15)
        # print(len(data.decode()))
        # print(data.decode())
        if data==b"":
            socket_L.put(name)
            exit()
        else:
            fa2.send(data)
        # fa2.send(data)
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
        # if socket_L.empty():
        #     pass
        # else:
        #     c=socket_L.get()
            # exit_c.append(c)
            # socket_L.put(c)
        # print(data)
        # print(len(l))
        for i in l:
            try:
                i.send(data)
                print(data)
            except:
                print(len(l))
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
            # if socket_l.empty():
            #     pass
            # else:
            #     l=socket_l.get()
            if socket_L.empty():
                pass
            else:
                n=socket_L.get()
                for i in l:
                    if l[i]==n:
                        exit_c=i
                l.pop(exit_c)
                socket_l.put(l)
                print("-----------------------------------------")

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
