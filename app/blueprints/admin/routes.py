
from flask import Blueprint, render_template, request, redirect, url_for

from flask_login import login_user, logout_user, current_user

from app.config import db

from app.models.user import User
from app.models.product import Product
from app.models.therapy import Therapy
from app.models.order import Order

from werkzeug.utils import secure_filename

from app.config import UPLOAD_FOLDER

import os


# Blueprint admin
admin = Blueprint('admin', __name__,
                  url_prefix="/admin",
                  template_folder="../../templates",
                  static_folder="../../static")


ALLOWED_EXT = ['jpeg', 'jpg', 'png']


# URL homepage admin
@admin.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == 'GET'):
        return render_template('admin/index.html')
    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
    func = User.query.filter_by(email=email).first()
    if(not func or not func.verify_password(password) or func.user_type != "admin"):
        return render_template('admin/index.html',
                               error=True)
    else:
        login_user(func)
        return render_template('admin/index.html')


# URL to logout Admin/funcionario
@admin.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/admin')


# URL Profile admin
@admin.route('/profile', methods=['GET'])
def profile():
    if(request.method == 'GET'):
        return render_template('admin/profile.html')


# UPDATE Admin

# Password
@admin.route('/profile/password/', methods=['POST'])
def change_password():
    if(request.method == 'POST'):
        pwd = request.form['old_password']
        new_pwd = request.form['new_password']
        user = current_user
        if user and user.verify_password(pwd):
            user.password = new_pwd
            db.session.commit()
            logout_user()
            return redirect(url_for('admin.index'))
        else:
            return render_template('admin/profile.html',
                                   error=True)


# Data
@admin.route('/profile/data', methods=['POST'])
def change_data():
    if(request.method == 'POST'):
        user = current_user
        if(user):
            email = request.form['email']
            cep = request.form['cep']
            number = request.form['number']
            complement = request.form['complement']
            fname = request.form['fname']
            lname = request.form['lname']
            pwd = request.form['password']

            # Check if already exists user with the form's e-mail
            check_email = User.query.filter_by(email=email).first()
            if(check_email):
                if(check_email.email != user.email):
                    return render_template('admin/profile.html',
                                           email_error=True)
                else:
                    pass

            # verify's password
            if(user.verify_password(pwd)):
                try:
                    user.cep = cep
                    if(user.cep == cep):
                        user.email = email
                        user.number = number
                        user.complement = complement
                        user.fname = fname
                        user.lname = lname
                        user.set_address()
                        db.session.commit()
                        logout_user()
                        return redirect(url_for('admin.index'))
                    else:
                        raise ValueError('Valor de CEP inválido...')
                except Exception:
                    return render_template('admin/profile.html',
                                           error=True)
            else:
                return render_template('admin/profile.html',
                                       error=True)


# PRODUCT


# Index Products
@admin.route('/products', methods=['GET'])
def admin_products():
    if (request.method == 'GET'):
        return render_template('admin/products/products.html')


# READ all products
@admin.route('/products/list', methods=['GET'])
def list_products():
    if (request.method == 'GET'):
        all_products = Product.query.all()
        return render_template('admin/products/list.html',
                               all_products=all_products)


# URL to delete a product by it's id
@admin.route('/products/delete/<id_product>', methods=['GET'])
def delete_product(id_product):
    if (request.method == 'GET'):
        product = Product.query.get(id_product)
        if (product):
            os.remove(f"{UPLOAD_FOLDER}/Product/{product.img}")
            db.session.delete(product)
            db.session.commit()
            return redirect('/admin/products')
        else:
            return redirect(url_for('admin.list_products'))


