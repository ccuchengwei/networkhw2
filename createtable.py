import sqlite3
from getpass import getpass
conn = sqlite3.connect('user.db')
print ("Opened database successfully")

# conn.execute('''CREATE TABLE user (ID INTEGER PRIMARY KEY, NAME TEXT, PASSWORD TEXT);''')

# print ("create table successfully")

conn.execute("INSERT INTO user (NAME,PASSWORD)  VALUES ('John','1234567') ")

user = input("Name:")
pw = getpass("password:")
sql = "INSERT INTO user (NAME,PASSWORD)  VALUES ('{}','{}') ".format(user,pw)
conn.execute(sql)

for row in conn.execute("SELECT * FROM user"):
    print (row)
conn.close()