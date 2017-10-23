#!/usr/bin/python3
import socket
import threading
import socketFW
import time
import socketmsg
import json
import pickle
import queue
def startdevicelistener(cfg):
    global devicesocket
    devicelistener=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    devicelistener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host="0.0.0.0"
    port=int(cfg["serverport"])
    devicelistener.bind((host,port))
    devicelistener.listen(5)
    while True:
        clientsocket,addr=devicelistener.accept()
        devicesocket=clientsocket
        print("#device#:",addr,"\t\t[linked]")


def startproxylistener(proxysocketdic,proxyport):
    print("proxylistener:\t"+str(proxyport)+"\t\t[start]")
    listener=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("0.0.0.0",proxyport))
    listener.listen(5)
    while True:
        clientsocket,addr=listener.accept()
        print("proxylistener:\t"+str(proxyport)+" is connected")
        proxysocketdic[proxyport].put(clientsocket)


def startuserlistener(proxysocketdic,userport,proxyport,port):
    print("userlistener:\t"+str(userport)+"\t\t[start]")
    global devicesocket
    userlistener=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    userlistener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host="0.0.0.0"
    userlistener.bind((host,userport))
    userlistener.listen(5)
    while True:
        clientsocket,addr=userlistener.accept()
        print("userlistener:\t"+str(userport)+" is connected")
        if devicesocket==None:
            clientsocket.close()
            print("[error]cannot find device, connection is closed")
            continue
        socketmsg.send(devicesocket,pickle.dumps({"proxyport":proxyport,"port":port}))
        timer=0
        while proxysocketdic[proxyport].empty()==True:
            time.sleep(0.1)
        proxysocket=proxysocketdic[proxyport].get()
        print("userlistener:\t"+str(userport)+"\t\t[success]")
        print("userlistener:\t"+str(userport)+"\t\t[startproxy]")
        socketFW.socketForward(clientsocket,proxysocket)

def socketdaemon():
    global devicesocket
    while True:
        if devicesocket==None:
            time.sleep(1)
            continue
        data=devicesocket.recv(1024)
        if len(data)==0:
            print("#device#\t\t\t[removed]")
            devicesocket=None

devicesocket=None
fcfg=open('servercfg.json', 'r')
cfg= json.load(fcfg)
bindcfg=cfg["portbinds"]
threading.Thread(target=startdevicelistener,args=(cfg,)).start()
threading.Thread(target=socketdaemon,args=()).start()
proxysocketdic={}
for key in bindcfg:
    proxyport=int(bindcfg[key][0])#device connect to this port
    userport=int(bindcfg[key][1])#user connect to this port
    port=int(key)#the port that user want to connect
    proxysocketdic[proxyport]=queue.Queue()
    threading.Thread(target=startproxylistener,args=(proxysocketdic,proxyport,)).start()
    threading.Thread(target=startuserlistener,args=(proxysocketdic,userport,proxyport,port,)).start()


while True:
    time.sleep(60)

