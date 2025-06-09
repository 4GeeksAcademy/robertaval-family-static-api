"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        if not members:
            return jsonify({'error': 'member not found or info missing'}), 400
        return jsonify(members), 200
    except Exception as e:
        return jsonify({'error': 'server error', 'message': str(e)}), 500

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        if not member_id:
            return jsonify({'error': 'member not found or info missing'}), 400
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({'error': 'member not found or info missing'}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({'error': 'server error', 'message': str(e)}), 500

@app.route('/members', methods=['POST'])
def add_member():
    try:
        request_body = request.get_json()
        if not request_body:
            return jsonify({'error': 'member not found or info missing'}), 400

        required_fields = ['first_name', 'age', 'lucky_numbers']
        for field in required_fields:
            if field not in request_body or request_body[field] == "":
                return jsonify({'error': 'member not found or info missing'}), 400

        if not isinstance(request_body['age'], int) or request_body['age'] <= 0:
            return jsonify({'error': 'age must be a positive integer'}), 400

        new_member = jackson_family.add_member(request_body)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({'error': 'server error', 'message': str(e)}), 500

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        if not member_id:
            return jsonify({'error': 'member not found or info missing'}), 400

        success = jackson_family.delete_member(member_id)
        if success:
            return jsonify({'done': True}), 200
        else:
            return jsonify({'error': 'member not found or info missing'}), 404
    except Exception as e:
        return jsonify({'error': 'server error', 'message': str(e)}), 500



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)