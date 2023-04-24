import sqlite3
import time

def respond(msg):
    return 'Hodor'

def findNextQuestion():
    try:
        sqliteConnection = sqlite3.connect('../instance/sylva.sqlite')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)

        res = cursor.execute('SELECT id, content FROM query WHERE answered=0 ORDER BY created')
        fetch = res.fetchone()

        ans = respond(fetch[1])
        res=cursor.execute("UPDATE query SET answered=1, answer='"+ans+"' WHERE id="+str(fetch[0]))
        sqliteConnection.commit()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def main():
    while(True):
        findNextQuestion()
        time.sleep(10)
        

if __name__ == "__main__":
    main()