# Add new product
@admin.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if (request.method == 'GET'):
        return render_template('admin/products/add.html')
    if (request.method == 'POST'):
        name = request.form['name']
        description = request.form['description']
        size = request.form['size']
        price = request.form['price']
        img = request.files['img']
        if(img):
            img_filename = secure_filename(img.filename)

            # Check if there's a valid extension
            check_ext = img_filename.split('.')
            if(check_ext[-1] not in ALLOWED_EXT):
                return render_template('admin/products/add.html',
                                       ext_error=True)

            # Check if already exists an img with same name
            check_img = Product.query.filter_by(img=img_filename).first()
            if(check_img):
                return render_template('admin/products/add.html',
                                       upload_error=True)

            # Save img inside UPLOAD_FOLDER
            img.save(os.path.join(f"{UPLOAD_FOLDER}/Product", img_filename))

            # Check if price has 2 decimals
            check_decimal = list(price.split("."))[-1]
            if(len(check_decimal) < 2):
                price += "0"
            new_product = Product(name=name,
                                  description=description,
                                  size=size,
                                  price=price,
                                  img=img_filename)

            # Checks if already exists a product with same name
            check_product = Product.query.filter_by(name=name).first()
            if (check_product):
                return render_template('admin/products/add.html',
                                       error=True)
            else:
                db.session.add(new_product)
                db.session.commit()
                return redirect('/admin/products')


# UPDATE a product
@admin.route('/products/change/<id_product>', methods=['GET', 'POST'])
def change_product(id_product):
    product = Product.query.get(id_product)
    if(product):
        if (request.method == 'GET'):
            return render_template('admin/products/update.html',
                                   product=product)
        if (request.method == 'POST'):
            name = request.form['name']
            description = request.form['description']
            size = request.form['size']
            price = request.form['price']

            # Check if price has 2 decimals
            check_decimal = list(price.split("."))[-1]
            if(len(check_decimal) < 2):
                price += "0"

            # Check if already exists a product with that name
            check_product = Product.query.filter_by(name=name).first()
            if(check_product):
                if(product.name != check_product.name):
                    return render_template('admin/products/update.html',
                                           error=True, product=product)

            # Get img and set a secure_filename
            img = request.files['img']
            if(img):
                img_filename = secure_filename(img.filename)

                # Check if there's a valid extension
                check_ext = img_filename.split('.')
                if(check_ext[-1] not in ALLOWED_EXT):
                    return render_template('admin/products/update.html',
                                           ext_error=True,
                                           product=product)

                # Check if already exists an img with same name
                check_img = Product.query.filter_by(img=img_filename).first()
                if(check_img):
                    if(img_filename != check_img.img):
                        return render_template('admin/products/update.html',
                                               upload_error=True,
                                               product=product)

                # Update new_img inside UPLOAD_FOLDER
                try:
                    os.remove(f"{UPLOAD_FOLDER}/Product/{product.img}")
                except Exception:
                    pass
                img.save(os.path.join(
                        f"{UPLOAD_FOLDER}/Product", img_filename))

                # Update image's name in product's column
                product.img = img_filename
                product.name = name
                product.description = description
                product.size = size
                product.price = price
                db.session.commit()
                return redirect('/admin/products')
    return render_template('admin/products/update.html',
                           error=True, product=product)


# THERAPY


# Index Therapies
@admin.route('/therapies', methods=['GET'])
def admin_therapies():
    if (request.method == 'GET'):
        return render_template('admin/therapies/therapies.html')


# READ all therapies
@admin.route('/therapies/list', methods=['GET'])
def list_therapies():
    if (request.method == 'GET'):
        all_therapies = Therapy.query.all()
        return render_template('admin/therapies/list.html',
                               all_therapies=all_therapies)


# ADD new therapy
@admin.route('/therapies/add', methods=['GET', 'POST'])
def add_therapy():
    if (request.method == 'GET'):
        return render_template('admin/therapies/add.html')
    if (request.method == 'POST'):
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        img = request.files['img']
        if(img):
            img_filename = secure_filename(img.filename)

            # Check if there's a valid extension
            check_ext = img_filename.split('.')
            if(check_ext[-1] not in ALLOWED_EXT):
                return render_template('admin/therapies/add.html',
                                       ext_error=True)

            # Check if already exists an img with same name
            check_img = Therapy.query.filter_by(img=img_filename).first()
            if(check_img):
                if(img_filename != check_img.img):
                    return render_template('admin/therapies/add.html',
                                           upload_error=True)

            # Save img inside UPLOAD_FOLDER
            img.save(os.path.join(f"{UPLOAD_FOLDER}/Therapy", img_filename))

            # Check if price has 2 decimals
            check_decimal = list(price.split("."))[-1]
            if(len(check_decimal) < 2):
                price += "0"

            new_therapy = Therapy(name=name,
                                  description=description,
                                  price=price,
                                  img=img_filename)
            # Checks if already exists a therapy with same name
            check_therapy = Therapy.query.filter_by(name=name).first()
            if (check_therapy):
                return render_template('admin/therapies/add.html',
                                       error=True)
            else:
                db.session.add(new_therapy)
                db.session.commit()
                return redirect('/admin/therapies')


