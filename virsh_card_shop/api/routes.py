from flask import Blueprint, request, jsonify
from ..helpers import token_required, process_pullsheet
from ..models import db, PullSheet, pullsheet_schema
import os, time, uuid, pandas

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/upload', methods=['POST'])
@token_required
def upload_csv(our_user):
    if request.files:
        file = request.files['csv']
        file_path = f'virsh_card_shop/static/csv/{file.filename}'
        file.save(file_path)
        transformed_file_path = process_pullsheet(file_path)
        df = pandas.read_csv(transformed_file_path)
        response_data = df.to_dict(orient='records')
        os.remove(transformed_file_path)
        return jsonify(response_data), 200
    else:
        return jsonify({'message': 'Unable to process file'}), 400

@api.route('/upload/<csv_name>', methods=['GET'])
@token_required
def get_pullsheet(csv_name):
    pullsheet = PullSheet.query.filter_by(file_name=csv_name).first()
    if pullsheet:
        response = pullsheet_schema.dump(pullsheet)
        return jsonify(response)
    else:
        return jsonify({'message': 'The csv file was not found'}), 404

@api.route('/upload/<csv_name>/edit', methods=['PUT'])
@token_required
def update_pullsheet(csv_name):
    pullsheet = PullSheet.query.filter_by(file_name=csv_name).first()
    if pullsheet:
        pullsheet.product_name = request.json['Product Name']
        pullsheet.condition = request.json['Condition']
        pullsheet.card_number = request.json['Number']
        pullsheet.card_set = request.json['Set']
        pullsheet.rarity = request.json['R']
        pullsheet.quantity = request.json['Q']

        db.session.commit()

        response = pullsheet_schema.dump(pullsheet)
        return jsonify(response)
    else:
        return jsonify({'message': 'The csv file was not found'}), 404

@api.route('/upload/<csv_name>/remove', methods=['DELETE'])
@token_required
def delete_pullsheet(csv_name):
    pullsheet = PullSheet.query.filter_by(file_name=csv_name).first()
    if pullsheet:
        db.session.delete(pullsheet)
        db.session.commit()

        # remove file from server
        os.remove(f'virsh_card_shop/static/csv/{csv_name}')

        return jsonify({'message': 'The csv file was successfully deleted'}), 200
    else:
        return jsonify({'message': 'The csv file was not found'}), 404