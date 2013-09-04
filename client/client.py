#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 21:37:26 2013
@Author: Daddiego Lucas
"""
import socket
import sys
import os


def clear_screen():
    if ( os.name=="nt"):
        cmd="cls"
    else:
        cmd="clear"
    os.system(cmd)

def main():
    
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("XMPlay Remote Control Server")
    print("")
    ip = str(input("Insert the IP address of the server: "))
    port = int(input("Insert the port: "))
    clear_screen()
    data = ""
    message="No command executed."
    song_title="Write some command."
    while (data != "exit"):
        try:
            # Connect to server and send data    
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
                print("XMPlay Remote Control Client Command Line")
                print("************ Info Window ************")
                print("")
                print("Message from the server: " + message)
                print("Song title: " + song_title)
                print("")
                print("**************************************")
                print("")
                print("Avaiable Commands: ")
                print("play,pause,stop,next,prev,update")
                print("Type exit to quit.")
                data = str(input("Type a command in lowercase and press enter: "))
                
                if (data.strip() != "exit"):
                    sock.connect((ip, port))
                    sock.sendall(bytes(data + "\n", "utf-8"))
                    received = str(sock.recv(1024), "utf-8").partition("|")
                    message=received[0]
                    song_title=received[2]
                    clear_screen()
                    
        except:
            print("Error: ",sys.exc_info()[0])    
            input("Press enter to continue.")
            break
        
        finally:
            sock.close()

if (__name__ == "__main__"):
    main()