# DELETE a therapy
@admin.route('/therapies/delete/<id_therapy>', methods=['GET'])
def delete_therapy(id_therapy):
    if (request.method == 'GET'):
        therapy = Therapy.query.get(id_therapy)
        if (therapy):
            os.remove(f"{UPLOAD_FOLDER}/Therapy/{therapy.img}")
            db.session.delete(therapy)
            db.session.commit()
            return redirect('/admin/therapies')
        else:
            return redirect('/admin/therapies')


# UPDATE a therapy
@admin.route('/therapies/change/<id_therapy>', methods=['GET', 'POST'])
def change_therapy(id_therapy):
    therapy = Therapy.query.get(id_therapy)
    if(therapy):
        if(request.method == 'GET'):
            return render_template('admin/therapies/update.html',
                                   therapy=therapy)
        if(request.method == 'POST'):
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']

            # Check if price has 2 decimals
            check_decimal = list(price.split("."))[-1]
            if(len(check_decimal) < 2):
                price += "0"

            # Check if already exists a therapy with that name
            check_therapy = Therapy.query.filter_by(name=name).first()
            if(check_therapy):
                if(therapy.name != check_therapy.name):
                    return render_template('admin/therapies/update.html',
                                           error=True, therapy=therapy)

            # Get img and set a secure_filename
            img = request.files['img']
            if(img):
                img_filename = secure_filename(img.filename)

                # Check if there's a valid extension
                check_ext = img_filename.split('.')
                if(check_ext[-1] not in ALLOWED_EXT):
                    return render_template('admin/therapies/update.html',
                                           ext_error=True,
                                           therapy=therapy)

                # Check if already exists an img with same name
                check_img = Therapy.query.filter_by(img=img_filename).first()
                if(check_img):
                    if(img_filename != check_img.img):
                        return render_template('admin/therapies/update.html',
                                               upload_error=True,
                                               therapy=therapy)

                # Update new_img inside UPLOAD_FOLDER
                os.remove(f"{UPLOAD_FOLDER}/Therapy/{therapy.img}")
                img.save(os.path.join(
                    f"{UPLOAD_FOLDER}/Therapy", img_filename))

                # Update image's name in therapy's column
                therapy.img = img_filename
                therapy.name = name
                therapy.description = description
                therapy.price = price
                db.session.commit()
                return redirect('/admin/therapies')
    return render_template('admin/therapies/update.html',
                           error=True,
                           therapy=therapy)


# ORDERS


# List orders
@admin.route('/orders', methods=['GET'])
def orders():
    user = current_user
    if(user):
        if(request.method == 'GET'):
            all_orders = Order.query.all()
            return render_template('admin/orders.html',
                                   all_orders=all_orders)

    return render_template('admin/orders.html',
                           error=True)


# Display a certain order
@admin.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    user = current_user
    if(user):
        if(request.method == 'GET'):
            order = Order.query.get(order_id)
            # set a list of products and therapies objects
            user_products = []
            user_therapies = []
            for product in order.products:
                item = Product.query.get(product)
                user_products.append(item)
            for therapy in order.therapies:
                item = Therapy.query.get(therapy)
                user_therapies.append(item)

            owner = User.query.get(order.id_user)
            return render_template('admin/close_order.html',
                                   order=order,
                                   owner=owner,
                                   user_products=user_products,
                                   user_therapies=user_therapies)


# Close an order
@admin.route('/order/delete/<order_id>', methods=['GET'])
def delete_order(order_id):
    user = current_user
    if(user):
        if(request.method == 'GET'):
            order = Order.query.get(order_id)
            db.session.delete(order)
            db.session.commit()

            return redirect(url_for('admin.orders'))
