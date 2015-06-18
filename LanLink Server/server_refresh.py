__author__ = 'SANDYMAN'


#this module is responsible for accepting and processing refresh request from client

import socket
import select
import shareddata

def ref_fun():
    host = socket.gethostname()
    refresh_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
    refresh_sock.bind((host,20006))
    refresh_sock.listen(5)
    inputs = [refresh_sock]
    outputs = []
    while True:
        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s is refresh_sock:
                    try:
                        connection, address = refresh_sock.accept()
                        outputs.append(connection)
                    except Exception,e:
                         print e.args
                else:
                    pass
            for s in writable:
                try:
                    #send list at a time or the items in list one by one
                    sendlst=shareddata.lst
                    for i in sendlst:
                         i = i+","
                    j=""
                    for i in sendlst:
                       j=j+","+i
                    try:
                        s.sendall(j)
                    except Exception,e:
                        print e.args
                except Exception,e:
                    print e.args
                    outputs.remove(s)
                else:
                    outputs.remove(s)
                    s.close()
            for s in exceptional:
                outputs.remove(s)
                if s in inputs:
                    inputs.remove(s)
                s.close()
