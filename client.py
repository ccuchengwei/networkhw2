

import argparse,socket,time,re,os
import threading
from getpass import getpass
paused = True
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
        
        clientsock.send(domessage.encode())
        check = clientsock.recv(1024).decode()
        if check == '1':
            
            mainroom(clientsock,user)
            break
        else:
            print("error")
            break
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
    global paused
    while True: 
        doMsg = input("")
        if re.match('sendfile (.*) (.*)',doMsg):
            getfileMsg = re.match('sendfile (.*) (.*)',doMsg)
            if not os.path.isfile(getfileMsg.group(2)):
                print("Error")
                continue
            clientsock.send(doMsg.encode())
            paused = True
            while True:
                if not paused:
                    break
            
            f = open (getfileMsg.group(2),'rb')
            bin = f.read()
            fsize = len(bin)
            clientsock.send(str(fsize).encode())
            time.sleep(0.2)
            clientsock.sendall(bin)
            paused = True
            while True:
                
                if not paused:
                    break
        elif doMsg == "logout":
           clientsock.send(doMsg.encode())
           break
        else:
            clientsock.send(doMsg.encode())
        time.sleep(0.2)
        

def recvThreadFunc(clientsock,user):
    global paused
    while True:
        recvMsg = clientsock.recv(1024).decode()
        if re.match('invitetalk from (.*)',recvMsg):
            inviteMsg = re.match('invitetalk from (.*)',recvMsg)
            clientsock.send(recvMsg.encode())
            print("\n {} invite talk Y or N:".format(inviteMsg.group(1)), end="")
            
        elif recvMsg == 'yestalk' or recvMsg == 'notalk':
            clientsock.send(recvMsg.encode())
            
        elif re.match('endtalkwith (.*)',recvMsg):
            clientsock.send(recvMsg.encode())
            exitMsg = re.match('endtalkwith (.*)',recvMsg)
            print("{} exit room,end talk!".format(exitMsg.group(1)))
            
        elif re.match('(.*) sendfile (.*)',recvMsg):
            recvfileMsg = re.match('(.*) sendfile (.*)',recvMsg)
            clientsock.send(recvMsg.encode())
            print("\n {} send {} to you, Y or N:".format(recvfileMsg.group(1),recvfileMsg.group(2)), end="")
            
        elif recvMsg == 'yesrecv' or recvMsg == 'norecv':
            clientsock.send(recvMsg.encode())
            
        elif recvMsg == "transmissionfile":
            paused = False
            while True:
                recvMsg = clientsock.recv(1024).decode()
                
                if recvMsg == "end of file transmisson":                   
                    print("\n"+recvMsg)
                    break
                else:
                    print(recvMsg, end="")
            paused = False

            
        elif re.match('recvsign (.*)',recvMsg):
            recvsignMsg = re.match('recvsign (.*)',recvMsg)
            filesizeMsg = int(clientsock.recv(1024).decode())
            data = b''
            fcsize = 0
            while fcsize < filesizeMsg:
                packet = clientsock.recv(filesizeMsg-fcsize)
                data += packet
                fcsize = len(data)
                
                if not packet:

                    break
                    
                else:
                    print("\r {}% of {} transmitted...".format(fcsize/filesizeMsg*100,recvsignMsg.group(1)),end="")
                   
            print("\nend of file transmisson")
            f = open(recvsignMsg.group(1),'wb')
            f.write(data)
            f.close()
        elif recvMsg == "logout":
            break
        else:
            print(recvMsg)



                
    
if  __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('-host', help="IP or hostname",default='127.0.0.1')
    parser.add_argument('-p' , help='server port default 1060',type = int,default='1060')
    args=parser.parse_args()
    address = (args.host , args.p)
    client(address)