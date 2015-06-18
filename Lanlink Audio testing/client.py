__author__ = "Sandyman"
"""
This module contains the client backend threads used to request for client lists.
"""
import socket

import threading
import clientlist

BUFSIZ = 1024

"""
Handles requesting the server for the available clients which would be built up as buttons in the client home screen.
The methodology applied is one where the server which has a special port(20006) allocated for this purpose is requested
for the info.
"""

def refresh_req():

    host = socket.gethostname()
    mycomp = socket.gethostbyaddr(host)
    server_addr = (clientlist.serverip,20006)
    refresh_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    refresh_sock.connect(server_addr)
    refresh_sock.settimeout(10)
    try:

        receiveddata = refresh_sock.recv(BUFSIZ)
        splitdata = receiveddata.split(",")
        for i in splitdata:
            if i!='':
                if i not in clientlist.lst:
                    clientlist.lst.append(i)
                else:
                    pass
        refresh_sock.close()
    except Exception,e:
        print e.args
        refresh_sock.close()


