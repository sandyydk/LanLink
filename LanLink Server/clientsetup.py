__author__ = 'Sandyman'
import socket
import shareddata


def clientset():

    host = socket.gethostname()
    setupsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    setupsock.bind((host,20009))
    setupsock.listen(5)
    while True:
        connection,address = setupsock.accept()
        connection.settimeout(5.0)
        clientip = address[0]
        clienttuple = socket.gethostbyaddr(address[0])  # Obtain name of client
        client = clienttuple[0]
        if client in shareddata.lst:
            shareddata.lst.remove(client)
            del shareddata.clientmapdict[client]
        else:
            shareddata.lst.append(client)
            shareddata.clientmapdict[client]= clientip
        connection.close()