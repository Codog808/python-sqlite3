import sqlite3
import os

class Database:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = None
        acceptable_names = [line.strip() for line in open('acceptable_bases.txt').read().splitlines()]
        if database_name in acceptable_names:
            self.update()
        else:
            raise ValueError(f'Database: unacceptable name: "{database_name}"')
    def create(self):
        if not os.path.exists(self.database_name):
            open(self.database_name, 'w').write('')
            print(f'Database: created: "{self.database_name}"#')
            self.connection = sqlite3.connect(self.database_name, check_same_thread=False)
            return True
        return False
    def read(self):
        """ return all table names, tables return all data ids, and data will return itself? """
        print(f'Database: returned table names: "{self.database_name}"^')
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return cursor.fetchall()
    def update(self):
        if os.path.exists(self.database_name):
            print(f'Database: connected: "{self.database_name}"@')
            self.connection = sqlite3.connect(self.database_name, check_same_thread=False)
            return True
        else:
            print(f'Database: not existing, create using .create() method: "{self.database_name}"!')
            return False
    def down(self):
        """ it is true that it is down, it is false that it is down """
        if self.connection:
            self.connection.close()
            print(f'Database: closed: "{self.database_name}"&')
            return False
        print(f'Database: was closed: "{self.database_name}"*')
        return True

if __name__ == '__main__':
    db = Database('example.db')
    tables = db.read()
    print('\t',tables)
    for i in tables:
        print('\t',i[0])

    print("\t'parsing an unacceptable database name'")
    try:
        db2 = Database('wrong.db')
        db2.create()
    except Exception as e:
        print(e)
