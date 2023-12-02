from flask import Blueprint, jsonify, request

from models import db, Audiobook

audiobook_bp = Blueprint('audiobook_bp', __name__)

@audiobook_bp.route('/', methods=['GET'])
def get_audiobooks():
    audiobooks = Audiobook.query.all()
    return jsonify([{'id': ab.id, 'title': ab.title, 'description': ab.description} for ab in audiobooks])


@audiobook_bp.route('/', methods=['POST'])
def add_audiobook():
    data = request.json
    new_audiobook = Audiobook(title=data['title'], description=data['description'])
    db.session.add(new_audiobook)
    db.session.commit()
    return jsonify({"message": "Audiobook added", "id": new_audiobook.id}), 201
