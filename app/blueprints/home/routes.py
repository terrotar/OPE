from flask import Blueprint, render_template, request

from app.models.therapy import Therapy
from app.models.product import Product


# Instancia do Blueprint home
home = Blueprint('home', __name__,
                 template_folder="../../templates",
                 static_folder="../../static")


# URL da homepage
@home.route('/', methods=['GET'])
def index():
    if(request.method == 'GET'):
        all_therapies = Therapy.query.all()
        all_products = Product.query.all()
        return render_template('index.html',
                               all_therapies=all_therapies,
                               all_products=all_products)
