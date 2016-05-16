#!/usr/bin/env python3
import sqlite3
import argparse
condb = sqlite3.connect('user.db')
print ("connect database success")
def client():
    print("test1")
def server():
    print("test2")
if  __name__ == '__main__':
    choice={'client':client , 'server':server}
    parser = argparse.ArgumentParser(description='Messenger')
    parser.add_argument('role', choices = choice , help='clint or server')
    args=parser.parse_args()
    fun = choice[args.role]
    fun();
 