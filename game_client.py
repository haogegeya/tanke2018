#!usr/bin/env python3
import pygame
from pygame.locals import *
from sys import exit
from socket import socket
from multiprocessing import Process,Pipe,Queue
import random
from time import sleep,time
from threading import Thread
from game_main import *
import os
from xiangjiaopanduan import ju_ju


#图片加载一直报警告,百度都没N长时间都没解决,这里清屏骗骗自己
os.system("clear")
print("1.单人游戏")
print("2.双人游戏")
print("3.三人游戏")
print("4.多人乱斗")
while True:
    try:
        player=int(input("请输入"))
    except:
        print("输入错误,重新输入")
        continue
    else:
        if player not in (1,2,3,4,5):
            print("输入错误,重新输入")
            continue
        else:
            break

if player==1:
    ADDR=6996
elif player==2:
    ADDR=6997
elif player==3:
    ADDR=6998
else:
    ADDR=6999
c=socket()
try:
    c.connect(("172.40.78.147",ADDR))
except:
    print("服务器异常")
    exit()
# c.connect(("192.168.207.132",6999))
# c.connect(("192.168.43.161",6995))
# c.connect(("172.40.78.146",6999))
#后面收数据，发数据，产生数据模块，游戏主逻辑分为四个进程，下面管道用于进程通信
fa1,fa2=Pipe()
fb1,fb2=Pipe()
q=Queue()
q1=Queue()

name=input("输入昵称：")
while True:
    c.send(name.encode())
    data=c.recv(128)
    if data==b"OK":
        NAME=name
        # fb2.send("OK")
        break
    elif data==b"NO":
        name=input("重复了，重新输入：")
    else:
        print(data.decode())
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
            f=data[4]
            l=data[5]
            #用＠来区别数据是坦克的数据
            data="@"+","+name+","+str(x)+","+str(y)+","+str(z)+","+str(e)+","+str(f)+","+str(l)
            #用户名最大8个字符
            if len(data) !=25:
                n=20-len(data)
                data=data+","+"#"*(n-1)
            c.send(data.encode())
            # print(data)
            if z==0:
                #主动告诉服务器要退出了
                c.send(b"@@")
            #处理进程退出
                break

#接受数据模块
def shuju_s(c):
    n=0
    while True:
        data=c.recv(25)
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
            f=data_tanke[6]
            l=data_tanke[7]
            q.put(["@",name,int(x),int(y),int(z),int(e),int(f),int(l)])
            #处理进程退出
            if NAME==name and int(z)==0:
                exit()
        elif data[0]=="#":
            if n==0:
                print("等待玩家加入(%d/%d)"%(player,player))
                print("3秒后开始游戏")
                sleep(3)
                fb2.send("OK")
                n+=1
            # print(data)
            data_buji=data.copy()
            x=data_buji[1]
            y=data_buji[2]
            z=data_buji[3]
            q.put(["#",int(x),int(y),int(z)])
        #等待玩家连入游戏
        elif data[0]=="$":
            print(data[1])


#数据产生及更新模块
def shuju():
    if ADDR!=6999:
        data=fb1.recv()
    x=random.randrange(800)
    y=random.randrange(600)
    #z用来判断坦克方向
    z=random.randint(1,4)
    #e=1的时候发射一颗子弹
    e=0
    #默认0分
    f=0
    #默认3生命值
    l=3
    move_speed=5
    move_x=0
    move_y=0
    while True:
        sleep(0.05)
        try :
            data=q1.get(False)
        except:
            pass
        else:
            if data=="l-":
                l-=1
            elif data=="l+":
                l+=1
            elif data=="f1+":
                f+=1
            elif data=="f3+":
                f+=3
            elif data=="f5+":
                f+=5
            elif data=="t":
                z=0
            elif data=="l0":
                f=0
                l=3
            elif type(data)==int:
                f+=data
                l+=1

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
        x+=move_x
        y+=move_y
        if x<0:
            x=0
        elif x>750:
            x=750
        if y<0:
            y=0
        elif y>550:
            y=550
        if ju_ju(x,y,50,50,145,288,87,57):
            x-=move_x
            y-=move_y
        if ju_ju(x,y,50,50,525,132,82,57):
            x-=move_x
            y-=move_y
        if ju_ju(x,y,50,50,627,427,56,71):
            x-=move_x
            y-=move_y
        #  
        fa2.send((x,y,z,e,f,l))
        e=0
        #处理进程退出
        if z==0:
            exit()

#游戏主逻辑模块
def main():
    #存放坦克的位置,方向,是否发子弹等信息
    tanke={}
    die_tanke_list=[]
    n=0
    m=0
    while True:
        # try:
        #     data=q.get(False)
        # except:
        #     try:
        #         data=data_none
        #     except:
        #         continue
        #     else:
        #         pass
        # else:
        #     if data[0]=="@":
        #         data_none=data.copy()
        #         data_none[5]=0
        data=q.get()
    
        #收到的是坦克信息
        if data[0]=="@":
            if data[4]==0:
                if data[1]==NAME:
                    exit()
                else:
                    if data[1] in die_tanke_list:
                        die_tanke_list.remove(data[1])
                #处理其他坦克退出
                try:
                    tanke.pop(data[1])
                except:
                    continue
                
            else:
                if data[1] in die_tanke_list:
                    continue


            #这里数据放入列表方便后面更改数据
            tanke[data[1]]=[data[2],data[3],data[4],data[5],data[6],data[7]]

        #收到的是补给信息
        elif data[0]=="#":
            tanke["buji"]=[data[1],data[2],data[3]]
        #打印坦克信息(测试)
        # print(tanke)

        # 让循环只在第一次执行下面两段代码
        if n==0:
            time_start=time()
            n+=1
        if m==0:
            time_passed=clock.tick()
            m+=1
        #获取每次循环的时间差
        time_passed=clock.tick()
        time_passed_seconds=time_passed/1000.0

        die_tanke,die_zidan,die_buji,tanke_buji,time_if,if_birth=game_main(tanke,NAME,time_start,time_passed_seconds)
        if if_birth==1:
            die_tanke_list=[]
        #保证按一次空格发射一颗子弹
        if data[0]=="@" and data[5]==1:
            tanke[data[1]][3]=0
        #时间到了
        if time_if:
            print("结束游戏")
            # sleep(3)
            fb2.send(tanke)
            q1.put("t")

        if die_tanke ==0:
            pass
        else:
            # if tanke[die_tanke][5]==1:
            #     tanke.pop(die_tanke)
            #     die_tanke_list.append(die_tanke)
            if die_tanke==NAME:
                if tanke[die_tanke][5]<=1:
                    q1.put("l0")
                    tanke.pop(die_tanke)
                    die_tanke_list.append(die_tanke)
                else:
                    q1.put("l-")
            elif die_zidan==NAME:
                if tanke[die_tanke][5]<=1:
                    q1.put(tanke[die_tanke][4])
                    tanke.pop(die_tanke)
                    die_tanke_list.append(die_tanke)
                else:
                    q1.put("l+")



        if die_buji:
            buji_lei=tanke["buji"][2]
            tanke.pop("buji")
            if tanke_buji==NAME:
                fa2.send("#")
                if buji_lei==1:
                    q1.put("f1+")
                elif buji_lei==2:
                    q1.put("f3+")
                else:
                    q1.put("f5+")

        # sleep(0.001)


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
c.close()


data=fb1.recv()
sleep(3)
fenshu={}
for name in data:
    if name !="buji":
        fenshu[name]=[data[name][4],data[name][5]]

print(fenshu)
jieguo(fenshu)
