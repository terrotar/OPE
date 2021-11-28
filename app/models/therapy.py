from app.config import db
from sqlalchemy.ext.hybrid import hybrid_property


# Columns of table Therapy
class Therapy(db.Model):
    __tablename__ = "terapia"
    id = db.Column("id_terapia", db.Integer, primary_key=True)
    __name = db.Column("nome", db.String, unique=True, nullable=False)
    __description = db.Column("descricao", db.String, nullable=False)
    __price = db.Column("preco", db.String, nullable=False)
    __img = db.Column("imagem", db.String, nullable=False)

    # Relationships
    cart = db.relationship("Cart_Therapy", cascade="all,delete", back_populates="therapy")
    # orders = db.relationship("Order", back_populates="therapies")

    def __init__(self, name, description, price, img):
        self.__name = name
        self.__description = description
        self.__price = price
        self.__img = img

# PROPERTIES of GET and SET attributes
    # Name
    @hybrid_property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    # Description
    @hybrid_property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    # Price
    @hybrid_property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

    # img
    @hybrid_property
    def img(self):
        return self.__img

    @img.setter
    def img(self, img):
        self.__img = img
