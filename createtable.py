import sqlite3
from getpass import getpass
conn = sqlite3.connect('user.db')
print ("Opened database successfully")

# conn.execute('''CREATE TABLE friend_list (ID INTEGER PRIMARY KEY, NAME TEXT, Friend TEXT);''')

# print ("create table successfully")

# conn.execute("INSERT INTO friend_list (NAME,Friend)  VALUES ('yy','gg') ")

# user = input("Name:")
# pw = getpass("password:")
# sql = "INSERT INTO user (NAME,PASSWORD)  VALUES ('{}','{}') ".format(user,pw)
# conn.execute(sql)
# conn.commit()
for row in conn.execute("SELECT * FROM message"):
    print (row)
conn.close()