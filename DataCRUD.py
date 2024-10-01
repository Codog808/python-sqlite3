import json
import os
import sqlite3
from DatabaseCRUD import Database
from TableCRUD import Table

class Data:
    def __init__(self, table: Table):
        self.connection = table.connection
        self.table_name = table.table_name
        self.table = table
    def create(self, pictured_dictionary):
        ids = [i[0] for i in self.table.read('id')]
        if pictured_dictionary['id'] in ids:
            print('data not inserted', pictured_dictionary['id'], 'item is already in')
            return 0
        data_dict = {k: (json.dumps(v) if isinstance(v, dict) or isinstance(v, list) or isinstance(v, set) else v) for k, v in pictured_dictionary.items()}
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['?'] * len(data_dict))
        values = tuple(data_dict.values())
        insert_sql = f"""
        INSERT INTO {self.table_name} ({columns}) 
        VALUES ({placeholders});
        """
        cursor = self.connection.cursor()
        cursor.execute(insert_sql, values)
        self.connection.commit()
        print("Item", cursor.lastrowid, "inserted correctly")
        return True
    def read(self, id_):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (id_,))
        row = cursor.fetchone()
        if row:
            column_names = [description[0] for description in cursor.description]
            record = dict(zip(column_names, row))
            record = {k: json.loads(v) if k != 'id' and k != 'date_of_birth' else v for k, v in record.items()}
            print('item',id_, 'returned')
            return record
        print('item', id_, 'does not exist')
        return None
    def update(self, pictured_dictionary):
        updated_data = {k: (json.dumps(v) if isinstance(v, dict) or isinstance(v, list) or isinstance(v, set) else v) for k, v in pictured_dictionary.items() if k != 'id'}
        columns = ', '.join([f"{key} = ?" for key in updated_data.keys() if key != 'id'])
        values = list(updated_data.values()) + [pictured_dictionary['id']]# Add the ID at the end for WHERE clause        values = tuple(data_dict.values())
        update_sql = f"UPDATE {self.table_name} SET {columns} WHERE id = ?"
        cursor = self.connection.cursor()
        cursor.execute(update_sql, values)
        self.connection.commit()
        print("Item", cursor.lastrowid, "updated correctly")
        return True
    def delete(self, id_):
        cursor = self.connection.cursor()
        delete_sql = f"DELETE FROM {self.table_name} WHERE id = ?"
        cursor.execute(delete_sql, (id_,))
        self.connection.commit()
        print('item', id_, 'deleted')
        return True

if __name__ == '__main__':
    test_data = {
        'photographs': ['path/to/photo.jpg'],
        'id': 1,
        'citizenships': ['US'],
        'traits': {'height': '6ft', 'eye_color': 'brown'},
        'uniques': {'fingerprint': 'hash123'},
        'residences': {'address': '123 Main St'},
        'entourages': ['Friends, Family'],
        'date_of_birth': '1990-01-01'
    }

    db = Database('example.db')
    table = Table('gayshit', db)
    data = Data(table)
    data.create(test_data)
    t = table.read('id')
    for i in range(t[-1][0], (t[-1][0] + 10)):
        test_data['id'] = i
        data.create(test_data)
    d = data.read(test_data['id'])
    print("first data returned")
    print(d)
    d['uniques']['shit'] = 'brown'
    data.update(d)
    dd = data.read(d['id'])
    print("second data returned, focus on 'uniques'")
    print(dd)

