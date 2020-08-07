import requests
import sqlite3
import json

conn = sqlite3.connect('child.db')
c = conn.cursor()
c.execute("SELECT TOKEN, EMAIL FROM users")
row = c.fetchone()
token = row[0]
email = row[1]

obj = {
    "date": "6-03-2018",
    "data": [
        {
            "child_Id": "Raj6547",
            "firstName": "something",
            "lastName": "something",
            "present": True,
            "reasonOfAbsence": "something"
        }
    ]
}

obj = {
    "attendance": [{
        "date": "6-03-2018",
        "data": [
            {
                "child_Id": "Raj6547",
                "firstName": "something",
                "lastName": "something",
                "present": True,
                "reasonOfAbsence": "something"
            }
        ]
    }, {
        "date": "13-05-2019",
        "data": [
            {
                "child_Id": "Raju6272786",
                "firstName": "something",
                "lastName": "something",
                "present": True,
                "reasonOfAbsence": "something"
            }
        ]
    }],
    "inOutMovement": [{
        "child_id": "jkjsdfkjd7678",
        "date_out": "20-07-2018",
        "time_out": "20-07-2018",
        "date_in":  "20-07-2018",
        "time_in": "20-07-2018"

    },{
        "child_id": "nnnklhfio697",
        "date_out": "25-07-2018",
        "time_out": "25-07-2018",
        "date_in":  "25-07-2018",
        "time_in": "25-07-2018"
    }]
}

url = "https://care-shaktimaan.herokuapp.com/postAttendance/{}".format(email)

response = requests.post(url, json=obj, headers={"Content-Type": "application/json",
                                                 "Authorization": "Bearer {}".format(token)} ,timeout=20)

print(response.text)
