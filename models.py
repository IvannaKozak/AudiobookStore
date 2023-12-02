from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    hashed_password = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(45), nullable=True)


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



# class UserLibrary(db.Model):
#     __tablename__ = 'user_library'

#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.String(200), nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
#     audiobook_id = db.Column(db.Integer, db.ForeignKey('audiobook.id'), nullable=True)

#     # Relationship with UserLibrary
#     library_entries = db.relationship('UserLibrary', backref='audiobook', lazy=True)