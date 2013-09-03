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
class TcpHandler(socketserver.StreamRequestHandler):      

    #def __init__(self):#,dde_client):
        #self.commands = {"stop":"key81","play":"key80"}
        #self.dde_client = dde_client
     #   pass
		
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("Server Says: {} wrote:".format(self.client_address[0]))
        print(self.data)
        self.prueba()
        #self.exec_command(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())
		
    def prueba(self):
	    print("probando")
        
    #def exec_command(self,data):
        #self.dde_client.exec_command(self.commands[data])
        
        
class Server(threading.Thread):
    def __init__(self, id, tcpHandler): #host="0.0.0.0",port=9999):
        threading.Thread.__init__(self)
        self.id = id
        self.server = tcpHandler
        #self._setup_server(host,port)
        
    #def _setup_server(self,host,port):
        # Create the server.
       # self.server = socketserver.TCPServer((host, port), TcpHandler)

    def run(self):
        self.server.serve_forever()
    
    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        
        
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
        if (self.conversation == None):
            self._setup_dde()
        
        self.conversation.Exec(command)
        
"""
Helpers Functions
"""

def main():

    dde_client = DdeExecute("XMPLAY","SYSTEM")
    tcpHandler = socketserver.TCPServer(("0.0.0.0",9999),TcpHandler)    
    server = Server(1,tcpHandler)
    server.daemon = True
    server.start()
    
    while (input("Write exit to quit: ") != "exit"):
        pass
    
    server.stop_server()
    sys.exit()
    

if __name__ == "__main__":
    main()
    
  