from math import prod
from flask import redirect, render_template, url_for, flash, request, session, current_app

from shop import db, app
from shop.products.models  import Product


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
        quantity = request.form.get("quantity")
        product = Product.query.filter_by(id=product_id).first()

        if product_id and quantity and request.method == "POST":
            cart_item = {product_id:{
                "name": product.name,
                # "origins": product.origins,
                "price": product.price,
                "discount": product.discount,
                "quantity": quantity
                # "image": product.image
            }}

            if "shopping_cart" in session:
                print(session["shopping_cart"])

                if product_id in session["shopping_cart"]:
                    print("This item is already in your shopping cart!")
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
    if "shopping_cart" not in session:
        return redirect(request.referrer)

    subtotal = 0
    grand_total = 0
    print(session["shopping_cart"])
    for product in session["shopping_cart"].values():
        discount = (product["discount"] / 100) * float(product["price"])
        subtotal += float(product["price"]) * int(product["quantity"])
        subtotal -= discount
        tax = "%.2f" % (0.1 * float(subtotal))
        grand_total = float("%.2f" % (1.1 * subtotal))

    return render_template("products/carts.html", title="Your Shopping Cart", tax=tax, grand_total=grand_total)
