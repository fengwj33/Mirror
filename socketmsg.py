#!/usr/bin/python3
import socket
import threading
import struct
def send(csocket,msg):
    head=struct.pack('Q',len(msg))
    csocket.send(head+msg)
    #csocket.send(msg)
def rcv(csocket):
    rval=bytes()
    length=csocket.recv(8)
    if len(length)==0:
        return rval
    length,=struct.unpack('Q',length)
    bsize=1024
    rem=length
    while rem!=0:
        if rem>bsize:
            temp=csocket.recv(bsize)
        else:
            temp=csocket.recv(rem)
        rem-=len(temp)
        rval+=temp
    return rval