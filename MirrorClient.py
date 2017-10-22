#!/usr/bin/python3
import socket
import threading
import socketFW
import time
import socketmsg
import json
import pickle
def startproxy(rcv,host,port):
    snd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    snd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    snd.connect((host,port))
    socketFW.socketForward(rcv,snd)

fcfg=open('clientcfg.json', 'r')
cfg= json.load(fcfg)
while True:
    req=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host=cfg["serverip"]
    port=int(cfg["serverport"])
    while True:
        try:
            req.connect((host,port))
            break
        except ConnectionRefusedError:
            print("ConnectionRefused")
            time.sleep(1)
    print("success")
    while True:
        data=socketmsg.rcv(req)
        if len(data)==0:
            break
        linkmsg=pickle.loads(data)
        proxyhost=host
        proxyport=int(linkmsg["proxyport"])
        proxysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        proxysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxysocket.connect((proxyhost,proxyport))
        startproxy(proxysocket,"127.0.0.1",int(linkmsg["port"]))
    print("ConnectionClosed")
    proxysocket.close()