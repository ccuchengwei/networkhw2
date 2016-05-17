#!/usr/bin/env python3
import sqlite3
import argparse,socket,time,re,queue

from threading import Thread

condb = sqlite3.connect('user.db')
print ("connect database success")
conlist = list()
def server(address):
    
    slisten = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    slisten.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        slisten.bind(address)    
    except Exception as e:
        print('port {} in use...'.format(args.sp))
        slisten.close()
        input('press any key to quit...')
        exit()
    slisten.listen(64)
    print('Listening at {}'.format(slisten.getsockname()))
    while True:
        connection, addr = slisten.accept()
        print('Accept a new connection', connection.getsockname(), connection.fileno())
        buf = connection.recv(1024).decode()
        if buf == '1' :
            print(0.0)
            thread = service(connection,connection.fileno())
            thread.start()
            
    slisten.close()

class service(Thread):
    def __init__(self, con, conid):
        Thread.__init__(self)
        self.con = con
        self.conid = conid
    def run(self):
        con = self.con
        do = con.recv(1024)
        print(do.decode)
        if re.match('login {.*},{.*}',do.decode()):
            print('123')
        else:
            print('321')
    
    
if  __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('-host', help="IP or hostname",default='0.0.0.0')
    parser.add_argument('-p' , help='server port default 1060',type = int,default='1060')
    args=parser.parse_args()
    address = (args.host , args.p)
    server(address)
 