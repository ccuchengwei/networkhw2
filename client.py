

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
                        mainroom(clientsock,user)


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
    th1 = threading.Thread(target=sendThreadFunc,args=(clientsock,user))  
    th2 = threading.Thread(target=recvThreadFunc,args=(clientsock,user))
    threads = [th1, th2]  
    for t in threads :  
        t.setDaemon(True)  
        t.start()  
    t.join()  


def sendThreadFunc(clientsock,user):
    time.sleep(0.2)
    check = 0
    while True: 
        doMsg = input("do:")
        clientsock.send(doMsg.encode())
        time.sleep(0.2)
        

def recvThreadFunc(clientsock,user):
    while True:
        recvMsg = clientsock.recv(1024).decode()
        print(recvMsg)



                
    
if  __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('-host', help="IP or hostname",default='127.0.0.1')
    parser.add_argument('-p' , help='server port default 1060',type = int,default='1060')
    args=parser.parse_args()
    address = (args.host , args.p)
    client(address)