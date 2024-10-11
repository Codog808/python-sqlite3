from flask import Flask, request, jsonify, g
from DatabaseCRUD import Database
from TableCRUD import Table
from DataCRUD import Data
import traceback
import sqlite3
class CRUD_API:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = None
        self.table = None
    
    def Database_update(self, database_name):
        try:
            self.db = Database(database_name)
            if self.db.connection == None:
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return 10
    def Database_down(self, database_name):
        pass

    def Table_update(self, database_name, table_name):
        check_database = self.Database_update(database_name)
        if check_database != 10 and check_database:
            self.table = Table(table_name, self.db)
            return True
        return False

    def register_routes(self):
        @self.app.route('/v2/<database_name>', methods=['POST'])
        def Database_create(database_name):
            """ create or check the validity of a database """
            check_database = self.Database_update(database_name)
            if check_database == False:
                self.db.create()
                return jsonify({'message': f'Database: Created: "{database_name}"'}), 200
            elif check_database == True:
                return jsonify({'message': f'Database: Connected: "{database_name}"'}), 201
            else:
                return jsonify({'error': f'Database: Unacceptable: "{database_name}"'}), 401
            return jsonify({'error': f'Database: Should not see this, "Database_create"'}), 999

        @self.app.route('/v2/<database_name>', methods=['GET'])
        def Database_read(database_name):
            check_database = self.Database_update(database_name)
            if  check_database != 10 and check_database:
                tables = [table[0] for table in self.db.read()]
                return jsonify(tables), 200
            else:
                return jsonify({'error': 'Database: Not existing: run POST of "{database_name}" to get more information'}), 500
            return jsonify({'error': f'Database: Should not see this, "Database_read"'}), 999







        @self.app.route('/v2/<database_name>/<table_name>/<schema_type>', methods=['POST'])
        def Table_create(database_name, table_name, schema_type):
            check_table = self.Table_update(database_name, table_name)
            if check_table:
                if schema_type == '':
                    schema_type = 'nibb'
                try:
                    self.table.create(schema_type)
                    return jsonify({'message': f'Table: Connected Schema "{schema_type}": "{database_name}/{table_name}"'}), 200
                except Excpetion as e:
                    print(e)
                    return jsonify({'error': f'Table: Unacceptable Schema "{schema_type}": "{database_name}/{table_name}"'}), 401

            return jsonify({'error': f'Table: Should not see this, "Table_create"'}), 999

        @self.app.route('/v2/<database_name>/<table_name>/<column_name>', methods=['GET'])
        def Table_read(database_name, table_name, column_name):
            check_table = self.Table_update(database_name, table_name)
            if check_table:
                try:
                    column = [id_[0] for id_ in self.table.read(column_name)]
                    return jsonify(column), 200
                except ValueError as ve:
                    print(ve)
                    return jsonify({'error': f'Table: Unacceptable column "{column_name}": "{database_name}/{table_name}"'}), 401
                except Exception as e:
                    print(e)
                    return jsonify({'error': f'Table: unknown error: "{database_name}/{table_name}"'}), 401
            else:
                    return jsonify({'error': f'Table: Unalive name "{table_name}": "{database_name}/{table_name}"'}), 400

            return jsonify({'error': f'Database: Should not see this, "Table_read"'}), 999

        @self.app.route('/v2/<database_name>/<table_name>', methods=['DELETE'])
        def Table_delete(database_name, table_name):
            check_table = self.Table_update(database_name, table_name)
            if check_table:
                self.table.delete()
                return jsonify({'message': f'Table: Deleted "{table_name}": "{database_name}/{table_name}"'}), 200
            else:
                return jsonify({'error': f'Table: Cannot find "{table_name}": "{database_name}/{table_name}"'}), 401
            return jsonify({'error': f'Database: Should not see this, "Table_delete"'}), 999





        @self.app.route('/v2/<database_name>/<table_name>/data', methods=['POST'])
        def Data_create(database_name, table_name):
            check_table = self.Table_update(database_name, table_name)
            if check_table:
                dictionary = request.json
                try:
                    Data(self.table).create(dictionary)
                    return jsonify({'message': f'\t\tData: Inserted item into: "{database_name}/{table_name}"'}), 200
                except sqlite3.IntegrityError:
                    return jsonify({'error': f'\t\tData: Not Inserted, item already there: "{database_name}/{table_name}"'}), 401
                except ValueError:
                    return jsonify({'error': f'\t\tData: Not Inserted, wrong dictionary structure: "{database_name}/{table_name}"'}), 401
            else:
                return jsonify({'error': f'\t\tData: path does not exists: "{database_name}/{table_name}"'}), 401
            return jsonify({'error': f'Database: Should not see this, "Data_create"'}), 999

        @self.app.route('/v2/<database_name>/<table_name>/data/<int:id_>', methods=['GET'])
        def Data_read(database_name, table_name, id_):
            check_table = self.Table_update(database_name, table_name)
            if check_table:
                record = Data(self.table).read(id_)
                if record == None:
                    return jsonify({'error': '\t\tData: id does not exist in table: "{database_name}/{table_name}"'}), 401
                else:
                    return jsonify(record), 200
            else:
                return jsonify({'error': f'\t\tData: path does not exists: "{database_name}/{table_name}"'}), 401
            return jsonify({'error': f'Database: Should not see this, "Data_read"'}), 999

        @self.app.route('/v2/<database_name>/<table_name>/data', methods=['PUT'])
        def Data_update(database_name, table_name):                     
            check_table = self.Table_update(database_name, table_name)
            if check_table:
                updated_dictionary = request.json
                try:
                    id_ = updated_dictionary['id']
                    Data(self.table).update(id_, updated_dictionary)
                    return jsonify({'message': f'\t\tData: Updated item "{id_}": "{database_name}/{table_name}"'}), 200
                except:
                    return jsonify({'error': f'\t\tData: Not updated, wrong dictionary structure: "{database_name}/{table_name}"'}), 401
            else:
                return jsonify({'error': f'\t\tData: path does not exists: "{database_name}/{table_name}"'}), 401
            return jsonify({'error': f'Database: Should not see this, "Data_update"'}), 999

        @self.app.route('/v2/<database_name>/<table_name>/data/<int:id_>', methods=['DELETE'])
        def Data_delete(database_name, table_name, id_):
            check_table = self.Table_update(database_name, table_name)
            if check_table:
                try:
                    Data(self.table).delete(id_)
                    return jsonify({'message': f'\t\tData: Deleted "{id_}": "{database_name}/{table_name}"'}), 200
                except:
                    return jsonify({'error': f'\t\tData: Not deleted, not found "{id_}": "{database_name}/{table_name}"'}), 401
            else:
                return jsonify({'error': f'\t\tData: path does not exists: "{database_name}/{table_name}"'}), 401
            return jsonify({'error': f'Database: Should not see this, "Data_delete"'}), 999

    def run(self, debug=True):
        self.app.run(debug=debug)

api = CRUD_API()
api.register_routes()
app = api.app
if __name__ == '__main__':
    api.run()

