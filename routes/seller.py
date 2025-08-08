from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from models.store import Store
from models.product import Product

seller_bp = Blueprint("seller", __name__, url_prefix="/seller")


@seller_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "seller":
        flash("Access denied: Sellers only.", "danger")
        return redirect(url_for("home"))

    store = Store.query.filter_by(owner_id=current_user.id).first()
    if not store:
        flash("You don't have a store yet. Please create one.", "warning")
        return redirect(url_for("seller.create_store"))

    products = Product.query.filter_by(store_id=store.id).all()
    return render_template("seller/dashboard.html", store=store, products=products)


@seller_bp.route("/create-store", methods=["GET", "POST"])
@login_required
def create_store():
    if current_user.role != "seller":
        flash("Access denied: Sellers only.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()

        if not name:
            flash("Store name is required.", "warning")
            return render_template("seller/create_store.html")

        existing = Store.query.filter_by(owner_id=current_user.id).first()
        if existing:
            flash("You already have a store.", "info")
            return redirect(url_for("seller.dashboard"))

        new_store = Store(name=name, description=description, owner_id=current_user.id)
        db.session.add(new_store)
        db.session.commit()
        flash("Store created!", "success")
        return redirect(url_for("seller.dashboard"))

    return render_template("seller/create_store.html")


@seller_bp.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    if current_user.role != "seller":
        flash("Access denied: Sellers only.", "danger")
        return redirect(url_for("home"))

    store = Store.query.filter_by(owner_id=current_user.id).first()
    if not store:
        flash("Please create a store first.", "warning")
        return redirect(url_for("seller.create_store"))

    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        barcode = request.form.get("barcode").strip()

        if not all([name, price, quantity, barcode]):
            flash("Please fill all required fields.", "warning")
            return render_template("seller/add_product.html")

        if Product.query.filter_by(barcode=barcode).first():
            flash("Barcode already exists. Must be unique.", "danger")
            return render_template("seller/add_product.html")

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            flash("Price must be a number and quantity an integer.", "warning")
            return render_template("seller/add_product.html")

        new_product = Product(
            store_id=store.id,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            barcode=barcode,
        )

        db.session.add(new_product)
        db.session.commit()
        flash("Product added!", "success")
        return redirect(url_for("seller.dashboard"))

    return render_template("seller/add_product.html")


@seller_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if current_user.role != "seller":
        flash("Access denied: Sellers only.", "danger")
        return redirect(url_for("home"))

    product = Product.query.get_or_404(product_id)
    if product.store.owner_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("seller.dashboard"))

    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        barcode = request.form.get("barcode").strip()

        if not all([name, price, quantity, barcode]):
            flash("Please fill all required fields.", "warning")
            return render_template("seller/edit_product.html", product=product)

        if (
            barcode != product.barcode
            and Product.query.filter_by(barcode=barcode).first()
        ):
            flash("Barcode already exists. Must be unique.", "danger")
            return render_template("seller/edit_product.html", product=product)

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            flash("Price must be a number and quantity an integer.", "warning")
            return render_template("seller/edit_product.html", product=product)

        product.name = name
        product.description = description
        product.price = price
        product.quantity = quantity
        product.barcode = barcode

        db.session.commit()
        flash("Product updated!", "success")
        return redirect(url_for("seller.dashboard"))

    return render_template("seller/edit_product.html", product=product)


@seller_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id):
    if current_user.role != "seller":
        flash("Access denied: Sellers only.", "danger")
        return redirect(url_for("home"))

    product = Product.query.get_or_404(product_id)
    if product.store.owner_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("seller.dashboard"))

    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "info")
    return redirect(url_for("seller.dashboard"))
