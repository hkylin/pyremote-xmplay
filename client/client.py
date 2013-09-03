#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 21:37:26 2013
@Author: Daddiego Lucas
"""

import socket
import sys

HOST, PORT = "192.168.0.11", 9999
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data = ""

while (data != "close"):
    try:
        # Connect to server and send data    
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
            sock.connect((HOST, PORT))
            data = str(input("Write some text: "))        
            sock.sendall(bytes(data + "\n", "utf-8"))
            print("Sent:     {}".format(data))
    
            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
            print("Received: {}".format(received)) 
            
    finally:
        sock.close()
        del sock
        print("final")

