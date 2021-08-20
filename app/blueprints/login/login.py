from app.config import db

from app.models.user import User

from flask import Blueprint, render_template, request

from flask_login import login_user, logout_user


# Instancia do Blueprint login
login = Blueprint('login', __name__, template_folder="../../templates/index.html")


# URL para usuário logar
@login.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'GET'):
        return render_template('login.html')
    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if(not user and not user.verify_password(password)):
        return render_template('login.html',
                               error=True)
    else:
        login_user(user)
        return render_template('index.html')


# URL para usuário deslogar
@login.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('index.html')


# URL para usuário alterar a senha
@login.route('/<username>/change_password', methods=['GET', 'POST'])
def change_password(username):
    if(request.method == 'GET'):
        return render_template('change_pwd.html')
    if(request.method == 'POST'):
        pwd = request.form['password']
        new_pwd = request.form['new_password']
        user = User.query.filter_by(name=username).first()
        if user and user.verify_password(pwd):
            user.password = new_pwd
            db.session.commit()
            return render_template('login.html')
        else:
            return render_template('change_pwd.html',
                                   check_error=True)


# URL para usuário alterar dados da conta
@login.route('/<username>/change_data', methods=['GET', 'POST'])
def change_data(username):
    if(request.method == 'GET'):
        return render_template('change_data.html')
    if(request.method == 'POST'):
        email = request.form['email']
        cep = request.form['cep']
        complement = request.form['complement']
        name = request.form['name']
        pwd = request.form['password']
        user = User.query.filter_by(name=username).first()
        if user and user.verify_password(pwd):
            user.email = email
            user.cep = cep
            user.complement = complement
            user.name = name
            user.set_address()
            db.session.commit()
            return render_template('login.html')
        else:
            return render_template('change_data.html',
                                   check_error=True)


# URL para usuário deletar a própria conta
@login.route('/<username>/delete', methods=['GET', 'POST'])
def delete_user(username):
    if(request.method == 'GET'):
        return render_template('delete_account.html')
    if(request.method == 'POST'):
        pwd = request.form['password']
        user = User.query.filter_by(name=username).first()
        if user and user.verify_password(pwd):
            db.session.delete(user)
            db.session.commit()
            return render_template('index.html')
        else:
            return render_template('delete_account.html',
                                   check_error=True)
