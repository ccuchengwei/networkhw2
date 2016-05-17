#!/usr/bin/env python3
import sqlite3
import argparse,socket,time,re,queue

from threading import Thread



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
            
            thread = service(connection,connection.fileno())
            thread.start()
            
    slisten.close()

class service(Thread):
    def __init__(self, con, conid):
        Thread.__init__(self)
        self.con = con
        self.conid = conid
    def run(self):
        condb = sqlite3.connect('user.db')
        # condb.execute('''CREATE TABLE user (ID INTEGER PRIMARY KEY, NAME TEXT, PASSWORD TEXT);''')
        con = self.con
    
        do = con.recv(1024).decode()
        print(do)
        for row in condb.execute("SELECT * FROM user"):
            print (row)
        
        if re.match('new (.*),(.*)',do) :
            domessage = re.match('new (.*),(.*)',do) 
            user = domessage.group(1)
            pw = domessage.group(2)
            sql = "SELECT * from user WHERE NAME = '{}'".format(user)
            result = condb.execute(sql)
            rowcount = len(result.fetchall())
            if rowcount == 0:
                sql = "INSERT INTO user (NAME,PASSWORD)  VALUES ('{}','{}') ".format(user,pw)
                condb.execute(sql)
                for row in condb.execute("SELECT * FROM user"):
                    print (row)
                condb.commit()
                con.send(b'1')
            else :
                con.send(b'0')
        elif re.match('login (.*),(.*)',do):
            domessage = re.match('login (.*),(.*)',do) 
            user = domessage.group(1)
            pw = domessage.group(2)
            sql = "SELECT * from user WHERE NAME = '{}'".format(user)
            for row in condb.execute(sql):
                if row[2] == pw:
                    print("0.0")


            
            
    
if  __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('-host', help="IP or hostname",default='127.0.0.1')
    parser.add_argument('-p' , help='server port default 1060',type = int,default='1060')
    args=parser.parse_args()
    address = (args.host , args.p)
    server(address)
 