import pymysql


def get_conn():
    conn = pymysql.connect(host="localhost", user="root", password="qpuur990415", db="imdb_movie", charset="utf8")
    cursor = conn.cursor()

    if (conn is not None) & (cursor is not None):
        print("Successfully connected")
    else:
        print("Connection failed")

    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        return 1
