from flask import render_template, request, redirect, session, url_for, flash, current_app
import secrets, os

from shop import db, app, photos
from .models import Brand, Category, Product
from .forms import ProductForm


items_per_page = 8

@app.route("/")
def home():
    page = request.args.get("page", default=1, type=int)
    # per_page = 3
    products = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=page, per_page=items_per_page)
    # brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    # categories = Category.query.join(Product, (Category.id == Product.category_id)).all()

    return render_template("products/index.html", title="Home Page", products=products, brands=get_brands(), categories=get_categories(), items_per_page=items_per_page)

@app.route("/search-results")
def search_products():
    search_keyword = request.args.get("search_product")
    page = request.args.get("page", default=1, type=int)
    products = Product.query.msearch(search_keyword, fields=["name", "desc"]).filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=page, per_page=items_per_page)

    return render_template("products/search-results.html", title=f"Search Results for '{search_keyword}'", products=products, brands=get_brands(), categories=get_categories(), items_per_page=items_per_page)

@app.route("/brands/<int:id>")
def filter_by_brand(id):
    page = request.args.get("page", default=1, type=int)
    # per_page = 3
    brand = Brand.query.filter_by(id=id).first_or_404()
    products = Product.query.filter(Product.stock > 0).filter_by(brand = brand).order_by(Product.id.desc()).paginate(page=page, per_page=items_per_page)
    # brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    # categories = Category.query.join(Product, (Category.id == Product.category_id)).all()

    return render_template("products/index.html", title="Home Page", products_by_brand=products, brands=get_brands(), categories=get_categories(), brand=brand, items_per_page=items_per_page)

@app.route("/categories/<int:id>")
def filter_by_category(id):
    page = request.args.get("page", default=1, type=int)
    # per_page = 3
    category = Category.query.filter_by(id=id).first_or_404()
    products = Product.query.filter(Product.stock > 0).filter_by(category = category).order_by(Product.id.desc()).paginate(page=page, per_page=items_per_page)
    # brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    # categories = Category.query.join(Product, (Category.id == Product.category_id)).all()

    return render_template("products/index.html", title="Home Page", products_by_category=products, brands=get_brands(), categories=get_categories(), category=category, items_per_page=items_per_page)

def get_brands():
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()

    return brands

def get_categories():
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()

    return categories

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
        
        return redirect(url_for("brands"))

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

@app.route("/delete-brand/<int:id>", methods=["POST"])
def delete_brand(id):
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))
    
    to_delete = Brand.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(to_delete)
        flash("Brand deleted!", category="success")
        db.session.commit()

        return redirect(url_for("brands"))

    flash("Delete unsuccessful!", category="danger")

    return redirect(url_for("admin"))

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
        
        return redirect(url_for("categories"))

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

@app.route("/delete-category/<int:id>", methods=["POST"])
def delete_category(id):
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))
    
    to_delete = Category.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(to_delete)
        flash("Category deleted!", category="success")
        db.session.commit()

        return redirect(url_for("categories"))

    flash("Delete unsuccessful!", category="danger")

    return redirect(url_for("admin"))

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
        try:
            image = photos.save(request.files.get("image"), folder="products", name=f"{secrets.token_hex(10)}.")[9:]
        except:
            image = "product.jpg"

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

        if request.files.get("image"):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/products/" + product.image))
                product.image = photos.save(request.files.get("image"), folder="products", name=f"{secrets.token_hex(10)}.")[9:]
            except:
                product.image = photos.save(request.files.get("image"), folder="products", name=f"{secrets.token_hex(10)}.")[9:]

        db.session.commit()
        flash("Product updated!", category="success")

        return redirect(url_for("admin"))

    form.name.data = product.name
    form.origins.data = product.origins
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.desc
    form.image.data = product.image

    return render_template("products/update-product.html", title="Update Product", form=form, brands=brands, categories=categories, product=product)

@app.route("/delete-product/<int:id>", methods=["POST"])
def delete_product(id):
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))

    product = Product.query.get_or_404(id)

    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/products" + product.image))
        except Exception as e:
            print(e)

        db.session.delete(product)
        db.session.commit()
        flash("Product deleted!", category="success")

        return redirect(url_for("admin"))

    flash("Delete unsuccessful!", category="danger")

    return redirect(url_for("admin"))

@app.route("/product/<int:id>")
def product_details(id):
    product = Product.query.get_or_404(id)
    # brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    # categories = Category.query.join(Product, (Category.id == Product.category_id)).all()

    return render_template("products/product-details.html", title="Product Details", product=product, brands=get_brands(), categories=get_categories())
