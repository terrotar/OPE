from app.config import db
from sqlalchemy.ext.hybrid import hybrid_property


# Columns of table Chart_Product
class Chart(db.Model):
    __tablename__ = "carrinho"
    id = db.Column("id_carrinho", db.Integer, primary_key=True)
    __id_user = db.Column("id_usuario", db.Integer, db.ForeignKey("usuario.id_usuario"))
    __id_chart_therapy = db.Column("id_terapia_carrinho", db.ARRAY(db.Integer), unique=False, nullable=True)
    __id_chart_prod = db.Column("id_produto_carrinho", db.ARRAY(db.Integer), unique=False, nullable=True)

    def __init__(self, id_user, id_chart_therapy, id_chart_prod):
        self.__id_user = id_user
        self.__id_chart_therapy = id_chart_therapy
        self.__id_chart_prod = id_chart_prod

# GETTERS AND SETTERS
    # id_chart_therapy
    @hybrid_property
    def id_chart_therapy(self):
        return self.__id_chart_therapy

    @id_chart_therapy.setter
    def id_chart_therapy(self, id_chart_therapy):
        self.__id_chart_therapy.append(id_chart_therapy)

    # id_chart_prod
    @hybrid_property
    def id_chart_prod(self):
        return self.__id_chart_prod

    @id_chart_prod.setter
    def id_chart_prod(self, id_chart_prod):
        self.__id_chart_prod.append(id_chart_prod)
