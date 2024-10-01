import sqlite3
import os
from DatabaseCRUD import Database


class Table:
    def __init__(self, table_name, database: Database):
        self.connection = database.connection
        self.table_name = table_name
        self.PICTURED_SCHEMA = """(id INTEGER PRIMARY KEY, photographs TEXT, citizenships TEXT, traits TEXT, uniques TEXT, residences TEXT, entourages TEXT, date_of_birth TEXT)"""
        self.PICTURED_SCHEMA_AUTO = """(id INTEGER PRIMARY KEY AUTOINCREMENT, photographs TEXT, citizenships TEXT, traits TEXT, uniques TEXT, residences TEXT, entourages TEXT, date_of_birth TEXT)"""
    def create(self, Auto=False):
        cursor = self.connection.cursor()
        SCHEMA = self.PICTURED_SCHEMA
        if Auto:
            SCHEMA = self.PICTURED_SCHEMA_AUTO
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} {SCHEMA}"
        cursor.execute(create_table_sql)
        self.update()
        print(self.table_name, 'created!')
        return True
    def read(self, column_name):
        cursor = self.connection.cursor()
        #query = f"SELECT {column_name} FROM {self.table_name}"
        pquery = f"SELECT {column_name} FROM {self.table_name}"
        print(self.table_name, 'returning', column_name, 'values@')
        cursor.execute(pquery)
        return cursor.fetchall()
    def update(self):
        self.connection.commit()
        print(self.table_name, 'updated#')
        return True
    def delete(self):
        cursor = self.connection.cursor()
        query_delete = f"DROP TABLE IF EXISTS {self.table_name}"
        cursor.execute(query_delete)
        self.update()
        print(self.table_name, 'dropped&')
        return True

if __name__ == '__main__':
    db = Database('example.db')
    db.update()
    table = Table('gayshit', db)
    table.create()
    ids = table.read('id')
    uniques = table.read('uniques')
    print(ids)
    print(uniques)
    table.delete()
    table.create()
