"""
@Author: Daddiego Lucas

"""
import sys,os
from server import Server

print("XMPlay Remote Control Server")
print("")
ip = input("Write the listening address(0.0.0.0 by default): ")
if (ip == ""):
    ip = "0.0.0.0"
    
port = input("Write the listening port(9999 by default): ")
if (port == ""):
    port = "9999"
    
port = int(port)

threadServer = Server(1,(ip,port))
threadServer.daemon = True
threadServer.start()
print("Server Started!")
while (input("Write exit to quit: ") != "exit"):
    os.system("cls")
    pass

threadServer.stop_server()
sys.exit()