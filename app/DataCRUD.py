import json
import traceback
import os
import sqlite3
from DatabaseCRUD import Database
from TableCRUD import Table
import json

# FIX THIS SHIT< REDO

class Data:
    def __init__(self, table: Table):
        self.connection = table.connection
        self.table_name = table.table_name
        self.table = table
        self.schema_type = table.schema_type
        self.schema = table.schema

    def create(self, dictionary):
        #checking is there is an id in dictionary
        working_schema = self.schema.copy()
        if not 'id' in list(dictionary.keys()):
            working_schema.remove('id')
        if sorted(list(dictionary.keys())) != sorted(working_schema):
            raise ValueError(f"Expected '{working_schema}' keys but was given '{list(dictionary.keys())}'")

        columns = ', '.join(working_schema)
        placeholders = ', '.join(['?'] * len(dictionary.keys()))
        values = tuple(dictionary[x] for x in working_schema)
        insert_sql = f"""
        INSERT INTO {self.table_name} ({columns}) 
        VALUES ({placeholders});
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert_sql, values)
            self.connection.commit()
            print(f"\t\tData: Inserted: '{cursor.lastrowid}': '{self.table_name}'")
            return True
        except sqlite3.IntegrityError:
            print(f"\t\tData: Item already in ID: '{dictionary['id']}': '{self.table_name}'")
            return False

    def read(self, id_):
        """ differentiates between a nibb table, where you have to get references. """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (id_,))
        print(f"\t\tData: Grabbing: '{id_}': '{self.table_name}'")
        row = cursor.fetchone()
        if self.schema_type == 'nibb':
            total_records = {}
            if row:
                print(f"\t\t\tData: Grabbing: nibb of '{id_}': '{self.table_name}'")
                column_names = [description[0] for description in cursor.description]
                total_records['nibb'] = (dict(zip(column_names, row)))
                
                print(f'\t\t\tData: Grabbing: documents for nibb of "{id_}": "{self.table_name}"')
                table_names = [name[0] for name in self.table.database.read()]
                document_records = []
                for table_name in table_names:
                    data = self.__class__(Table(table_name, self.table.database))
                    if 'nibb_reference_id' in data.schema:
                        cursor.execute(f"SELECT * FROM {data.table_name} WHERE nibb_reference_id = ?", (id_,))
                        rows = cursor.fetchall()
                        if rows:
                            print(f'\t\t\tData: Grabbing: document for nibb of "{id_}" from "{table_name}"')
                            for row in rows:
                                document_records.append(dict(zip(data.schema, row)))
                total_records['documents'] = document_records
                return total_records
        elif self.schema_type == 'documents':
            if row:
                print(f'\t\t\tData: Grabbed: document of "{id_}": "{self.table_name}"')
                column_names = [description[0] for description in cursor.description]
                record = dict(zip(column_names, row))
                return record
        else:
            if row:
                print(f'\t\t\tData: Grabbed: Unknown "{id_}": "{self.table_name}"')
                column_names = [description[0] for description in cursor.description]
                record = dict(zip(column_names, row))
                return record

        print(f'\t\t\tData: Stopped, unknown id: "{id_}": "{self.table_name}"')
        return None
    def update(self, id_, values):
        """Update a record in the table by ID."""
        if 'id' in values:
            del values['id']  # Ensure we don't update the ID itself
        working_schema = self.schema.copy()
        working_schema.remove('id')
        if list(values.keys()) != working_schema:
            raise ValueError(f"\t\tData: Expected {working_schema} values, got {list(values.keys())}.")

        # Build the update SQL query
        columns = ', '.join([f"{col} = ?" for col in self.schema if col != 'id'])
        update_sql = f"UPDATE {self.table_name} SET {columns} WHERE id = ?"

        # Add the id to the list of values for the WHERE clause
        cursor = self.connection.cursor()
        try:
            cursor.execute(update_sql, (*values.values(), id_))
            self.connection.commit()
            print(f"\t\tData: Record '{id_}' updated: '{self.table_name}'.")
            return True    
        except Exception as e:
            print(f"\t\tData: Unable to update '{id_}': '{self.table_name}'.")
            return False
    def delete(self, id_):
        """Delete a record from the table by ID."""
        cursor = self.connection.cursor()
        delete_sql = f"DELETE FROM {self.table_name} WHERE id = ?"
        try:
            cursor.execute(delete_sql, (id_,))
            self.connection.commit()
            print(f'\t\tData: Deleted "{id_}": "{self.table_name}"')
            return True
        except Exception as e:
            print(f'\t\tData: Failed to delete "{id_}": "{self.table_name}". Error: {e}')
            return False


if __name__ == '__main__':
    db = Database('anus.db')
    db.create()

    t1 = Table('poor', db)
    t1.create('documents')
    documents = {
            'nibb_reference_id': 10,
            'doc_name': 'video_path',
            'doc_path': '/home/fug/fury'
            }
    d1 = Data(t1)
    d1.create(documents)
    id_docs = documents.copy()
    id_docs.update({"id": 10})
    d1.create(id_docs)

    nibb = {
            'name': 'elliot',
            'birthday': '2024-01-01',
            'birthplace': 'brazzas'
            }

    tb = Table('rich', db)
    tb.create()
    d0 = Data(tb)
    d0.create(nibb)
    id_nibb = nibb.copy()
    id_nibb.update({"id": 10})
    d0.create(id_nibb)

    data0 = d0.read(10)
    data1 = d1.read(10)
    
    new_doc = documents.copy()
    new_doc['nibb_reference_id'] = 11
    for doc in data0['documents']:
        d1.update(doc['id'], new_doc)
    d1.update(id_docs['id'], id_docs)

    for id_ in tb.read('id'):
        d0.delete(id_[0])
    for id_ in t1.read('id'):
        d1.delete(id_[0])

    print('from rich:', data0)
    print('from poor:', data1)
