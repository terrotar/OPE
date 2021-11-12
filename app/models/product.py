from app.config import db
from sqlalchemy.ext.hybrid import hybrid_property


# Columns of table Product
class Product(db.Model):
    __tablename__ = "produto"
    id = db.Column("id_produto", db.Integer, primary_key=True)
    __name = db.Column("nome", db.String, unique=True, nullable=False)
    __description = db.Column("descricao", db.String, unique=False, nullable=False)
    __size = db.Column("tamanho", db.Float, unique=False, nullable=False)
    __price = db.Column("preco", db.Float, unique=False, nullable=False)
    __img = db.Column("imagem", db.String, nullable=False)

    # Relationships
    cart = db.relationship("Cart_Product", cascade="all,delete", back_populates="product")

    def __init__(self, name, description, size, price, img):
        self.__name = name
        self.__description = description
        self.__size = size
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

    # Size
    @hybrid_property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

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
