import pymongo
import sqlite3
import socket


conn = sqlite3.connect("child.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS details 
            (FNAME TEXT NOT NULL,
            LNAME TEXT NOT NULL,
            C_ID TEXT PRIMARY KEY NOT NULL,
            AGE INT NOT NULL, 
            DOR TEXT NOT NULL,
            GENDER CHAR(1) NOT NULL,
            WITNESS CHAR(25) NOT NULL,
            SET_EXIST BOOLEAN);''')  

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


IPaddress = socket.gethostbyname(socket.gethostname())

if IPaddress != "127.0.0.1":

    client_web = pymongo.MongoClient(
        "mongodb+srv://CCI:root@cluster0.4gzmr.mongodb.net/Jhansi?retryWrites=true&w=majority")
    db = client_web["Jhansi"]
    col = db["children"]

    c = conn.execute('''SELECT C_ID FROM details;''')
    rows = c.fetchall()
    l_local = []
    for row in rows:
        l_local.append(row[0])

    f = open("CCI.txt", "r")
    lines = list(f)
    cci_id = lines[0].rstrip("\n")
    f.close()

    l_web = [] 
    doc = col.find({"cci_id": f"{cci_id}"}, {"_id": 0, "__v":0})
    for x in doc:
        l_web.append(x["C_Id"])
        if(x["C_Id"] not in l_local):
            c.execute('''INSERT INTO details(FNAME, LNAME, C_ID, AGE, DOR, GENDER, WITNESS, SET_EXIST)
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', 
                        (x["fname"], x["lname"], x["C_Id"], x["age"], x["reg_date"], x["gender"], x["witness"],"False"))
        else:
            pass


    #Checking for children who left cci and replacing them from main database to another database
    for x in l_local:
        if x not in l_web:
            c.execute('''SELECT * FROM details WHERE C_ID = '%s' ''' % x)
            row = c.fetchone()
            c.execute('''INSERT INTO leftdetails VALUES (?, ?, ?, ?, ?, ?, ?, ?)''' , (row))
            c.execute('''DELETE * FROM details WHERE C_ID = '%s' ''' % x)




    """For getting CCI Details"""
    col = db["ccis"]
    doc = col.find({"cci_id": f"{cci_id}"}, {"_id": 0, "__v": 0})
    for x in doc:
        fl = open("CCI.txt", "a")
        cci_name = x["cci_name"]+"\n"
        fl.write(cci_name)
        cci_HeadName = x["cci_HeadName"]["fname"]+" "+x["cci_HeadName"]["lname"]+"\n"
        fl.write(cci_HeadName)
        fl.close()

else:
    print("No internet")


conn.commit()
conn.close()
