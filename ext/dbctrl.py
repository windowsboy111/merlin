from contextlib import closing
import sqlite3
def close_connection(connection):
    with closing(connection) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT 1").fetchall()
            return rows
