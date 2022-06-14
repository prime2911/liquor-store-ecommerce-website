from flask import render_template, request, redirect, session, url_for, flash, current_app
from flask_login import login_required, current_user, login_user, logout_user
import secrets, os

from shop import db, app, photos, search, bcrypt, login_manager
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import Customer


@app.route("/customers/register", methods=["GET", "POST"])
def customer_register():
    form = CustomerRegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        try:
            image = photos.save(request.files.get("profile_pic"), folder="customers", name=f"{secrets.token_hex(10)}.")
        except:
            image = "profile.jpg"

        customer = Customer(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            dob=form.dob.data,
            civ_id=form.civ_id.data,
            phone_number=form.phone_number.data,
            profile_pic=image
        )

        db.session.add(customer)
        db.session.commit()
        flash(f"Welcome, {form.name.data}!", category="success")

        return redirect(url_for("home"))

    return render_template("customers/register.html", title="User Registration", form=form)

@app.route("/customers/login", methods=["GET", "POST"])
def customer_login():
    form = CustomerLoginForm()

    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer)
            flash(f"You are now logged it, {customer.name}", category="success")
            next = request.args.get("next")

            return redirect(next or url_for("home"))

        flash("Incorrect credentials!", category="danger")

        return redirect(url_for("customer_login"))

    return render_template("customers/login.html", title="User Login", form=form)

@app.route("/customers/logout", methods=["GET"])
def customer_logout():
    logout_user()

    return redirect(url_for("home"))
