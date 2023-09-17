import sqlite3



conn=sqlite3.connect('userdb.db')

c=conn.cursor()

#c.execute('''CREATE TABLE userdata(sno INTEGER,rno INTEGER PRIMARY KEY NOT NULL,name varchar(30) NOT NULL,sex VARCHAR(7),age INTEGER ,year varchar(10),branch varchar(40),DOB DATE ,DOJ DATE,email varchar(30) NOT NULL,username varchar(30) NOT NULL,password varchar(30) NOT NULL )''')

#c.execute('''CREATE TABLE menu_item(id INTEGER PRIMARY KEY ASC,name varchar(250) NOT NULL,price varchar(250),course varchar(250),description varchar(250) NOT NULL,restaurant_id INTEGER NOT NULL,FOREIGN KEY(restaurant_id) REFERENCES restaurant(id))''')

#c.execute('''ALTER TABLE userdata ADD COLUMN prflpic varchar(250)''')

#c.execute('''UPDATE userdata SET prflpic="images/defaultuser.png" WHERE sex="male"''')

#c.execute('''ALTER TABLE userdata ADD COLUMN aboutu varchar(250)''')

#c.execute('''UPDATE userdata SET aboutu="  " WHERE sex="male"''')

conn.commit()
conn.close()

conn=sqlite3.connect('friendsdb.db')

#c=conn1.cursor()

#c.execute('''CREATE TABLE friendsdb(sno INTEGER PRIMARY KEY ,frsend INTEGER NOT NULL ,frget INTEGER NOT NULL,sendd varchar(20),acceptd varchar(20),accept INTEGER )''')


conn.commit()
conn.close()


conn=sqlite3.connect('messagesdb.db')

c=conn.cursor()

c.execute('''CREATE TABLE messagesdb(sno INTEGER PRIMARY KEY ,mid varchar(50),msend INTEGER NOT NULL ,mget INTEGER NOT NULL,sendm varchar(250),sendd varchar(30),seend varchar(30),getv INTEGER )''')


conn.commit()
conn.close()
