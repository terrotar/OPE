
from flask import Blueprint, render_template, request

from flask_login import login_user, logout_user, current_user

from app import db

from app.models.func_model import Admin


# Blueprint admin
admin = Blueprint('admin', __name__,
                  url_prefix="/admin",
                  template_folder="../../html_teste",
                  static_folder="../../estaticos_teste")


# URL homepage/login table Admin/funcionario
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


# URL logout Admin/funcionario
@admin.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('index_admin.html')


# URL product
@admin.route('/products', methods=['GET', 'POST'])
def list_products():
    if (request.method == 'GET'):
        return render_template('products.html')
