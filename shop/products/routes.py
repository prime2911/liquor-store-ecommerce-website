from unicodedata import category
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

    return render_template("products/add-brand.html", title="Add Brand")

@app.route("/update-brand/<int:id>", methods=["GET", "POST"])
def update_brand(id):
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))

    to_update = Brand.query.get_or_404(id)
    brand = request.form.get("brand")

    if request.method == "POST":
        to_update.name = brand
        flash("Brand updated!", category="success")
        db.session.commit()

        return redirect(url_for("brands"))

    return render_template("products/update-brand.html", title="Update Brand", to_update=to_update)

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
        
        return redirect(url_for("add_category"))

    return render_template("products/add-category.html", title="Add Category")

@app.route("/update-category/<int:id>", methods=["GET", "POST"])
def update_category(id):
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))

    to_update = Category.query.get_or_404(id)
    category = request.form.get("category")

    if request.method == "POST":
        to_update.name = category
        flash("Category updated!", category="success")
        db.session.commit()

        return redirect(url_for("categories"))

    return render_template("products/update-category.html", title="Update Category", to_update=to_update)

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

@app.route("/update-product/<int:id>", methods=["GET", "POST"])
def update_product(id):
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))

    brands = Brand.query.all()
    categories = Category.query.all()
    product = Product.query.get_or_404(id)

    brand = request.form.get("brand")
    category = request.form.get("category")
    form = ProductForm(request.form)

    if request.method == "POST":
        product.name = form.name.data
        product.origins = form.origins.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.desc = form.description.data
        product.brand_id = brand
        product.category_id = category
        db.session.commit()
        flash("Product Updated!", category="success")

        return redirect("/")

    form.name.data = product.name
    form.origins.data = product.origins
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.desc
    form.image.data = product.image

    return render_template("products/update-product.html", title="Update Product", form=form, brands=brands, categories=categories, product=product)
