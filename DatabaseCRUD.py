import sqlite3
import os

class Database:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = None
        if os.path.exists(self.database_name):
            self.update()
    def create(self):
        if os.path.exists(self.database_name):
            print(self.database_name, 'exists%')
            return False
        print(self.database_name, 'creating$')
        return self.update()
    def read(self):
        """ return all table names, tables return all data ids, and data will return itself? """
        print(self.database_name + ', returning table names^')
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return cursor.fetchall()
    def update(self):
        print(self.database_name, 'connecting#')
        self.connection = sqlite3.connect(self.database_name, check_same_thread=False)
        return True
    def down(self):
        """ it is true that it is down, it is false that it is down """
        if self.connection:
            self.connection.close()
            print(self.database_name, 'closing connection@')
            return False
        print(self.database_name, 'connection closed!')
        return True

if __name__ == '__main__':
    db = Database('example.db')
    tables = db.read()
    print(tables)
    for i in tables:
        print(i[0])

