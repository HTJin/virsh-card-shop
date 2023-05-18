from flask import Blueprint, request, jsonify, redirect
from ..helpers import token_required
from ..models import db, PullSheet, pullsheet_schema, pullsheets_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/upload', methods=['POST'])
@token_required
def create_pullsheet(our_user):
    product_name = request.json['product_name']
    condition = request.json['condition']
    card_set = request.json['card_set']
    rarity = request.json['rarity']
    quantity = request.json['quantity']
    file_name = request.json['file_name']
    
    pullsheet = PullSheet(product_name, condition, card_set, rarity, quantity, file_name)
    db.session.add(pullsheet)
    db.session.commit()
    
    response = pullsheet_schema.dump(pullsheet)
    return jsonify(response)
  
@api.route('/upload/<csv_name>', methods=['GET'])
@token_required
def get_pullsheet(csv_name):
    if csv_name:
        pullsheets = PullSheet.query.get(csv_name)
        response = pullsheets_schema.dump(pullsheets)
        return jsonify(response)
    else:
        return jsonify({'message': 'The csv file was not found'}), 401
  
@api.route('/upload/<csv_name>/edit', methods=['PUT'])
@token_required
def update_pullsheet(csv_name):
    pullsheet = PullSheet.query.get(csv_name)
    pullsheet.product_name = request.json['product_name']
    pullsheet.condition = request.json['condition']
    pullsheet.card_set = request.json['card_set']
    pullsheet.rarity = request.json['rarity']
    pullsheet.quantity = request.json['quantity']
    pullsheet.file_name = request.json['file_name']
    
    db.session.commit()
    
    response = pullsheet_schema.dump(pullsheet)
    return jsonify(response)
  
@api.route('/upload/<csv_name>/remove', methods=['DELETE'])
@token_required
def delete_pullsheet(csv_name):
    pullsheet = PullSheet.query.get(csv_name)
    
    db.session.delete(pullsheet)
    db.session.commit()
    
    pullsheet_schema.dump(pullsheet)
    return redirect('/profile')