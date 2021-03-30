from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/TCC"
# mysql://scott:tiger@localhost/mydatabase


db = SQLAlchemy(app)


class Pedro(db.Model):
    ra = db.Column(db.Integer, primary_key=True, auto_increment=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    logradouro = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.String(5), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(20), nullable=False)


db.create_all()


@app.route("/", methods=["GET"])
def index():
    Pedro(nome="SEI LA",
          email="SEILA@SEILA.COM.BR",
          logradouro="SEI LA",
          numero="66666",
          cep="666666-666",
          complemento="LÁ NO SEI LA")
    return "deu boa"
