from flask import Blueprint, jsonify, request

from models import db, Category

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/', methods=['POST'])
def add_category():
    data = request.json
    new_category = Category(category_name=data['category_name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category added", "id": new_category.id}), 201

@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_list = [{'id': category.id, 'category_name': category.category_name} for category in categories]
    return jsonify(category_list), 200

@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200
