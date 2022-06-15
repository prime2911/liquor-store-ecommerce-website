from flask import render_template, request, redirect, session, url_for, flash, make_response
from flask_login import login_required, current_user, login_user, logout_user
import secrets
import pdfkit

from shop import db, app, photos, bcrypt
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import Customer, Invoice
from shop.products.routes import get_brands, get_categories


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

@app.route("/order", methods=["GET"])
@login_required
def place_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice_number = secrets.token_hex(5)
        try:
            invoice = Invoice(
                invoice_number=invoice_number,
                customer_id=customer_id,
                invoice_details=session["shopping_cart"]
            )

            db.session.add(invoice)
            db.session.commit()
            session.pop("shopping_cart", None)
            flash("Your order has been sent!", category="success")

            return redirect(url_for("get_invoice_details", invoice_number=invoice_number))
            
        except Exception as e:
            print(e)
            flash("There was an error!", category="danger")

            return redirect(url_for("get_cart"))

@app.route("/invoices", methods=["GET"])
@login_required
def get_invoices():
    if current_user.is_authenticated:
        customer_id = current_user.id
        customer = Customer.query.filter_by(id=customer_id).first()
        invoices = Invoice.query.filter_by(customer=customer).all()
    else:
        return redirect(url_for("customer_login"))

    return render_template("customers/invoices.html", title="My Invoices", invoices=invoices, brands=get_brands(), categories=get_categories())

@app.route("/invoices/<invoice_number>", methods=["GET"])
@login_required
def get_invoice_details(invoice_number):
    if current_user.is_authenticated:
        subtotal = 0
        grand_total = 0
        customer_id = current_user.id
        customer = Customer.query.filter_by(id=customer_id).first()
        invoice = Invoice.query.filter_by(invoice_number=invoice_number).filter_by(customer=customer).first()

        for product in invoice.invoice_details.values():
            discount = (product["discount"] / 100) * float(product["price"])
            subtotal += float(product["price"]) * int(product["quantity"])
            subtotal -= discount
            tax = "%.2f" % (0.1 * float(subtotal))
            grand_total = float("%.2f" % (1.1 * subtotal))
    else:
        return redirect(url_for("customer_login"))

    return render_template("customers/invoice_details.html", title="Invoice Details", tax=tax, grand_total=grand_total, customer=customer, invoice=invoice, brands=get_brands(), categories=get_categories())

@app.route("/export-invoice/<invoice_number>", methods=["POST"])
@login_required
def export_invoice(invoice_number):
    if current_user.is_authenticated:
        subtotal = 0
        grand_total = 0
        customer_id = current_user.id
        if request.method == "POST":
            customer = Customer.query.filter_by(id=customer_id).first()
            invoice = Invoice.query.filter_by(invoice_number=invoice_number).filter_by(customer=customer).first()

            for product in invoice.invoice_details.values():
                discount = (product["discount"] / 100) * float(product["price"])
                subtotal += float(product["price"]) * int(product["quantity"])
                subtotal -= discount
                tax = "%.2f" % (0.1 * float(subtotal))
                grand_total = float("%.2f" % (1.1 * subtotal))

            rendered_template = render_template("customers/invoice_pdf.html", title="Invoice Details", tax=tax, grand_total=grand_total, customer=customer, invoice=invoice)
            config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
            pdf = pdfkit.from_string(rendered_template, False, configuration=config)
            response = make_response(pdf)

            response.headers["content-Type"] = "application/pdf"
            response.headers["content-Disposition"] = f"inline; filename={invoice_number}.pdf"

            return response
        
    return redirect(url_for("get_invoice_details"))
