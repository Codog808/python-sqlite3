import requests
import json
import os


class CRUD_API_V1_CLIENT:
    def __init__(self):
        self.url = 'http://127.0.0.1:5000/v2/!/@/data'

    def Database_create(self, database_name):
        database_url = self.url.split('!')[0] + database_name
        response = requests.post(database_url)
        return response.json()

    def Database_read(self, database_name):
        database_url = self.url.split('!')[0] + database_name 
        response = requests.get(database_url)
        return response.json()

    def Table_create(self, database_name, table_name, schema_type='nibb'):
        table_url = self.url.split('!')[0] + database_name + '/' + table_name + '/' + schema_type
        response = requests.post(table_url)
        return response.json()

    def Table_read(self, database_name, table_name, column_name='id'):
        table_url = self.url.split('!')[0] + database_name + '/' + table_name + '/' + column_name
        response = requests.get(table_url)
        return response.json()
    
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

if __name__ == '__main__':
    client = CRUD_API_V1_CLIENT()
    response = client.Database_create('example.db')
    print(response)
    response = client.Database_create('notacceptable.db')
    print(response)
    response = client.Database_create('cool.db')
    print(response)
    os.system('rm -f cool.db')
    response = client.Database_read('notacceptable.db')
    print(response)
    response = client.Database_read('example.db')
    print(response)
    print('\n\n\nTable Examples')
    response = client.Table_create('example.db', 'nibbler', 'nibb')
    print(response)
    response = client.Table_create('example.db', 'dibbler', 'documents')
    print(response)
    print('connecting to anus.db')
    response = client.Table_read('anus.db', 'scenes', 'id')
    print(response)
    response = client.Table_read('anus.db', 'scenes', 'shit')
    print(response)
    response = client.Table_create('example.db', 'doller', 'documents')
    print(response)
    response = client.Table_read('example.db', 'doller', 'id')
    print(response)
    response = client.Table_delete('example.db', 'doller')
    print(response)
    print('\n\n\nData Examples')
    nibb = {
            'id': 10,
            'name': 'elliot',
            'birthday': '2024-01-01',
            'birthplace': 'brazzas'
            }

    documents = {
            'nibb_reference_id': 10,
            'doc_name': 'video_path',
            'doc_path': '/home/fug/fury'
            }
    # nibb
    response = client.Data_create('example.db', 'nibbler', nibb)
    print(response)
    # docs
    response = client.Data_create('example.db', 'doller', documents)
    print(response)
    response = client.Data_create('example.db', 'dibbler', documents)
    print(response)
    response = client.Data_read('example.db', 'nibbler',nibb['id'])
    print(response)
    new_nibb = nibb.copy()
    new_nibb['name'] ='yolo'
    response = client.Data_update('example.db', 'nibbler', new_nibb)
    print(response)
    response = client.Data_read('example.db', 'nibbler',nibb['id'])
    print(response)
    response = client.Data_delete('example.db', 'nibbler',nibb['id'])
    print(response)
    response = client.Data_read('example.db', 'nibbler',nibb['id'])
    print(response)
