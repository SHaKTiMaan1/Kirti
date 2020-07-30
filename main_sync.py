import sqlite3
from datetime import date
import pymongo
import socket
import time

#Getting CCI ID through file
f = open("CCI.txt", "r")
lines = list(f)
cci_id = lines[0].rstrip("\n")
f.close()

#Getting system date
d = date.today().strftime('%d-%m-%Y')

#Connecting to sqlite database
conn = sqlite3.connect('child.db')
c = conn.cursor()

#List which stores data to be synced
l = []

#selecting dates whose attendance has not been synced putting  all the info in a list containing objects
c.execute('''SELECT DISTINCT DATE FROM attendance WHERE SYNCED = 'False' AND DATE != '%s'  ''' % d)
temp_ls = c.fetchall()
for row in temp_ls:
    working_date = row[0]
    ls = []
    c.execute(''' SELECT DATE, C_ID, FNAME, LNAME, ATTEND
                FROM attendance 
                INNER JOIN details ON attendance.C_ID = details.C_ID 
                WHERE SYNCED = 'False' AND DATE != '%s'  ''' % d)
    for row in c.fetchall():
        if row[0] == working_date:
            if row[4] == "True":
                present = True
            else:
                present = False
            child_obj = {
                "C_Id": row[1],
                "firstName": row[2],
                "lastName": row[3],
                "present": present
            }
            ls.append(child_obj)
    #The list ls is completed till here
    attendance_obj = {
        "date": working_date,
        "data": ls
    }
    l.append(attendance_obj)
    #Here l stores all the objects to be pushed into the mongodb atlas



while True:

    IPaddress = socket.gethostbyname(socket.gethostname())
    if IPaddress != "127.0.0.1":
        #Connecting to the mongodb atlas
        client_web = pymongo.MongoClient(
            "mongodb+srv://CCI:root@cluster0.4gzmr.mongodb.net/CARE?retryWrites=true&w=majority")
        db = client_web["CARE"]
        


        #ATTENDANCE SYNC PART

        if(len(l) > 0):
            col = db["ccis"]
            query = {"cci_id": f"{cci_id}"}
            for obj in l:
                result = col.update_one(query, {'$push': {"attendance": obj}})
            if result.modified_count > 0:
                l.clear()
                c.execute(" UPDATE attendance SET SYNCED = 'True' WHERE DATE != '%s' "% d)
            conn.commit()


        #MESSAGE SYNC PART

        #Getting last time when we cci received message from cwc
        f = open("last_time.txt", "r")
        lines = list(f)
        t = lines[0].rstrip("\n")
        t = float(t)  # in milliseconds
        f.close()
        col = db["messages"]
        query = {"cci_id": f"{cci_id}"}
        
        
        #UP to DOWN messages i.e CWC to CCI
        doc = col.find_one(query, {"_id": 0, "__v": 0})
        messages = doc["Messages"]
        for message in reversed(messages):
            if(message["sender"] == "cwc" and t < message["time"]):
                c.execute('''INSERT INTO messages VALUES(
                            ?, ?, ?)''', (message["message"], message["sender"], message["time"]))
                t = message["time"]
        
        #Saving changes to dbs
        conn.commit()
        #Update new time in milliseconds
        f = open("last_time.txt", "w+")
        f.write(str(t))
        f.close()


        #DOWN to UP messages i.e CCI to CWC

        #Getting last time when message was received by CWC from CCI
        for message in reversed(messages):
            if(message["sender"] == "cci"):
                local_latest_time = message["time"]
                break

        c.execute('''SELECT * FROM messages WHERE SENDER = "cci" ''')
        for row in c.fetchall():
            if(row[2] > local_latest_time):
                obj = {
                    "time": row[2],
                    "sender": row[1],
                    "message": row[0]}
                result = col.find_one_and_update(query, {'$push': {"Messages": obj}})

    else:
        time.sleep(20)

