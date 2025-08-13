from models import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    barcode = db.Column(
        db.String(50), unique=True, nullable=False
    )  # barcode for each product
    image_url = db.Column(db.String(255))  # optional product image URL
