import sqlite3

conn = sqlite3.connect('child.db')
c = conn.cursor()

# c.execute(
#     '''INSERT INTO attendance values ("02-08-2020","KhuBHO9240","True","False")''')
# c.execute(
#     '''INSERT INTO attendance values ("02-08-2020","MAHBHO201965376","True","False")''')
# c.execute(
#     '''INSERT INTO attendance values ("02-08-2020","MahBHO6235","True","False")''')
# c.execute(
#     '''INSERT INTO attendance values ("02-08-2020","MurBHO9820","False","False")''')

c.execute('''SELECT * FROM attendance''')
for row in c.fetchall():
    print(row)

c.execute("drop table details")
c.execute("drop table attendance")
c.execute("drop table in_and_out")
c.execute("drop table messages")
c.execute("drop table leftdetails")
c.execute("drop table users")

# for row in c.fetchall():
#     print(row)

conn.commit()
