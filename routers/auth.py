from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import Bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__)
bcrypt = Bcrypt()


# Your SECRET_KEY and ALGORITHM
SECRET_KEY = "1bc991a9acbaf16a0183effe123615d85e3d7b1c17d1541pf8e869df41654a39"
ALGORITHM = "HS256"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check if the Authorization header is present and formatted correctly
        if 'Authorization' in request.headers:
            try:
                auth_header = request.headers['Authorization']
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Bearer token malformed.'}), 401

        # If no token is present, return an error
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # If a token is present, verify it and proceed
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Here you could add additional verification or user loading if needed
        except JWTError as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        # If everything is fine, call the actual route function
        return f(*args, **kwargs)

    return decorated



@auth_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        username=data['username'],
        email=data['email'],
        hashed_password=hashed_password,
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User was successfully created"}), 201


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@auth_bp.route('/token', methods=['POST'])
def login_for_access_token():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.hashed_password, password):
        access_token = create_access_token(user.username, user.id, user.role, timedelta(minutes=60))
        return jsonify({"access_token": access_token, "token_type": "bearer"})
    else:
        return jsonify({"message": "Invalid username or password"}), 401
    


# @auth_bp.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']

#     user = User.query.filter_by(username=username).first()
#     if user and bcrypt.check_password_hash(user.hashed_password, password):
#         # Generate a token here if needed
#         return jsonify({"message": "Login successful"}), 200
#     else:
#         return jsonify({"message": "Invalid username or password"}), 401
    

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = User.query.filter_by(username=data['username']).first()

#     if user and bcrypt.check_password_hash(user.hashed_password, data['password']):
#         return jsonify({"message": "Login successful"}), 200
#     else:
#         return jsonify({"message": "Invalid username or password"}), 401
