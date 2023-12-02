# from flask import Blueprint, request, jsonify
# from flask_restful import Api, Resource
# from models import db, User
# from flask_bcrypt import Bcrypt
# import jwt
# from datetime import datetime, timedelta

# auth_bp = Blueprint('auth_bp', __name__)
# api = Api(auth_bp)
# bcrypt = Bcrypt()

# SECRET_KEY = "6414c382523609c6639ad95059572736"

# from functools import wraps
# from flask import request, jsonify
# import jwt

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         if 'Authorization' in request.headers:
#             token = request.headers['Authorization'].split(" ")[1]

#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401

#         try:
#             data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             current_user = User.query.filter_by(id=data['id']).first()
#         except:
#             return jsonify({'message': 'Token is invalid!'}), 401

#         return f(current_user, *args, **kwargs)

#     return decorated


# class RegisterUser(Resource):
#     def post(self):
#         data = request.get_json()
#         hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

#         new_user = User(
#             username=data['username'],
#             email=data['email'],
#             hashed_password=hashed_password,
#             role=data['role']
#             # Add other fields as necessary
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({"message": "User registered successfully."}), 201


# class LoginUser(Resource):
#     def post(self):
#         data = request.get_json()
#         user = User.query.filter_by(username=data['username']).first()

#         if user and bcrypt.check_password_hash(user.hashed_password, data['password']):
#             token = jwt.encode({
#                 'sub': user.username,
#                 'id': user.id,
#                 'exp': datetime.utcnow() + timedelta(hours=1)
#             }, SECRET_KEY, algorithm="HS256")
#             return jsonify({'token': token})
        
#         return jsonify({"message": "Invalid username or password"}), 401

# class ListUsers(Resource):
#     def get(self):
#         users = User.query.all()
#         user_list = [{'username': user.username, 'email': user.email} for user in users]
#         return jsonify(user_list)

# class DeleteUser(Resource):
#     def delete(self, username):
#         user = User.query.filter_by(username=username).first()
#         if user:
#             db.session.delete(user)
#             db.session.commit()
#             return jsonify({"message": f"User {username} deleted"})
#         return jsonify({"message": "User not found"}), 404

# api.add_resource(RegisterUser, '/register')
# api.add_resource(LoginUser, '/login')
# api.add_resource(ListUsers, '/users')
# api.add_resource(DeleteUser, '/delete/<string:username>')
