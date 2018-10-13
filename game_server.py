from socket import *
from os import fork
from multiprocessing import  Pipe,Queue
from time import sleep

s=socket(family=AF_INET,type=SOCK_STREAM,proto=0)
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(("0.0.0.0",6995))
s.listen(3)
socket_l=Queue()
l={}
fa1,fa2=Pipe(False)

#接受玩家的数据   
def shuju_s(c):
    while True:
        data=c.recv(15)
        print(len(data.decode()))
        print(data.decode())
        fa2.send(data)
#把接受的任意来源的数据发送给所有人
def shuju_f():
    while True:
        print("---------------")
        data=fa1.recv()
        print("...............")
        if socket_l.empty():
            pass
        else:
            l=socket_l.get()
        print(data)
        # print(l)   
        for i in l:
            i.send(data)

p=fork()
if p==0:
#发送数据的进程
    shuju_f()
else:
    while True:
        c,a=s.accept()
        while True:
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
                    shuju_s(c)
                else:
                    break
            else:
                c.send(b"NO")
