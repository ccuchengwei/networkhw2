#!/usr/bin/env python3
import sqlite3
import argparse,socket,time
condb = sqlite3.connect('user.db')
print ("connect database success")
def server(address):
    listen = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        listen.bind(address)    
    except Exception as e:
        print('port {} in use...'.format(args.sp))
        listen.close()
        input('press any key to quit...')
        exit()
    print('Listening at {}'.format(listen.getsockname()))
    listen.close()
    
if  __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('host', help="IP or hostname")
    parser.add_argument('-p' , help='server port default 1060',type = int,default='1060')
    args=parser.parse_args()
    address = (args.host , args.p)
    server(address)
 