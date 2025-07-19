
from flask import Flask
import helper
import os
from flask import request


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, 'data.json')
PORT = 5001

app = Flask(__name__)

# API-1
@app.route('/')
def home():
    return f'Server is running on http://localhost:{PORT} \n', 200

# API-2
@app.route('/get/data')
def get_data():
    try:
        if not os.path.exists(DATA_FILE):
            return {'error': f'Data file not found at {DATA_FILE}'}, 404
        data = helper.read_json_file(DATA_FILE)
        return data, 200
    except Exception as e:
        return {'error': str(e)}, 500

# API-3
# Example: curl -X POST -H "Content-Type: application/json" -d '{"id":"1", "name":"John", "age":30, "class":"6"}' http://localhost:5001/add/data
@app.route('/add/data', methods=['POST'])
def add_data():
    try:
        # Step-1: Get the existing data
        if not os.path.exists(DATA_FILE):
            existing_data = []
        else:
            existing_data = helper.read_json_file(DATA_FILE)
        
        # Step-2: get new data from the request
        new_data = request.get_json()

        # Step-3: Validate entries in data
        # Ensure required keys are present
        if not new_data or 'id' not in new_data or 'name' not in new_data or 'age' not in new_data or 'class' not in new_data:
            return {'error': f'Invalid data format, all keys should be present: {accepted_keys}'}, 400
        # Ensure no extra keys are present
        accepted_keys = {'id', 'name', 'age', 'class'}
        for key in new_data.keys():
            if key not in accepted_keys:
                return {'error': f'Invalid key: {key}'}, 400

        # Step-4: Check for duplicate ID, duplicate IDs are not allowed
        for item in existing_data:
            if item['id'] == new_data['id']:
                return {'error': 'ID already exists'}, 400

        # Step-5: Add new data to existing data and write to file
        existing_data.append(new_data)
        helper.write_json_file(DATA_FILE, existing_data)
        return new_data, 201
    except Exception as e:
        print(f"Error adding data: {e}")
        return {'error': str(e)}, 500

# API-4
# Example: curl -X POST -H "Content-Type: application/json" -d '{"id":"1", "name":"John Updated"}' http://localhost:5001/update/data
@app.route('/update/data', methods=['POST'])
def update_data():
    # Step-1: Get the existing data
    if not os.path.exists(DATA_FILE):
        return {'error': f'Data file not found at {DATA_FILE}'}, 404
    else:
        existing_data = helper.read_json_file(DATA_FILE)

    # Step-2: Get new data from the request
    new_data = request.get_json()

    # Step-3 Validate Data
    # Ensure no extra keys are present
    accepted_keys = {'id', 'name', 'age', 'class'}
    for key in new_data.keys():
        if key not in accepted_keys:
            return {'error': f'Invalid key: {key}'}, 400

    # Ensure required keys are present
    if not new_data or 'id' not in new_data:
        return {'error': f'Invalid data format, id must be present to update a record'}, 400

    # Step-4: Check if ID exists
    id_exists = False
    for item in existing_data:
        if item['id'] == new_data['id']:
            id_exists = True
            break
    if not id_exists:
        return {'error': f'ID not found in existing data: {new_data["id"]}'}, 404

    # Step-5: Update the existing record
    for item in existing_data:
        if item['id'] == new_data['id']:
            item.update(new_data)
            break
    helper.write_json_file(DATA_FILE, existing_data)

    # get the updated entry
    for item in existing_data:
        if item['id'] == new_data['id']:
            updated_entry = item
            break
    return {'status': 'Data updated successfully', 'updated entry': updated_entry}, 200

# API-5
# create delete API, delete a record by ID
# Example: curl -X POST -H "Content-Type: application/json" -d '{"id":"1"}' http://localhost:5001/delete/data
@app.route('/delete/data', methods=['POST'])
def delete_data():
    # Step-1: Get the existing data
    if not os.path.exists(DATA_FILE):
        return {'error': f'Data file not found at {DATA_FILE}'}, 404
    else:
        existing_data = helper.read_json_file(DATA_FILE)

    # Step-2: Get the ID from the request
    delete_data = request.get_json()
    if not delete_data or 'id' not in delete_data:
        return {'error': f'Invalid data format, id must be present to delete a record'}, 400

    # Step-3: Check if ID exists
    id_exists = False
    for item in existing_data:
        if item['id'] == delete_data['id']:
            id_exists = True
            break
    if not id_exists:
        return {'error': f'ID not found in existing data: {delete_data["id"]}'}, 404

    # Step-4: Delete the record
    updated_data = [item for item in existing_data if item['id'] != delete_data['id']]
    helper.write_json_file(DATA_FILE, updated_data)
    return {'status': 'Data deleted successfully', 'deleted id': delete_data['id']}, 200

# API-6
# Get a record by ID
# Example: curl -X GET http://localhost:5001/get/data/1
@app.route('/get/data/<id>', methods=['GET'])
def get_data_by_id(id):
    # Step-1: Get the existing data
    if not os.path.exists(DATA_FILE):
        return {'error': f'Data file not found at {DATA_FILE}'}, 404
    else:
        existing_data = helper.read_json_file(DATA_FILE)

    # Step-2: Find the record by ID
    for item in existing_data:
        if item['id'] == id:
            return {'data': item}, 200

    # Step-3: If ID not found, return error
    return {'error': f'ID not found in existing data: {id}'}, 404

if __name__ == '__main__':
    print(f'Starting server on http://localhost:{PORT}')
    app.run(debug=True, port=PORT)
