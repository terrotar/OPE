
from flask import Blueprint, render_template, request, redirect, url_for

from flask_login import login_user, logout_user, current_user

from app import db

from app.models.user import User
from app.models.product import Product
from app.models.therapy import Therapy


import requests


# Blueprint admin
admin = Blueprint('admin', __name__,
                  url_prefix="/admin",
                  template_folder="../../templates",
                  static_folder="../../static")


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
        new_product = Product(name=name,
                              description=description,
                              size=size,
                              price=price)
        # Checks if already exists a product with same name
        check_product = Product.query.filter_by(name=name).first()
        if (check_product):
            return {'Error': 'Produto com mesmo nome já cadastrado.'}
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
            product.name = request.form['name']
            product.description = request.form['description']
            product.size = request.form['size']
            product.price = request.form['price']
            db.session.commit()
            return redirect('/admin/products')
    return render_template('admin/products/update.html',
                           error=True)


# THERAPY


# READ all therapies
@admin.route('/therapies', methods=['GET', 'POST'])
def list_therapies():
    if (request.method == 'GET'):
        all_therapies = Therapy.query.all()
        return render_template('therapies.html',
                               all_therapies=all_therapies)


# ADD new therapy
@admin.route('/add/therapy', methods=['GET', 'POST'])
def add_therapy():
    if (request.method == 'GET'):
        return render_template('new_therapy.html')
    if (request.method == 'POST'):
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        new_therapy = Therapy(name=name,
                              description=description,
                              price=price)
        # Checks if already exists a therapy with same name
        check_therapy = Therapy.query.filter_by(name=name).first()
        if (check_therapy):
            return {'Error': 'Terapia com mesmo nome já cadastrado.'}
        else:
            db.session.add(new_therapy)
            db.session.commit()
            return redirect('/admin/therapies')


# DELETE a therapy
@admin.route('/delete/therapy/<id_therapy>', methods=['GET'])
def delete_therapy(id_therapy):
    if (request.method == 'GET'):
        therapy = Therapy.query.get(id_therapy)
        if (therapy):
            db.session.delete(therapy)
            db.session.commit()
            return redirect('/admin/therapies')
        else:
            return {'Error': 'id_therapy não existe no banco de dados.'}


# UPDATE a therapy
@admin.route('/change/therapy', methods=['GET', 'POST'])
def change_therapy():
    id_therapy = request.args.get('id_therapy')
    therapy = Therapy.query.get(id_therapy)
    if (request.method == 'GET'):
        return render_template('change_therap.html',
                               therapy=therapy)
    if (request.method == 'POST'):
        therapy_id = request.form['therapy_id']
        therapy = Therapy.query.get(therapy_id)
        therapy.name = request.form['name']
        therapy.description = request.form['description']
        therapy.price = request.form['price']
        db.session.commit()
        return redirect('/admin/therapies')
