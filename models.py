from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(200), nullable=True)

class Audiobook(db.Model):
    __tablename__ = 'audiobook'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(2000), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    # Relationship (optional, if you want to use it in queries)
    category = db.relationship('Category', backref=db.backref('audiobooks', lazy=True))
