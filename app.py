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
    def Table_good(self, database_name, table_name):
        if self.Database_good(database_name) and table_name != '':
            if self.db:
                if table_name in [i[0] for i in self.db.read()]:
                    self.table = Table(table_name, self.db)
                    return True
        return False

    def register_routes(self):
        @self.app.route('/v1/<database_name>', methods=['POST'])
        def Database_create(database_name):
            if self.Database_good(database_name):
                return jsonify({'message': f'Database {database_name}: connected'}), 200
            if database_name:
                return jsonify({'error': f'Database {database_name}: name not acceptable'}), 405
            return jsonify({'error': 'Database name empty'}), 400
        
        @self.app.route('/v1/<database_name>/read', methods=['GET'])
        def Database_read(database_name):
            if self.Database_good(database_name):
                tables = [i[0] for i in self.db.read()]
                return jsonify(tables), 200
            if database_name:
                return jsonify({'error': f'Database {database_name}: name not acceptable'}), 405
            return jsonify({'error': 'Database name empty'}), 400

        @self.app.route('/v1/<database_name>/<table_name>', methods=['POST'])
        def Table_create(database_name, table_name):
            if self.Table_good(database_name, table_name):
                auto_increment = request.json.get('auto_increment', False)
                self.table.create(Auto=auto_increment)
                self.table_name = table_name
                return jsonify({'message': f'Table {table_name}: created successfully'}), 201
            return jsonify({'error': 'Table name not acceptable'}), 400

        @self.app.route('/v1/<database_name>/<table_name>/read/<column>', methods=['GET'])
        def Table_read(database_name, table_name, column):
            if self.Table_good(database_name, table_name):
                rows = [i[0] for i in self.table.read(column)]
                if not rows:
                    return jsonify({'error': 'Table is empty'}), 500
                return jsonify(rows), 200
            return jsonify({'error': 'Table name not acceptable'}), 400

        @self.app.route('/v1/<database_name>/<table_name>/data', methods=['POST'])
        def Data_insert(database_name, table_name):
            if self.Table_good(database_name, table_name):
                data = Data(self.table)
                record = request.json
                if data.create(record):
                    return jsonify({'message': f'PICTURED inserted into {table_name} successfully'}), 201
                else:
                    return jsonify({'error': 'PICTURED Already inserted'}), 400
            else:
                return jsonify({'error': 'Wrong database pathing'}), 400

        @self.app.route('/v1/<database_name>/<table_name>/data/<int:id>', methods=['GET'])
        def Data_read(database_name, table_name, id):
            if self.Table_good(database_name, table_name):
                data = Data(self.table)
                record = data.read(id)
                if record:
                    return jsonify(record), 200
                else:
                    return jsonify({'message': 'Record not found'}), 404
            else:
                return jsonify({'error': 'Wrong database pathing'}), 400

    def run(self, debug=True):
        self.app.run(debug=debug)
api = CRUD_API()
api.register_routes()
app = api.app
if __name__ == '__main__':
    api.run()

