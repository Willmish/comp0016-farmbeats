'''
# ---- TO BE DONE USING MYSQL ---
import mysql.connector


db = mysql.connector.connect(
        host="localhost"
        #user="root",
        #password="kapsko2000"
        )
print(db)
'''
import sqlite3


class DatabaseManager():
    def __init__(self, database_path: str = "test.db"):
        self._database_path: str = database_path
        self._connection = None
        self._cursor = None

    def connect(self):
        self._connection = sqlite3.connect(self._database_path)
        self._cursor = self._connection.cursor()

    def __repr__(self) -> str:
        res = ''
        for row in self._cursor.execute("SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%';"):
            res += str(row) + '\n'
        return res

if __name__ == "__main__":
    db = DatabaseManager()
    db.connect()
    db._cursor.execute("
    print(db)
