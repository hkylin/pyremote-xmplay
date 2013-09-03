#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 21:36:42 2013
@Author: Daddiego Lucas
"""

"""
Imports
"""
import sys
import socketserver
import threading


"""
Classes
"""
class DdeExecute():
    import win32ui
    import dde
    
    def __init__(self,app,topic):
        self.conversation = None
        self.app = app
        self.topic = topic
        self._setup_dde()     
    
    def _setup_dde(self):
        serv = self.dde.CreateServer()
        serv.Create("TC")
        self.conversation = self.dde.CreateConversation(serv)
        self.conversation.ConnectTo(self.app,self.topic)
        
    def exec_command(self,command):
        print(command)
        self.conversation.Exec(command)

class TcpHandler(socketserver.StreamRequestHandler):      
		
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        data = self.rfile.readline().strip()
        print("Server Says: {} wrote:".format(self.client_address[0]))
        data = str(data)[2:-1]
        print(str(data))
        self.server.exec_command(data)
        
class MyServer(socketserver.TCPServer):
    
    def __init__(self, ip_port, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, ip_port, RequestHandlerClass)
        self.commands = {}
        
    def add_dde_client(self, dde_client):
        self.dde_client = dde_client
        
    def add_commands(self,data,command):
        self.commands[data] = command
            
    def exec_command(self,data):
        self.dde_client.exec_command(self.commands[data])

        
class Server(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        
    def run(self):
        self.server = MyServer(("0.0.0.0",9999),TcpHandler)
        self.server.add_commands("stop","key81")
        self.server.add_commands("play","key80")
        self.server.add_dde_client(DdeExecute("xmplay","system"))
        self.server.serve_forever()
    
    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        
"""
Helpers Functions
"""


def main():
    threadServer = Server(1)
    threadServer.start()
    
    while (input("Write exit to quit: ") != "exit"):
        pass
    
    threadServer.stop_server()
    sys.exit()
    

if __name__ == "__main__":
    main()
    
  