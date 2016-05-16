

import argparse,socket,time,re,queue
from threading import Thread

def client(address):
    clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
        clientsock.connect(address)
    except:
        print ("connect error")
        exit()
    casecontrol = input('welcome server,you can login or new ')  
    for task in switch(casecontrol): 
        if case (login):
            
    
    
            
    

    
    
if  __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('-host', help="IP or hostname",default='127.0.0.1')
    parser.add_argument('-p' , help='server port default 1060',type = int,default='1060')
    args=parser.parse_args()
    address = (args.host , args.p)
    client(address)