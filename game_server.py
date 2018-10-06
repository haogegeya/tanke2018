from socket import *
from os import fork
from multiprocessing import  Pipe,Queue

s=socket(family=AF_INET,type=SOCK_STREAM,proto=0)
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(("0.0.0.0",6996))
s.listen(3)
socket_l=Queue()
l={}
fa1,fa2=Pipe(False)     
def shuju_s(c):
    while True:
        data=c.recv(128)
        print(data.decode())
        fa2.send(data)

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
                p=fork()
                if p==0:
                    shuju_s(c)
                else:
                    break
            else:
                c.send(b"NO")


   # ---------------------- 
    # if p==0:
    #     do_shuju_s(c)
    # else:
    #     p=fork()
    #     if p==0:
    #         shuju_f(l)
    #     else:
    #         continue
   # ---------------------- 
   # ---------------------- 
    # if p==0:
    #     q=fork()
    #     if q==0:
    #         shuju_s(c)
    #     elif q>0:
    #         shuju_f()
    #     else:
    #         print("创建进程失败")
    # else:
    #     continue
   # ---------------------- 









    
