from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from models import db

# Initialize extensions outside of create_app to avoid circular imports
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import models after db is initialized
    with app.app_context():
        from models.user import User
        from models.store import Store
        from models.product import Product
        from models.order import Order, OrderItem

        # Register user_loader
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.seller import seller_bp
    from routes.buyer import buyer_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(buyer_bp)

    @app.route("/")
    def home():
        return render_template("login.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
