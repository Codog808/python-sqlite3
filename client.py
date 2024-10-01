import requests
import json

class CRUD_API_CLIENT:
    def __init__(self):
        self.url = 'http://127.0.0.1:5000/v1/!/@/data'

    def Database_create(self, database_name):
        database_url = self.url.split('!')[0] + database_name
        response = requests.post(database_url)

    def Database_read(self, database_name):
        database_url = self.url.split('!')[0] + database_name + '/read'
        response = requests.get(database_url)
        return response.json()

    def Table_create(self, database_name, table_name, auto_increment=False):
        table_url = self.url.split('!')[0] + database_name + '/' + table_name
        data = {
                'auto_increment':auto_increment
                }
        response = requests.post(table_url, json=data)

    def Table_read(self, database_name, table_name, column_name='id'):
        table_url = self.url.split('!')[0] + database_name + '/' + table_name + '/read/' + column_name
        response = requests.get(table_url)
        if response.status_code == 200:
            return response.json()
        else:
            return False

    def Data_insert(self, database_name, table_name, data_json):
        data_url = self.url.split('!')[0] + database_name + '/' + table_name + '/data'
        response = requests.post(data_url, json=data_json)
        if response.status_code == 400:
            return False
        return True

    def Data_read(self, database_name, table_name, id_):
        data_url = self.url.split('!')[0] + database_name + '/' + table_name + '/data/' + str(id_)
        response=requests.get(data_url)
        return response.json()

def pictured_print(jdata):
    print()
    print('Photographs:\t', jdata['photographs'])
    print('Id:\t\t', jdata['id'])
    print('Citizenships:\t', jdata['citizenships'])
    print('Traits:\t\t', jdata['traits'])
    print('Uniques:\t', jdata['uniques'])
    print('Residences:\t', jdata['residences'])
    print('Entourages:\t', jdata['entourages'])
    print('Date_of_birth:\t', jdata['date_of_birth'])
    print()


data = {
    'photographs': ['path/to/photo.jpg'],
    'id': 100,
    'citizenships': ['US'],
    'traits': {'height': '6ft', 'eye_color': 'brown'},
    'uniques': {'fingerprint': 'hash123'},
    'residences': {'address': '123 Main St'},
    'entourages': ['Friends, Family'],
    'date_of_birth': '1990-01-01'
}

if __name__ == '__main__':
    client = CRUD_API_CLIENT()
    tables = client.Database_read('example.db')
    print(tables)
    for table in tables:
        input(table)
        ids = client.Table_read('example.db', table)
        if table == 'gayshit':
            for x in range(1,10):
                data['id'] = x
                client.Data_insert('example.db', table, data)
        if ids:
            for i in ids:
                data = client.Data_read('example.db', table, i)
                pictured_print(data)
