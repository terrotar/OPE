
from flask import Blueprint, render_template, request, redirect

from flask_login import login_user, logout_user, current_user

from app import db

from app.models.func_model import Admin
from app.models.prod_model import Product


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
    return render_template('index_admin.html')


# URL that list all products
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


# URL to create a new product
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
