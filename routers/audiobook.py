from flask import Blueprint, jsonify, request

from models import db, Audiobook
from routers.auth import token_required

audiobook_bp = Blueprint('audiobook_bp', __name__)

@audiobook_bp.route('/', methods=['GET'])
@token_required
def get_audiobooks():
    audiobooks = Audiobook.query.all()
    return jsonify([{'id': ab.id, 'title': ab.title, 'description': ab.description, 'category_id': ab.category_id} for ab in audiobooks])


@audiobook_bp.route('/', methods=['POST'])
@token_required
def add_audiobook():
    data = request.json
    new_audiobook = Audiobook(
        title=data['title'], 
        description=data['description'],
        category_id=data.get('category_id'))
    db.session.add(new_audiobook)
    db.session.commit()
    return jsonify({"message": "Audiobook added", "id": new_audiobook.id}), 201


@audiobook_bp.route('/<int:audiobook_id>', methods=['DELETE'])
@token_required
def delete_audiobook(audiobook_id):
    audiobook = Audiobook.query.get_or_404(audiobook_id)
    db.session.delete(audiobook)
    db.session.commit()
    return jsonify({"message": "Audiobook deleted"}), 200


@audiobook_bp.route('/<int:audiobook_id>', methods=['PUT'])
@token_required
def update_audiobook(audiobook_id):
    data = request.get_json()
    audiobook = Audiobook.query.get_or_404(audiobook_id)
    
    audiobook.title = data.get('title', audiobook.title)
    audiobook.description = data.get('description', audiobook.description)
    audiobook.category_id = data.get('category_id', audiobook.category_id)
    
    db.session.commit()
    return jsonify({"message": "Audiobook updated", "id": audiobook.id}), 200
