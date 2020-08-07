import sys
import bcrypt
import sqlite3
import requests
import json
import socket

conn = sqlite3.connect('child.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users(
    EMAIL TEXT NOT NULL,
    PWD TEXT NOT NULL, 
    TOKEN TEXT
);''')

c.execute('''CREATE TABLE IF NOT EXISTS details 
            (FNAME TEXT NOT NULL,
            LNAME TEXT NOT NULL,
            C_ID TEXT PRIMARY KEY NOT NULL,
            AGE INT NOT NULL, 
            DOR TEXT NOT NULL,
            GENDER TEXT NOT NULL,
            SET_EXIST BOOLEAN "False");''')

c.execute('''CREATE TABLE IF NOT EXISTS attendance
            (DATE TEXT NOT NULL,
            C_ID TEXT NOT NULL,
            ATTEND BOOLEAN DEFAULT "False" NOT NULL ,
            ROA TEXT,
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


email="mridul@mail.com"
password= "mridul12"

data = {
    "email" : "mridul@mail.com",
    "password" : "mridul12"
}


c.execute('''Select PWD FROM users WHERE EMAIL = ?''', (email, ))
hashed = c.fetchone()
if hashed is None:
    IPaddress = socket.gethostbyname(socket.gethostname())
    if IPaddress != "127.0.0.1":
        url = "https://care-shaktimaan.herokuapp.com/desktopLogin"
        response = requests.post(url, data, timeout=20)
        if(response.status_code == 200):
            print("Login Successful")
            salt = bcrypt.gensalt()
            pswdencoded = password.encode('utf-8')
            hashed = bcrypt.hashpw(pswdencoded, salt)
            c.execute('''INSERT INTO users (EMAIL, PWD) VALUES(?, ?)''', (email, hashed.decode()))
            x = json.loads(response.text)
            token = x[0]
            c.execute('''UPDATE users SET TOKEN = ? WHERE EMAIL = ?''', (token, email))
            childobjs = x[1]

            for obj in childobjs:
                c.execute('''INSERT INTO details (FNAME, LNAME, C_ID, AGE, DOR, GENDER ) VALUES (?, ?, ?, ?, ?, ?)''', (
                    obj["firstName"], obj["lastName"], obj["child_id"], obj["age"], obj["registrationDate"], obj["gender"]))
        else:
            print(response.status_code)
    else:
        print("No internet")


else:
    IPaddress = socket.gethostbyname(socket.gethostname())
    if IPaddress != "127.0.0.1":
        url = "https://care-shaktimaan.herokuapp.com/desktopLogin"
        response = requests.post(url, data, timeout=20)
        if(response.status_code == 200):
            print("Login Successful")
            x = json.loads(response.text)
            token = x[0]
            c.execute('''UPDATE users SET TOKEN = ? WHERE EMAIL = ?''',
                      (token, email))
            childobjs = x[1]

            #C_IDS in local database
            c = conn.execute('''SELECT C_ID FROM details;''')
            rows = c.fetchall()
            l_local = []
            for row in rows:
                l_local.append(row[0])
            l_web = []
            for obj in childobjs:
                l_web.append(obj["child_id"])
                if(obj["child_id"] not in l_local):
                    c.execute('''INSERT INTO details (FNAME, LNAME, C_ID, AGE, DOR, GENDER ) VALUES (?, ?, ?, ?, ?, ?)''', (
                        obj["firstName"], obj["lastName"], obj["child_id"], obj["age"], obj["registrationDate"], obj["gender"]))
                else:
                    pass

            #Checking for children who left cci and replacing them from main database to another database
            for x in l_local:
                if x not in l_web:
                    c.execute(
                        '''SELECT * FROM details WHERE C_ID = ? ''', (x, ))
                    row = c.fetchone()
                    c.execute(
                        '''INSERT INTO leftdetails VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (row))
                    c.execute(
                        '''DELETE * FROM details WHERE C_ID = ? ''', (x, ))
                        
        else:
            print(response.status_code)

    else:
        hashed = hashed[0].encode('utf-8')
        pswdencoded = password.encode('utf-8')
        if(bcrypt.checkpw(pswdencoded, hashed)):
            print("Login Successful")
        else:
            print("Wrong Credentials")

conn.commit()
conn.close()









































































