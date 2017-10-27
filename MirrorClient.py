#!/usr/bin/python3
import socket
import threading
import socketFW
import time
import socketmsg
import json
import pickle
def startproxy(localport, remotehost, remoteport):
    remotesocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remotesocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        remotesocket.connect((remotehost, remoteport))
    except ConnectionRefusedError:
        print("ConnectionRefused")
        return
    localsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    localsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        localsocket.connect(("127.0.0.1",localport))
    except ConnectionRefusedError:
        print("localport: ConnectionRefused")
        remotesocket.close()
        return
    socketFW.socketForward(localsocket,remotesocket)

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
        localport=int(linkmsg["port"])
        remotehost=host
        remoteport=int(linkmsg["proxyport"])
        threading.Thread(target=startproxy,args=(localport, remotehost, remoteport,)).start()

    print("ConnectionClosed")
    req.close()
