from app import db

from app.models.user import User

from flask import Blueprint, render_template, request

from flask_login import login_user


# Instancia do Blueprint register
register = Blueprint('register', __name__, template_folder="../../templates/index.html")


@register.route('/cadastrar', methods=['GET', 'POST'])
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
            new_user.set_address()
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return render_template('index.html')
        else:
            return render_template('register.html',
                                   check_error=True)
