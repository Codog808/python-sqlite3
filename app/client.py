import requests
import json


class CRUD_API_V1_CLIENT:
    def __init__(self):
        self.url = 'http://127.0.0.1:5000/v1/!/@/data'

    def Database_create(self, database_name):
        database_url = self.url.split('!')[0] + database_name
        response = requests.post(database_url)
        return response.json()

    def Database_read(self, database_name):
        database_url = self.url.split('!')[0] + database_name 
        response = requests.get(database_url)
        return response.json()

    def Table_create(self, database_name, table_name, auto_increment=False):
        table_url = self.url.split('!')[0] + database_name + '/' + table_name
        data = {
                'auto_increment':auto_increment
                }
        response = requests.post(table_url, json=data)
        return response.json()

    def Table_read(self, database_name, table_name, column_name='id'):
        table_url = self.url.split('!')[0] + database_name + '/' + table_name + '/' + column_name
        response = requests.get(table_url)
        if response.status_code == 200:
            return response.json()
        else:
            return False
    
    def Table_delete(self, database_name, table_name):
        table_url = self.url.split('!')[0] + database_name + '/' + table_name
        response = requests.delete(table_url)
        return response.json()

    def Data_create(self, database_name, table_name, data_json):
        data_url = self.url.split('!')[0] + database_name + '/' + table_name + '/data'
        response = requests.post(data_url, json=data_json)
        return response.json()

    def Data_read(self, database_name, table_name, id_):
        data_url = self.url.split('!')[0] + database_name + '/' + table_name + '/data/' + str(id_)
        response=requests.get(data_url)
        return response.json()

    def Data_update(self, database_name, table_name, new_data_json):
        data_url = self.url.split('!')[0] + database_name + '/' + table_name + '/data'
        response=requests.put(data_url, json=new_data_json)
        return response.json()

    def Data_delete(self, database_name, table_name, id_):
        data_url = self.url.split('!')[0] + database_name + '/' + table_name + '/data/' + str(id_)
        response=requests.delete(data_url)
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
    client = CRUD_API_V1_CLIENT()
    database_name = 'cool.db'
    client.Database_create(database_name)

    table_name = 'dump'
    out = client.Table_create(database_name, table_name)
    client.Data_create(database_name, table_name, data)
    tables = client.Database_read(database_name)
    for table in tables:
        print(table)
        client.Data_create(database_name, table, data)
        ids = client.Table_read(database_name, table, 'id')

        print('\t', ids)
        for x in range(ids[-1] + 1, ids[-1] + 11):
            data['id'] = x
            client.Data_create(database_name, table, data)
        ids = client.Table_read(database_name, table, 'id')
        client.Data_delete(database_name, table_name, ids[-1])
        datax = data.copy()
        datax['uniques']['fagbutt'] = 'jj'
        client.Data_update(database_name, table_name, datax)
        rex = client.Data_read(database_name, table_name, ids[-2])
        pictured_print(rex)

        print('\t', ids)

        

