import dns
import mysql.connector
import pymongo

mysqldb = mysql.connector.connect(
    host="localhost", user="root", password="root", database="child")
mycursor = mysqldb.cursor()
mycursor.execute("SELECT * FROM info")
myresult = mycursor.fetchall()
for x in myresult:
    print(x[0])
print(type(x))

client = pymongo.MongoClient(
    "mongodb://root:root@cci-shard-00-00-wkfkn.mongodb.net:27017,cci-shard-00-01-wkfkn.mongodb.net:27017,cci-shard-00-02-wkfkn.mongodb.net:27017/test?ssl=true&replicaSet=CCI-shard-0&authSource=admin&retryWrites=true&w=majority")
mymongodb = client.child
mymongocol = mymongodb.data
for x in mymongocol.find():
  print(x)

 x in mymongocol.find():
  temp=x["rollno"]
  for y in myresult:
    if(temp==y[0]):
      temp1 = y[1]
      myquery = {"rollno":temp}
      newvalues = {"$set": {"Name": temp1}}
      mymongocol.update_one(myquery, newvalues)
print(type(x))
