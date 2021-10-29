from flask import Blueprint, render_template, request


# Instancia do Blueprint home
home = Blueprint('home', __name__,
                 template_folder="../../templates",
                 static_folder="../../estatic")


# URL da homepage
@home.route('/', methods=['GET'])
def index():
    if(request.method == 'GET'):
        return render_template('index.html')
