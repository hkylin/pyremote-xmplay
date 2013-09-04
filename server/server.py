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
import win32gui,win32ui, dde
import time

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
            return "Sucessfull!"
        except:
            return "Cannot exec the command"
        

class TcpHandler(socketserver.StreamRequestHandler):      
    
    def handle(self):
        command = self.rfile.readline().strip()
        #data consists of b'data_readed'
        command = command.decode()
        msg1 = self.execute(command)
        time.sleep(1)
        msg2 = self.title()
        msg = msg1 + "|" + msg2
        self.wfile.write(msg.encode())
        
    def execute(self,data):
        return self.server.exec_command(data)
    
    def title(self):
        return self.server.get_song_title()
        
        
class MyTcpServer(socketserver.TCPServer):

    def __init__(self, ip_port, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, ip_port, RequestHandlerClass)
        self.commands = {}
        
    def add_dde_client(self, dde_client):
        self.dde_client = dde_client
        
    def add_title_finder(self,title_finder):
        self.title_finder = title_finder
        
    def add_commands(self,data,command):
        self.commands[data] = command
        
    def get_song_title(self):
        try:
            return self.title_finder.get_current_song_title()
        except:
            return "Could not retrieve the song title"
             
    def exec_command(self,data):
        try:
            if (data.startswith("update")):
                return "Succesful!"
            else:
                return self.dde_client.exec_command(self.commands[data])
        except:
            return "Command not loaded"             

class Server(threading.Thread):
    
    def __init__(self, id,params=("0.0.0.0",9999)):
        threading.Thread.__init__(self)
        self.id = id
        self.server = MyTcpServer(params,TcpHandler)
        
    def conf_server(self):
        self.server.add_title_finder(Titles())
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
        
class Titles():
    
    def __init__(self):
        self.windows = []

    def _win_enum_handler(self,hwnd,ctx):
        if win32gui.IsWindowVisible(hwnd):
            self.windows.append(win32gui.GetWindowText(hwnd))
            
    def _load_titles(self):
        win32gui.EnumWindows(self._win_enum_handler,None)

    def get_current_song_title(self):       
        self._load_titles()
        for item in self.windows:
            if (item.startswith("XMPlay")):
                title = (item[9:])
        return title

if __name__=="__main__":
    import run
    run.main()