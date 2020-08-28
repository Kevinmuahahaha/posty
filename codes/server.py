from mod.modlog import debug
from mod.interaction_routine import interaction_routine
import threading
import sys
import socket
HOST_IP="127.0.0.1"
HOST_PORT=23869
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind((HOST_IP,HOST_PORT))
soc.listen(5)
debug("Server running at %s:%s"%(HOST_IP, HOST_PORT))
debug("Ready for incoming requests.")

while True:
    client_sock, client_addr = soc.accept()
    debug("Connection From: " + str(client_addr[0]) + ":" + str(client_addr[1]))
    thread_interaction = threading.Thread(target=interaction_routine,args=(client_sock,))
    thread_interaction.start()
