import sqlite3
import os
from DatabaseCRUD import Database


class Table:
    def __init__(self, table_name, database: Database):
        self.connection = database.connection
        self.table_name = table_name
        self.database = database
        self.NIBB_SCHEMA = """(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, birthday TEXT, birthplace TEXT)"""
        self.DOCUMENTS_SCHEMA = """(id INTEGER PRIMARY KEY AUTOINCREMENT, nibb_reference_id INTEGER, doc_name TEXT, doc_path TEXT, FOREIGN KEY(nibb_reference_id) REFERENCES nibb(id))"""
        NIBB_SCHEMA = ['id', 'name', 'birthday', 'birthplace']
        DOC_SCHEMA = ['id', 'nibb_reference_id', 'doc_name', 'doc_path']
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        self.schema = [row[1] for row in cursor.fetchall()]
        self.schema_type = 'random'
        if NIBB_SCHEMA == self.schema:
            self.schema_type = 'nibb'
        elif DOC_SCHEMA == self.schema:
            self.schema_type = 'documents'

    def create(self, schema_type="nibb"):
        cursor = self.connection.cursor()
        if schema_type == "nibb":
            SCHEMA = self.NIBB_SCHEMA
        elif schema_type == "documents":
            SCHEMA = self.DOCUMENTS_SCHEMA
        else:
            raise ValueError(f"\tTable: invalid schema '{schema_type}', schemas are 'nibb' or' 'documents'!")

        create_table_sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} {SCHEMA}"
        cursor.execute(create_table_sql)
        print(f'\tTable: Creating: "{self.table_name}"@')
        self.update()
        return True

    def read(self, column_name):
        cursor = self.connection.cursor()
        try:
            pquery = f"SELECT {column_name} FROM {self.table_name}"
            cursor.execute(pquery)
            print(f'\tTable: Returned column "{column_name}": "{self.table_name}"#')
            return cursor.fetchall()
        except:
            raise ValueError(f'\tTable: Erroneous Column name "{column_name}": "{self.table_name}"')

    def update(self):
        self.connection.commit()
        print(f'\tTable: Updated: "{self.table_name}"$')
        return True

    def delete(self):
        cursor = self.connection.cursor()
        query_delete = f"DROP TABLE IF EXISTS {self.table_name}"
        cursor.execute(query_delete)
        print(f'\tTable: Deleting: "{self.table_name}"%')
        self.update()
        return True


if __name__ == '__main__':
    db = Database('example.db')
    try:
        bib_table = Table('bib', db)
    except:
        pass
    nibb = Table('nibb', db)
    nibb.create(schema_type="nibb")
    print(nibb.read('id'))
    try:
        nibb.read('shit')
    except Exception as e:
        print(e)
    documents_table = Table('documents', db)
    documents_table.create(schema_type="documents")
    

