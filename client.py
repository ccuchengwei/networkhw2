

import argparse,socket,time,re
from threading import Thread
from getpass import getpass

def client(address):
    clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
        clientsock.connect(address)
    except:
        print ("connect error")
        exit()
    clientsock.send(b'1')
    casecontral = input('login or new:')  
   
    if casecontral == 'login':
        
        user = input("Name:")
        pw = getpass("password:")
        domessage = 'login {},{}'.format(user,pw)
        print(domessage)
        clientsock.send(domessage.encode())
        check = clientsock.recv(1024).decode
        print(check)
    elif casecontral == 'new':
       
        user = input("Name:")
        pw = getpass("password:")
        pwconfirm = getpass("confirm password:")
        if(pw != pwconfirm):
            continue
        domessage = 'new {},{}'.format(user,pw)
        print(domessage)
        clientsock.send(domessage.encode())
        check = clientsock.recv(1024).decode()
        if check == '0':
            print("Name is used!")

    
    
            
    

    
    
if  __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('-host', help="IP or hostname",default='127.0.0.1')
    parser.add_argument('-p' , help='server port default 1060',type = int,default='1060')
    args=parser.parse_args()
    address = (args.host , args.p)
    client(address)