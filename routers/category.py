from flask import Blueprint, jsonify, request

from models import db, Category
from routers.auth import token_required

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/', methods=['POST'])
@token_required
def add_category():
    data = request.json
    new_category = Category(category_name=data['category_name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category added", "id": new_category.id}), 201

@category_bp.route('/', methods=['GET'])
@token_required
def get_categories():
    categories = Category.query.all()
    category_list = [{'id': category.id, 'category_name': category.category_name} for category in categories]
    return jsonify(category_list), 200

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@token_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


@category_bp.route('/<int:category_id>', methods=['PUT'])
@token_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    if 'category_name' in data:
        category.category_name = data['category_name']
    else:
        return jsonify({"message": "Missing category_name field"}), 400

    db.session.commit()
    
    return jsonify({"message": "Category updated", "id": category.id}), 200



# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpdmFua2EiLCJpZCI6MSwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzAxNjA5MTE4fQ.LIJIKBAy_3eSJzQvgyZJsYw3x6TDV0wXMM8lX3wC5NQ
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpdmFua2EiLCJpZCI6MSwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzAxNjg5NjA0fQ.vVcpEe8xaEDyy2ISC5pgcc-S84f53yiD_obpHv6FRjI
