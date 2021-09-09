
from flask import Blueprint, render_template, request

from flask_login import login_user, logout_user, current_user

from app import db

from app.models.func_model import Admin


# Instancia do Blueprint admin
admin = Blueprint('admin', __name__,
                  url_prefix="/admin",
                  template_folder="../../html_teste",
                  static_folder="../../estaticos_teste")


# URL da homepage de admin
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


@admin.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('index_admin.html')
