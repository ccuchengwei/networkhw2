

import argparse,socket,time,re
import threading
from getpass import getpass

def client(address):
    clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
        clientsock.connect(address)
    except:
        print ("connect error")
        exit()
    clientsock.send(b'1')
    
    while True:
        casecontral = input('login or new:')  
        if casecontral == 'login':
            login(clientsock)
        elif casecontral == 'new':
            
                user = input("Name:")
                pw = getpass("password:")
                pwconfirm = getpass("confirm password:")
                if(pw != pwconfirm):
                    print ("error")
                else:
                    domessage = 'new {},{}'.format(user,pw)
                    print(domessage)
                    clientsock.send(domessage.encode())
                    check = clientsock.recv(1024).decode()
                    if check == '0':
                        print("Name is used!")
                    else:
                        break


def login(clientsock):
    while True:
        user = input("Name:")
        pw = getpass("password:")
        domessage = 'login {},{}'.format(user,pw)
        print(domessage)
        clientsock.send(domessage.encode())
        check = clientsock.recv(1024).decode()
        if check == '1':
            mainroom(clientsock,user)
        else:
            print("error")
def mainroom(clientsock,user):
    print("Welcome "+user)
    
    th2 = threading.Thread(target=recvThreadFunc,args=(clientsock,user))
    cond1 = threading.Condition()
    th1 = sendThreadFunc(clientsock,cond1,False)


class sendThreadFunc(threading.Thread):
    def __init__(self,clientsock,cond1,paused1):
        threading.Thread.__init__(self)
        self.con = clientsock
        self.pause_cond = cond1
        self.paused = paused1                
    def run(self)
        while True:   
            while paused1:
                pause_cond1.wait()
            doMsg = input("do:")
            self.con.send(doMsg.encode())


def recvThreadFunc(clientsock,user):
    global paused1
    global pause_cond1
    while True:
        recvMsg = clientsock.recv(1024).decode()
        print(recvMsg)
        paused1 = False
        pause_cond1.notify()
        pause_cond1.release()

                
    
if  __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('-host', help="IP or hostname",default='127.0.0.1')
    parser.add_argument('-p' , help='server port default 1060',type = int,default='1060')
    args=parser.parse_args()
    address = (args.host , args.p)
    client(address)