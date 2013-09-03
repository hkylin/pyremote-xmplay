#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 21:36:42 2013
@Author: Daddiego Lucas
"""

"""
Imports
"""
import socketserver, threading
import win32ui, dde

"""
Classes
"""
class DdeExecute():
    
    def __init__(self,app,topic):
        self.conversation = None
        self.app = app
        self.topic = topic
        self._setup_dde()     
    
    def _setup_dde(self):
        self.serv = dde.CreateServer()
        self.serv.Create("TC")
        try:
            self.conversation = dde.CreateConversation(self.serv)
            self.conversation.ConnectTo(self.app,self.topic)
        except:
            print("Cannot connect to XMPlay")
        
    def exec_command(self,command):
        try:
            self.conversation.Exec(command)
        except:
            print("Cannot exec the command")
        

class TcpHandler(socketserver.StreamRequestHandler):      
    
    def handle(self):
        data = self.rfile.readline().strip()
        #data consists of b'data_readed'
        data = str(data)[2:-1] #in this line, i remove the b''
        self.server.exec_command(data)
        
class MyTcpServer(socketserver.TCPServer):

    def __init__(self, ip_port, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, ip_port, RequestHandlerClass)
        self.commands = {}
        
    def add_dde_client(self, dde_client):
        self.dde_client = dde_client
        
    def add_commands(self,data,command):
        self.commands[data] = command
        
            
    def exec_command(self,data):
        try:
            self.dde_client.exec_command(self.commands[data])
        except:
            print("Command not loaded")

class Server(threading.Thread):
    
    def __init__(self, id,params=("0.0.0.0",9999)):
        threading.Thread.__init__(self)
        self.id = id
        self.server = MyTcpServer(params,TcpHandler)
        
    def conf_server(self):
        self.server.add_dde_client(DdeExecute("xmplay","system"))
        self.server.add_commands("play","key80")
        self.server.add_commands("pause","key80")
        self.server.add_commands("stop","key81")
        self.server.add_commands("next","key128")
        self.server.add_commands("prev","key129")
        
    def run(self):        
        self.conf_server()
        self.server.serve_forever()
    
    def stop_server(self):
        self.server.dde_client.serv.Destroy()
        self.server.shutdown()
        self.server.server_close()