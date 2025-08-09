from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()

class Admin(UserMixin):
    id = 1
    username = "admin"
    password = "admin"

@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":
        return Admin()
    return None

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    # ✅ Importar modelos antes de crear tablas
    from .models import User  

    with app.app_context():
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app