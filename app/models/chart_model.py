from app.config import db
from sqlalchemy.ext.hybrid import hybrid_property


# Columns of table Chart_Product
class Chart_Product(db.Model):
    __tablename__ = "produto_carrinho"
    id = db.Column("id_carrinho", db.Integer, primary_key=True)
    __id_user = db.Column("id_usuario", db.Integer, unique=True, nullable=False)
    __id_user = db.Column("id_usuario", db.Integer, unique=False, nullable=False)
    __id_user = db.Column("id_usuario", db.Integer, unique=True, nullable=False)

    def __init__(self, id_user, unit_price, qtd):
        self.__id_user = id_user
        self.__unit_price = unit_price
        self.__qtd = qtd

# GETTERS AND SETTERS
    # id_user
    @hybrid_property
    def id_user(self):
        return self.__id_user

    @id_user.setter
    def id_user(self, id_user):
        self.__id_user = id_user
