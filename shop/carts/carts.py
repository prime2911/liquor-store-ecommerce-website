from math import prod
from flask import redirect, render_template, url_for, flash, request, session

from shop import app
from shop.products.models import Product
from shop.products.routes import get_brands, get_categories


def merge_dicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2

    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

    return False


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    try:
        product_id = request.form.get("product_id")
        quantity = int(request.form.get("quantity"))
        product = Product.query.filter_by(id=product_id).first()

        if product_id and quantity and request.method == "POST":
            cart_item = {product_id:{
                "name": product.name,
                # "origins": product.origins,
                "price": product.price,
                "discount": product.discount,
                "quantity": quantity,
                "stock": product.stock,
                "image": product.image
            }}

            if "shopping_cart" in session:
                print(session["shopping_cart"])

                if product_id in session["shopping_cart"]:
                    # print("This item is already in your shopping cart!")
                    # flash("This item is already in your shopping cart!", category="danger")
                    for key, product in session["shopping_cart"].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            # product["quantity"] += 1
                            if product["quantity"] + 1 <= product["stock"]:
                                product["quantity"] += 1
                            else:
                                flash("Buying amount exceeds stock!", category="danger")

                else:
                    session["shopping_cart"] = merge_dicts(session["shopping_cart"], cart_item)

                    return redirect(request.referrer)
            else:
                session["shopping_cart"] = cart_item

                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route("/carts")
def get_cart():
    if "shopping_cart" not in session or len(session["shopping_cart"]) <= 0:
        return redirect(url_for("home"))

    subtotal = 0
    grand_total = 0
    # print(session["shopping_cart"])
    for product in session["shopping_cart"].values():
        discount = (product["discount"] / 100) * float(product["price"])
        subtotal += float(product["price"]) * int(product["quantity"])
        subtotal -= discount
        tax = "%.2f" % (0.1 * float(subtotal))
        grand_total = float("%.2f" % (1.1 * subtotal))

    return render_template("products/carts.html", title="Your Shopping Cart", tax=tax, grand_total=grand_total, brands=get_brands(), categories=get_categories())

@app.route("/update-cart/<int:id>", methods=["POST"])
def update_cart(id):
    if "shopping_cart" not in session or len(session["shopping_cart"]) <= 0:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        quantity = int(request.form.get("quantity"))
        
        try:
            session.modified = True
            for key, product in session["shopping_cart"].items():
                if int(key) == id:
                    product["quantity"] = quantity
                    flash("Your cart is updated!", category="success")

                    return redirect(url_for("get_cart"))
        except Exception as e:
            print(e)

            return redirect(url_for("get_cart"))

@app.route("/remove-cart/<int:id>")
def remove_cart(id):
    if "shopping_cart" not in session or len(session["shopping_cart"]) <= 0:
        return redirect(url_for("home"))
    
    try:
        session.modified = True

        for key, _ in session["shopping_cart"].items():
            if int(key) == id:
                session["shopping_cart"].pop(key, None)

                return redirect(url_for("get_cart"))
    except Exception as e:
        print(e)

        return redirect(url_for("get_cart"))

@app.route("/clear-cart")
def clear_cart():
    if "shopping_cart" not in session or len(session["shopping_cart"]) <= 0:
        return redirect(url_for("home"))
    
    try:
        session.pop("shopping_cart", None)

        return redirect(url_for("home"))
    except Exception as e:
        print(e)

        return redirect(url_for("get_cart"))
