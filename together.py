import requests
import sqlite3

data = {
    "attendance" : [3,4,5],
    "inOutMovement": [1,2,3]
}


url = "https://care-shaktimaan.herokuapp.com/postAttendance"
response = requests.post(url, data, timeout=20)
print(response.text)
