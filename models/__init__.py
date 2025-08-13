from flask_sqlalchemy import SQLAlchemy

# Create a single SQLAlchemy instance that can be imported by both app.py and models
db = SQLAlchemy()

# Import all models to ensure they are registered with SQLAlchemy
# These imports must come after db is defined to avoid circular imports
from .user import User
from .store import Store
from .product import Product
from .order import Order, OrderItem

__all__ = ["db", "User", "Store", "Product", "Order", "OrderItem"]
