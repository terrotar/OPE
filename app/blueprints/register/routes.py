from flask import Blueprint, render_template, request, redirect, url_for

from flask_login import login_user

from app.config import db

from app.models.user import User

import datetime


# Instancia do Blueprint register
register = Blueprint('register', __name__,
                     template_folder="../../templates",
                     static_folder="../../static")


@register.route('/cadastrar', methods=['GET', 'POST'])
def register_user():
    if(request.method == 'GET'):
        return render_template('register.html')
    if(request.method == 'POST'):
        bday = int(request.form['bday'])
        bmonth = int(request.form['bmonth'])
        byear = int(request.form['byear'])
        birthday = datetime.date(byear, bmonth, bday)
        new_user = User(email=request.form['email'],
                        password=request.form['password'],
                        cpf=int(request.form['cpf']),
                        cep=request.form['cep'],
                        number=request.form['number'],
                        complement=request.form['complement'],
                        fname=request.form['fname'],
                        lname=request.form['lname'],
                        birthday=birthday)
        email_checker = User.query.filter_by(email=request.form['email']).first()
        cpf_checker = User.query.filter_by(cpf=request.form['cpf']).first()
        if email_checker or cpf_checker:
            return render_template('register.html',
                                   check_error=True)
        if(new_user.check_cpf() is True) and (new_user.check_age() is True):
            new_user.set_address()
            new_user.set_age()
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home.index'))
        else:
            return render_template('register.html',
                                   check_error=True)
