from contextlib import closing
import sqlite3
def close_connection(connection):
    closing(connection)
def close_cursor(cursor):
    closing(cursor)
