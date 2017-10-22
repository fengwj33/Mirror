#!/usr/bin/python3
import socket
import threading
def forward_oneway(pin,pout,flag):
    bsize=1024
    pin.settimeout(2)
    while True:
        try:
            data=pin.recv(bsize)
        except socket.timeout:
            if flag[0]==False:
                print("pip closed")
                pin.close()
                return
            continue
        except socket.error:
            print (e)
            return
        else:
            if flag[0]==False:
                print("pip closed")
                pin.close()
                return
            pout.send(data)
            if len(data)==0:
                pin.close()
                flag[0]=False
                return
def socketForward(socket1,socket2):
    flag=[True]
    threading.Thread(target=forward_oneway,args=(socket1,socket2,flag,)).start()
    threading.Thread(target=forward_oneway,args=(socket2,socket1,flag,)).start()
    