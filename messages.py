from datetime import datetime, timedelta
import sqlite3
import time
import os

os.system("msg_sync.py")

conn = sqlite3.connect('child.db')
c = conn.cursor()

key = 'y'
while( key!= 'q'):
    print("Enter message")
    msg = input()
    c.execute('''INSERT INTO messages VALUES (?, ?, ?)''', (msg, "cci", time.time()*1000))
    c.execute('''SELECT * FROM messages ORDER BY TIME ASC''')
    for row in c.fetchall():
        print(row)
    key = input().strip()
    
conn.commit()
conn.close()
