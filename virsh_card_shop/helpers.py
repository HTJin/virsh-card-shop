from flask import request, jsonify, json
from functools import wraps
from .models import User
import secrets, decimal, csv

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
    
def token_required(flask_function):
    @wraps(flask_function)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        return flask_function(our_user, *args, **kwargs)
    return decorated

def process_pullsheet(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        processed_data = []
        for row in csv_reader:
            transformed_row = {
                'R': row[5],
                'Q': str(int(row[6]) > 1),
                'product_name': row[1],
                'set': row[4],
                'number': row[3],
                'in_stock': str(int(row[6]) > 1),
            }
            processed_data.append(transformed_row)
        processed_data.sort(key=lambda x: (-x['set'], x['R'], x['product_name']))
        with open('transformed_data.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=processed_data[0].keys())
            writer.writeheader()
            for row in processed_data:
                writer.writerow(row)
        return 'transformed_data.csv'