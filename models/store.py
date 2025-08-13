from models import db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # link to User who owns this store

    products = db.relationship("Product", backref="store", lazy=True)
