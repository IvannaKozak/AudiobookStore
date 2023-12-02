from flask import Blueprint, jsonify, request

from models import db, Audiobook

audiobook_bp = Blueprint('audiobook_bp', __name__)

@audiobook_bp.route('/', methods=['GET'])
def get_audiobooks():
    audiobooks = Audiobook.query.all()
    return jsonify([{'id': ab.id, 'title': ab.title, 'description': ab.description, 'category_id': ab.category_id} for ab in audiobooks])


@audiobook_bp.route('/', methods=['POST'])
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
def delete_audiobook(audiobook_id):
    audiobook = Audiobook.query.get_or_404(audiobook_id)
    db.session.delete(audiobook)
    db.session.commit()
    return jsonify({"message": "Audiobook deleted"}), 200

