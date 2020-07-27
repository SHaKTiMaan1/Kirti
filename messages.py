import pymongo
from datetime import datetime, timedelta
from bson import Int64


def ticks_to_datetime(ticks):
    return datetime(1, 1, 1) + timedelta(microseconds=ticks / 10)


client_web = pymongo.MongoClient(
    "mongodb+srv://CCI:root@cluster0.4gzmr.mongodb.net/Jhansi?retryWrites=true&w=majority")
db = client_web["CARE"]
col = db["messages"]
f = open("CCI.txt", "r")
lines = list(f)
cci_id = lines[0].rstrip("\n")
f.close()
query = {"cci_id": f"{cci_id}"}
doc = col.find_one(query, {"_id": 0, "__v": 0})
print(doc)
obj = {
    "time": datetime.today(),
    "message" : "Hey There time using datetime.today()!!!"
}

result = col.find_one_and_update(query,{'$push':{"Messages": obj}})

# old_time = record['old_time'][0]
# new_time = ticks_to_datetime(old_time)
# print(new_time)
