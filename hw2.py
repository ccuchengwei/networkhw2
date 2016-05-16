#!/usr/bin/env python3
import sqlite3
import argparse,socket,time
condb = sqlite3.connect('user.db')
print ("connect database success")
def client():
    print("test1")
def server(sp):
    listen = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        listen.bind(('', int(sp)))    #we want to send from port 68
    except Exception as e:
        print('port {} in use...'.format(sp))
        listen.close()
        input('press any key to quit...')
        exit()
    print('Listening at {}'.format(listen.getsockname()))
    listen.close()
    
if  __name__ == '__main__':
    choice={'client':client , 'server':server}
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('role', choices = choice , help='clint or server')
    parser.add_argument('-sp' , help='server port default 1060',default='1060')
    parser.add_argument('-cp' , help='clint port default 1060',default='1060')
    args=parser.parse_args()
    fun = choice[args.role]
    fun(args.sp);
 