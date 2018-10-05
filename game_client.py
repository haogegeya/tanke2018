from socket import socket
from multiprocessing import Process
import random
from time import sleep
c=socket()
c.connect(("127.0.0.1",6996))
def shuju_f(c):
    while True:
        x=random.randrange(100)
        y=random.randrange(100)
        data="#A"+","+str(x)+","+str(y)
        c.send(data.encode())
        sleep(2)
def shuju_s(c):
    while True:
        data=c.recv(128)
        data=data.decode().split(",")
        name=data[0]
        x=data[1]
        y=data[2]
        print((name,x,y))
p1=Process(target=shuju_f,args=(c,))
p2=Process(target=shuju_s,args=(c,))
p1.start()
p2.start()
# p1.join()
# p2.join()



