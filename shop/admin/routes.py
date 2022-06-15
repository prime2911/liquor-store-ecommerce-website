from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Product, Brand, Category


@app.route("/admin")
def admin():
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))

    products = Product.query.all()

    return render_template("admin/index.html", title="Admin Page", products=products)


@app.route("/brands")
def brands():
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))

    brands = Brand.query.order_by(Brand.id.asc()).all()

    return render_template("admin/brands.html", title="Manage Brands", brands=brands)

@app.route("/categories")
def categories():
    if "email" not in session:
        flash("Please login first!", category="danger")

        return redirect(url_for("login"))

    categories = Category.query.order_by(Category.id.asc()).all()

    return render_template("admin/categories.html", title="Manage Categories", categories=categories)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {form.name.data}!", category="success")

        return redirect(url_for("login"))

    return render_template("admin/register.html", form=form, title="Admin Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if "email" not in session:
        if request.method == "POST" and form.validate():
            user = User.query.filter_by(email=form.email.data).first()

            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session["email"] = form.email.data
                flash(f"Welcome {user.name}! You are logged in now!",
                    category="success")

                return redirect(request.args.get("next") or url_for("admin"))
            else:
                flash("Password is incorrect!", category="danger")
    
    else:
        return redirect(url_for("admin"))

    return render_template("admin/login.html", form=form, title="Admin Login")

@app.route("/logout", methods=["GET"])
def logout():
    try:
        session.pop("email", None)

        return redirect(url_for("login"))
    except Exception as e:
        print(e)

        return redirect(url_for("admin"))
