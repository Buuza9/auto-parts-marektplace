from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app=app)
    login_manager.login_view = "auth.login"
    return app


# #import models
# from models import user, store, product, order

# #Register blueprints
# from routes.auth import auth_bp
# from routes.store import store_bp
# from routes.product import product_bp
# from routes.order import order_bp

# app.register_blueprint(auth_bp)
# app.register_blueprint(store_bp)
# app.register_blueprint(product_bp)
# app.register_blueprint(order_bp)
#
# @app.route('/')
# def home():
# 	return render_template('index.html')

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
