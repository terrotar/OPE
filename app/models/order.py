from app.config import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import ARRAY as test


# Columns of table Order
class Order(db.Model):
    __tablename__ = "pedido"
    id = db.Column("id_pedido", db.Integer, primary_key=True)
    __id_user = db.Column("id_usuario", db.Integer, db.ForeignKey("usuario.id_usuario"))
    __products = db.Column("id_produtos", test(db.Integer), nullable=True)
    __therapies = db.Column("id_terapias", db.ARRAY(db.Integer), nullable=True)
    __amount_order = db.Column("total", db.Float, nullable=False)

    # Relationships
    owner = db.relationship("User", back_populates="orders")
    # products = db.relationship("Product", back_populates="orders")
    # therapies = db.relationship("Therapy", back_populates="orders")

    def __init__(self, id_user, products, therapies, amount_order):
        self.__id_user = id_user
        self.__products = products
        self.__therapies = therapies
        self.__amount_order = amount_order

# GETTERS AND SETTERS
    # id_user
    @hybrid_property
    def id_user(self):
        return self.__id_user

    @id_user.setter
    def id_user(self, id_user):
        self.__id_user = id_user

    # products
    @hybrid_property
    def products(self):
        return self.__products

    @products.setter
    def products(self, products):
        self.__products = products

    # therapies
    @hybrid_property
    def therapies(self):
        return self.__therapies

    @therapies.setter
    def therapies(self, therapies):
        self.__therapies = therapies

    # amount_order
    @hybrid_property
    def amount_order(self):
        return self.__amount_order

    @amount_order.setter
    def amount_order(self, amount_order):
        self.__amount_order = amount_order
