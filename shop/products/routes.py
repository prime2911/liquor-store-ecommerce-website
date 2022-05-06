from flask import render_template, request, redirect, session, url_for, flash
import secrets

from shop import db, app, photos
from .models import Brand, Category, Product
from .forms import ProductForm


@app.route("/add-brand", methods=["GET", "POST"])
def add_brand():
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))

    if request.method == "POST":
        brand_name = request.form.get("brand")
        brand = Brand(name=brand_name)

        db.session.add(brand)
        flash(f"Brand \"{brand_name}\" added to the database!", category="success")
        db.session.commit()
        
        return redirect(url_for("add_brand"))

    return render_template("products/add-brand.html", brands="brands", title="Add Brand")

@app.route("/add-category", methods=["GET", "POST"])
def add_category():
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))
        
    if request.method == "POST":
        category_name = request.form.get("category")
        category = Category(name=category_name)

        db.session.add(category)
        flash(f"Category \"{category_name}\" added to the database!", category="success")
        db.session.commit()
        
        return redirect(url_for("add_brand"))

    return render_template("products/add-brand.html", title="Add Category")

@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))
        
    brands = Brand.query.all()
    categories = Category.query.all()
    form = ProductForm(request.form)

    if request.method == "POST":
        name = form.name.data
        origins = form.origins.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.description.data
        brand = request.form.get("brand")
        category = request.form.get("category")
        image = photos.save(request.files.get("image"), name=secrets.token_hex(10) + ".")

        product = Product(
            name=name,
            origins=origins,
            price=price,
            discount=discount,
            stock=stock, desc=desc,
            brand_id=brand,
            category_id=category,
            image=image
        )

        db.session.add(product)
        flash(f"Product \"{name}\" added to the database!", category="success")
        db.session.commit()

        return redirect(url_for("admin"))

    return render_template("products/add-product.html", title="Add Product", form=form, brands=brands, categories=categories)
