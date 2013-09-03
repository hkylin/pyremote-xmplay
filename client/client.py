#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 21:37:26 2013
@Author: Daddiego Lucas
"""
import socket

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = str(input("Insert the IP address of the server: "))
port = int(input("Input the port: "))

data = ""

while (data != "exit"):
    try:
        # Connect to server and send data    
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
            sock.connect((ip, port))
            data = str(input("Write some text, exit to quit: "))
            if (data != "exit"):
                sock.sendall(bytes(data + "\n", "utf-8"))
                print("Sent:     {}".format(data))
            
    finally:
        sock.close()
        del sock