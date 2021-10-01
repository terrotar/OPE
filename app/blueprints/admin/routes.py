
from flask import Blueprint, render_template, request, redirect

from flask_login import login_user, logout_user, current_user

from app import db

from app.models.func_model import Admin
from app.models.prod_model import Product
from app.models.therap_model import Therapy


import requests


# Blueprint admin
admin = Blueprint('admin', __name__,
                  url_prefix="/admin",
                  template_folder="../../html_teste",
                  static_folder="../../estaticos_teste")


# URL homepage/login of table Admin/funcionario
@admin.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == 'GET'):
        return render_template('index_admin.html')
    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
    func = Admin.query.filter_by(email=email).first()
    if(not func or not func.verify_password(password)):
        return render_template('index_admin.html',
                               error=True)
    else:
        login_user(func)
        return render_template('index_admin.html')


# URL to logout Admin/funcionario
@admin.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/admin')
    # return render_template('index_admin.html')


# PRODUCT


# READ all products
@admin.route('/products', methods=['GET', 'POST'])
def list_products():
    if (request.method == 'GET'):
        all_products = Product.query.all()
        return render_template('products.html',
                               all_products=all_products)


# URL to delete a product by it's id
@admin.route('/delete/product/<id_product>', methods=['GET'])
def delete_product(id_product):
    if (request.method == 'GET'):
        product = Product.query.get(id_product)
        if (product):
            db.session.delete(product)
            db.session.commit()
            return redirect('/admin/products')
        else:
            return {'Error': 'id_product não existe no banco de dados.'}


# Add new product
@admin.route('/add/product', methods=['GET', 'POST'])
def add_product():
    if (request.method == 'GET'):
        return render_template('new_product.html')
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
@admin.route('/change/product', methods=['GET', 'POST'])
def change_product():
    id_product = request.args.get('id_product')
    product = Product.query.get(id_product)
    if (request.method == 'GET'):
        return render_template('change_prod.html',
                               product=product)
    if (request.method == 'POST'):
        product_id = request.form['product_id']
        product = Product.query.get(product_id)
        product.name = request.form['name']
        product.description = request.form['description']
        product.size = request.form['size']
        product.price = request.form['price']
        db.session.commit()
        return redirect('/admin/products')


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
