import sqlite3
import socket
from login import email, pswd
import json
import requests

conn = sqlite3.connect("child.db")
c = conn.cursor()
  

c.execute('''CREATE TABLE IF NOT EXISTS attendance
            (DATE TEXT NOT NULL,
            C_ID TEXT NOT NULL,
            ATTEND BOOLEAN DEFAULT "False" NOT NULL ,
            SYNCED BOOLEAN DEFAULT "False");''')

c.execute('''CREATE TABLE IF NOT EXISTS messages(
             MSG TEXT,
             SENDER TEXT NOT NULL,
             TIME REAL NOT NULL);''')

c.execute('''CREATE TABLE IF NOT EXISTS leftdetails 
            (FNAME TEXT NOT NULL,
            LNAME TEXT NOT NULL,
            C_ID TEXT PRIMARY KEY NOT NULL,
            AGE INT NOT NULL, 
            DOR TEXT NOT NULL,
            GENDER CHAR(1) NOT NULL,
            WITNESS CHAR(25) NOT NULL,
            SET_EXIST BOOLEAN);''')

c.execute('''CREATE TABLE IF NOT EXISTS in_and_out(
             C_ID TEXT NOT NULL,
             DATE_OUT TEXT,
             TIME_OUT TEXT,
             DATE_IN TEXT,
             TIME_IN TEXT,
             SYNCED BOOLEAN DEFAULT "False");''')


IPaddress = socket.gethostbyname(socket.gethostname())

if IPaddress != "127.0.0.1":

    c = conn.execute('''SELECT C_ID FROM details;''')
    rows = c.fetchall()
    l_local = []
    for row in rows:
        l_local.append(row[0])

    l_web = [] 
    url = "https://care-shaktimaan.herokuapp.com/firstTimeLoginPlain/{}/{}".format(
        email, pswd)
    x = requests.get(url, timeout=20)
    y = json.loads(x.text)
    for obj in y:
        l_web.append(obj["child_id"])
        if(obj["child_id"] not in l_local):
            c.execute('''INSERT INTO details (FNAME, LNAME, C_ID, AGE, DOR, GENDER ) VALUES (?, ?, ?, ?, ?, ?)''', (
                obj["firstName"], obj["lastName"], obj["child_id"], obj["age"], obj["registrationDate"], obj["gender"]))
        else:
            pass


    #Checking for children who left cci and replacing them from main database to another database
    for x in l_local:
        if x not in l_web:
            c.execute('''SELECT * FROM details WHERE C_ID = ? ''', (x, ))
            row = c.fetchone()
            c.execute('''INSERT INTO leftdetails VALUES (?, ?, ?, ?, ?, ?, ?, ?)''' , (row))
            c.execute('''DELETE * FROM details WHERE C_ID = ? ''', (x, ))


else:
    print("No internet")


conn.commit()
conn.close()
