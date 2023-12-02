from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, Audiobook, Category
from routers.audiobook import audiobook_bp
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:MiUniDB@localhost/AudiobookStoreDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

CORS(app) 


# Routers setup

# app.register_blueprint(auth.router, url_prefix='/auth')
# app.register_blueprint(admin.router, url_prefix='/admin')
# app.register_blueprint(users.router, url_prefix='/users')
app.register_blueprint(audiobook_bp, url_prefix='/audiobook')


# Swagger

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Audiobook Store'
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# temp

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Audiobook Store'})


# Run app

if __name__ == '__main__':
    app.run(debug=True)
