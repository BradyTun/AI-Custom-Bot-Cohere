from flask import Flask
from flask_login import LoginManager
from models import db, User
from migrate import migrate
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.list import list_bp
from settings import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize database
db.init_app(app)
migrate.init_app(app, db)
 
# Authentication setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(list_bp)

if __name__ == '__main__':
    app.run(debug=True)