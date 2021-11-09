from app.config import db
from sqlalchemy.ext.hybrid import hybrid_property


# Columns of table Cart_Therapy
class Cart_Therapy(db.Model):
    __tablename__ = "terapia_carrinho"
    id = db.Column("id_terapia_carrinho", db.Integer, primary_key=True)
    __id_user = db.Column("id_usuario", db.Integer, db.ForeignKey("usuario.id_usuario"))
    __id_therapy = db.Column("id_terapia", db.Integer, db.ForeignKey("terapia.id_terapia"))
    __unit_price = db.Column("preco_unit", db.Float, unique=False, nullable=False)
    __qtd = db.Column("qtd", db.Integer, unique=False, nullable=False)

    def __init__(self, id_user, id_therapy, unit_price, qtd):
        self.__id_user = id_user
        self.__id_therapy = id_therapy
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

    # id_therapy
    @hybrid_property
    def id_therapy(self):
        return self.__id_therapy

    # unit_price
    @hybrid_property
    def unit_price(self):
        return self.__unit_price

    @unit_price.setter
    def unit_price(self, unit_price):
        self.__unit_price = unit_price

    # qtd
    @hybrid_property
    def qtd(self):
        return self.__qtd

    @qtd.setter
    def qtd(self, qtd):
        self.__qtd = qtd
