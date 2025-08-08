from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app import db
from models.store import Store
from models.product import Product
from models.order import Order, OrderItem

buyer_bp = Blueprint("buyer", __name__, url_prefix="/buyer")


@buyer_bp.route("/stores")
def stores():
    stores = Store.query.all()
    return render_template("buyer/stores.html", stores=stores)


@buyer_bp.route("/store/<int:store_id>")
def store_products(store_id):
    store = Store.query.get_or_404(store_id)
    products = Product.query.filter_by(store_id=store.id).all()
    return render_template("buyer/store_products.html", store=store, products=products)


@buyer_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("buyer/product_detail.html", product=product)


@buyer_bp.route("/cart")
@login_required
def cart():
    cart = session.get("cart", {})
    products = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(pid)
        if product:
            subtotal = product.price * qty
            total += subtotal
            products.append({"product": product, "quantity": qty, "subtotal": subtotal})
    return render_template("buyer/cart.html", products=products, total=total)


@buyer_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get("quantity", 1))
    if quantity <= 0:
        flash("Quantity must be at least 1.", "warning")
        return redirect(url_for("buyer.product_detail", product_id=product_id))

    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    session["cart"] = cart
    flash(f"Added {quantity} x {product.name} to cart.", "success")
    return redirect(url_for("buyer.cart"))


@buyer_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
@login_required
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session["cart"] = cart
        flash("Product removed from cart.", "info")
    return redirect(url_for("buyer.cart"))


@buyer_bp.route("/checkout", methods=["POST"])
@login_required
def checkout():
    cart = session.get("cart", {})
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("buyer.cart"))

    # Group products by store to create separate orders if needed
    products = Product.query.filter(
        Product.id.in_([int(pid) for pid in cart.keys()])
    ).all()
    store_orders = {}

    for product in products:
        store_orders.setdefault(product.store_id, []).append(product)

    # For simplicity, create one order per store
    for store_id, prods in store_orders.items():
        total_price = 0
        order = Order(buyer_id=current_user.id, store_id=store_id, total_price=0)
        db.session.add(order)
        db.session.flush()  # Get order.id before commit

        for product in prods:
            qty = cart.get(str(product.id), 0)
            subtotal = product.price * qty
            total_price += subtotal
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=qty,
                unit_price=product.price,
            )
            db.session.add(order_item)

        order.total_price = total_price

    db.session.commit()
    session["cart"] = {}  # Clear cart
    flash("Order placed successfully!", "success")
    return redirect(url_for("buyer.stores"))
