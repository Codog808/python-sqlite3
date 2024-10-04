from flask import Flask, request, jsonify, g
from DatabaseCRUD import Database
from TableCRUD import Table
from DataCRUD import Data

def acceptable_database_name(database_name):
    acceptable_databases = open('acceptable_bases.txt').read().split('\n')
    if database_name in acceptable_databases:
        return True
    return False

class CRUD_API:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = None
        self.table = None
        self.database_name = ''
        self.table_name = ''

    def Database_good(self, database_name):
        if acceptable_database_name(database_name) and database_name != '':
            self.db = Database(database_name)
            try:
                # Attempt to connect to the database (assume update() connects to the DB)
                self.db.update()  # If update runs without error, it's already created
                print(f"Connected to database: {database_name}")
            except Exception as e:
                print(f"Database {database_name} does not exist. Creating new database.")
                self.db.create()
            # Update the current database name to the connected one
            self.database_name = database_name
            return True
        return False

        return False 
    def Table_good(self, database_name, table_name):
        if self.Database_good(database_name) and table_name != '':
            if self.db:
                if table_name in [i[0] for i in self.db.read()]:
                    self.table = Table(table_name, self.db)
                    return 2
                else: 
                    self.table = Table(table_name, self.db)
                    return 1
        return False

    def register_routes(self):
        @self.app.route('/v1/<database_name>', methods=['POST'])
        def Database_create(database_name):
            if self.Database_good(database_name):
                return jsonify({'message': f'Database {database_name}: connected'}), 200
            if database_name:
                return jsonify({'error': f'Database {database_name}: name not acceptable'}), 401
            return jsonify({'error': 'Database name empty'}), 400
        
        @self.app.route('/v1/<database_name>', methods=['GET'])
        def Database_read(database_name):
            if self.Database_good(database_name):
                tables = [i[0] for i in self.db.read()]
                return jsonify(tables), 200
            if database_name:
                return jsonify({'error': f'Database {database_name}: name not acceptable'}), 401
            return jsonify({'error': 'Database name empty'}), 400




        @self.app.route('/v1/<database_name>/<table_name>', methods=['POST'])
        def Table_create(database_name, table_name):
            goodness = self.Table_good(database_name, table_name)
            if  goodness == 1:
                auto_increment = request.json.get('auto_increment', False)
                self.table.create(Auto=auto_increment)
                self.table_name = table_name
                return jsonify({'message': f'Table {table_name}: created successfully'}), 201
            elif goodness == 2:
                return jsonify({'message': f'Table {table_name}: connected'}), 200
            return jsonify({'error': 'Table name not acceptable'}), 401

        @self.app.route('/v1/<database_name>/<table_name>/<column>', methods=['GET'])
        def Table_read(database_name, table_name, column):
            if self.Table_good(database_name, table_name):
                rows = [i[0] for i in self.table.read(column)]
                if not rows:
                    return jsonify({'error': 'Table is empty'}), 400
                return jsonify(rows), 200
            return jsonify({'error': 'Table name not acceptable'}), 401

        @self.app.route('/v1/<database_name>/<table_name>', methods=['DELETE'])
        def Table_delete(database_name, table_name):
            goodness = self.Table_good(database_name, table_name)
            if  goodness == 1:
                self.table.delete()
                return jsonify({'message': f'Table {table_name}: deleted successfully'}), 201
            elif goodness == 2:
                return jsonify({'message': f'Table {table_name}: does not exist'}), 200
            return jsonify({'error': 'Table name not acceptable'}), 401



        @self.app.route('/v1/<database_name>/<table_name>/data', methods=['POST'])
        def Data_create(database_name, table_name):
            if self.Table_good(database_name, table_name):
                data = Data(self.table)
                record = request.json
                if data.create(record):
                    return jsonify({'message': f'PICTURED inserted into {table_name} successfully'}), 201
                else:
                    return jsonify({'error': 'PICTURED Already inserted'}), 401
            else:
                return jsonify({'error': 'Wrong database pathing'}), 402

        @self.app.route('/v1/<database_name>/<table_name>/data/<int:id_>', methods=['GET'])
        def Data_read(database_name, table_name, id_):
            if self.Table_good(database_name, table_name):
                data = Data(self.table)
                record = data.read(id_)
                if record:
                    return jsonify(record), 200
                else:
                    return jsonify({'message': 'Record not found'}), 404
            else:
                return jsonify({'error': 'Wrong database pathing'}), 402

        @self.app.route('/v1/<database_name>/<table_name>/data', methods=['PUT'])
        def Data_update(database_name, table_name):                     
            if self.Table_good(database_name, table_name):
                data = Data(self.table)                                                               
                record = request.json  # New data that will replace the existing one
                id_ = record['id']
                if data.update(record):  # Assuming the `update` method updates the record by ID
                    return jsonify({'message': f'PICTURED with ID {id_} updated in {table_name} successfully'}), 201
                else:
                    return jsonify({'error': f'PICTURED with ID {id_} not found'}), 404
            else:                                  
                return jsonify({'error': 'Wrong database pathing'}), 400

        @self.app.route('/v1/<database_name>/<table_name>/data/<int:id_>', methods=['DELETE'])
        def Data_delete(database_name, table_name, id_):
            if self.Table_good(database_name, table_name):
                data = Data(self.table)
                if data.delete(id_):  # Assuming the delete method removes the record by ID
                    return jsonify({'message': f'Record with ID {id_} deleted from {table_name} successfully'}), 200
                else:
                    return jsonify({'error': f'Record with ID {id_} not found'}), 404
            else:
                return jsonify({'error': 'Wrong database pathing'}), 400


    def run(self, debug=True):
        self.app.run(debug=debug)
api = CRUD_API()
api.register_routes()
app = api.app
if __name__ == '__main__':
    api.run()

