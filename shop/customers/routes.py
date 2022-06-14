from flask import render_template, request, redirect, session, url_for, flash, current_app
import secrets, os

from shop import db, app, photos, search, bcrypt
from .forms import CustomerRegistrationForm
from .models import Customer


@app.route("/customers/register", methods=["GET", "POST"])
def customer_register():
    form = CustomerRegistrationForm(request.form)

    if request.method == "POST":
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        try:
            image = photos.save(request.files.get("profile_pic"), name=f"customers/{secrets.token_hex(10)}.")
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
        # db.session.commit()
        flash(f"Welcome, {form.name.data}!", category="success")

        return redirect(url_for("home"))

    return render_template("customers/register.html", title="User Registration", form=form)