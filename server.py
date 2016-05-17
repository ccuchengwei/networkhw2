#!/usr/bin/env python3
import sqlite3
import argparse,socket,time,re,queue

from threading import Thread



condict = dict()
def server(address):
    
    slisten = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    
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
        
        print('Accept a new connection', connection.getsockname())
        buf = connection.recv(1024).decode()
        if buf == '1' :
            
            thread = checklogin(connection)
            thread.start()
            
    slisten.close()

class checklogin(Thread):
    def __init__(self, con):
        Thread.__init__(self)
        self.con = con
        
    def run(self):
        condb = sqlite3.connect('user.db')
        # condb.execute('''CREATE TABLE user (ID INTEGER PRIMARY KEY, NAME TEXT, PASSWORD TEXT);''')
        con = self.con
        while True:
            do = con.recv(1024).decode()
            print(do)

            
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
                        print (row)
                        con.send(b'1')
                        condict[user] = con
                        service(user,con,condb)
                    else:
                        con.send(b'0')
            

def service(user,con,condb):

    sql = "SELECT * FROM message WHERE Sendto = '{}'".format(user)
    result = condb.execute(sql)
    for row in result:
        leaveMsg = "Message from {}: {} \n".format(row[1],row[3])
        con.send(leaveMsg.encode())
    condb.execute("DELETE FROM message WHERE Sendto = '{}'".format(user))
    condb.commit()
    while True:
   
        try:
            doMsg = con.recv(1024).decode() 
            print("0.0")
            if doMsg ==  "friend list":
                friendlist(user,con,condb)
            elif re.match('friend add (.*)',doMsg):
                
                addfriend = re.match('friend add (.*)',doMsg)
                condb.execute("INSERT INTO friend_list (NAME,Friend)  VALUES ('{}','{}') ".format(user,addfriend.group(1)))
                condb.commit()
            elif re.match('friend rm (.*)',doMsg):
                rmfriend = re.match('friend rm (.*)',doMsg)
                condb.execute("DELETE FROM friend_list WHERE Friend = '{}'".format(rmfriend.group(1)))
                condb.commit()
                for row in condb.execute("SELECT * FROM friend_list"):
                    print (row)
            elif re.match('send (.*) (.*)',doMsg):
                # condb.execute('''CREATE TABLE message (ID INTEGER PRIMARY KEY, USER TEXT, Sendto TEXT,Msg TEXT);''')
                sendMsg = re.match('send (.*) (.*)',doMsg)
                if condict.get(sendMsg.group(1)):
                    con2 = condict.get(sendMsg.group(1))
                    con2Msg = "\nMessage from {}: {} \ndo:".format(user,sendMsg.group(2))
                    con2.send(con2Msg.encode())
                else :
                    condb.execute("INSERT INTO message (USER,Sendto,Msg)  VALUES ('{}','{}','{}') ".format(user,sendMsg.group(1),sendMsg.group(2)))
                    condb.commit()
            elif re.match('talk (.*)',doMsg):
            
        except (OSError, ConnectionResetError): 
            try:  
                condict.pop(user)
                               
            except:  
                pass
            con.close() 
            return

def friendlist(user,con,condb):
    # condb.execute('''CREATE TABLE friend_list (ID INTEGER PRIMARY KEY, NAME TEXT, Friend TEXT);''')
    sql = "SELECT * FROM friend_list WHERE NAME = '{}'".format(user)
    result = condb.execute(sql)
    
    for row in result:
        if condict.get(row[2]) :
            friendmsg = row[2] + " online"                        
            con.send(friendmsg.encode())
        else :
            friendmsg = row[2] + " offline"
            con.send(friendmsg.encode())
    
    
    
            
            
    
if  __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('-host', help="IP or hostname",default='127.0.0.1')
    parser.add_argument('-p' , help='server port default 1060',type = int,default='1060')
    args=parser.parse_args()
    address = (args.host , args.p)
    server(address)
 