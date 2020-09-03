from contextlib import closing
import sqlite3
connection = sqlite3.connect("/home/windowsboy111/Documents/drive/coding/py/Merlin-py/ext/chat/chats.db")
cursor = connection.cursor()
cursor.execute('DROP TABLE warnings;')

with closing(connection) as connection:
    with closing(connection.cursor()) as cursor:
        rows = cursor.execute("SELECT 1").fetchall()
        print(rows)
