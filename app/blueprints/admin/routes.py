
from flask import Blueprint, render_template, request


# Instancia do Blueprint admin
admin = Blueprint('admin', __name__,
                  url_prefix="/admin",
                  template_folder="../../html_teste",
                  static_folder="../../estaticos_teste")


# URL da homepage de admin
@admin.route('/', methods=['GET'])
def index():
    if(request.method == 'GET'):
        return render_template('index_admin.html')
