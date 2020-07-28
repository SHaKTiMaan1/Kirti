import sqlite3
import datetime
import pymongo
import time
from datetime import datetime

# t = time()*1000 #milliseconds
# f = open("last_time.txt", "w+")
# f.write(str(t))

conn = sqlite3.connect('child.db')
c = conn.cursor()

client_web = pymongo.MongoClient(
    "mongodb+srv://CCI:root@cluster0.4gzmr.mongodb.net/Jhansi?retryWrites=true&w=majority")
db = client_web["CARE"]
col = db["messages"]

while True:

    f = open("last_time.txt", "r")
    lines = list(f)
    t = lines[0].rstrip("\n")
    t = float(t)  #in milliseconds
    f.close()



    f = open("CCI.txt", "r")
    lines = list(f)
    cci_id = lines[0].rstrip("\n")
    ##temporary
    cci_id = "GhaM2"

    f.close()

    query = {"cci_id": f"{cci_id}"}
    doc = col.find_one(query, {"_id": 0, "__v": 0})
    messages = doc["Messages"]
    for message in reversed(messages):
        if(message["sender"] == "cwc" and t < message["time"]):
            c.execute('''INSERT INTO messages VALUES(
                        ?, ?, ?)''',(message["message"], message["sender"], message["time"]))
            t = message["time"]
        
    #milliseconds
    f = open("last_time.txt", "w+")
    f.write(str(t))
    f.close()


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
    time.sleep(1)