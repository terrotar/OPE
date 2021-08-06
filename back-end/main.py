from app import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app.models import User


@app.route('/', methods=['GET'])
def index():
    if(request.method == 'GET'):
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/cadastrar', methods=['GET', 'POST'])
def register():
    if(request.method == 'GET'):
        return render_template('register.html')
    if(request.method == 'POST'):
        new_user = User(email=request.form['email'],
                        password=request.form['password'],
                        cpf=request.form['cpf'],
                        cep=request.form['cep'],
                        complement=request.form['complement'],
                        name=request.form['name'],
                        bday=int(request.form['bday']),
                        bmonth=int(request.form['bmonth']),
                        byear=int(request.form['byear']))
        email_checker = User.query.filter_by(email=request.form['email']).first()
        cpf_checker = User.query.filter_by(cpf=request.form['cpf']).first()
        if email_checker or cpf_checker:
            return render_template('register.html',
                                   check_error=True)
        if(new_user.check_cpf() is True) and (new_user.check_age() is True):
            new_user.set_adress()
            db.session.add(new_user)
            db.session.commit()
            return render_template('index.html')
        else:
            return render_template('register.html',
                                   check_error=True)


@app.route('/<username>/change_password', methods=['GET', 'POST'])
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


@app.route('/<username>/change_data', methods=['GET', 'POST'])
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
            user.set_adress()
            db.session.commit()
            return render_template('login.html')
        else:
            return render_template('change_data.html',
                                   check_error=True)


@app.route('/<username>/delete', methods=['GET', 'POST'])
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


if __name__ == "__main__":
    app.run(debug=True)
