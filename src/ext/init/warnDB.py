from contextlib import closing
import sqlite3
connection = sqlite3.connect("data/warnings.db")
cursor = connection.cursor()
# cursor.execute("""CREATE TABLE warnings (
#     ID int,
#     Person int,
#     Reason varchar(255),
#     Moderator varchar(255),
#     WarnedDate DATE
# );""")

with closing(connection) as connection:
    with closing(connection.cursor()) as cursor:
        rows = cursor.execute("SELECT 1").fetchall()
        print(rows)
