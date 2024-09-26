from src.db.model import Categoria, Venta, Ropa
from peewee import fn


def get_sell_by_month():
    query = (
        Venta.select(
            fn.strftime("%m", Venta.fecha).alias("mes"),
            fn.COUNT(Venta.id).alias("cantidad"),
        )
        .group_by(fn.strftime("%m", Venta.fecha))
        .dicts()
    )
    return query


def get_sell_total():
    query = Venta.select(fn.SUM(Venta.cantidad * Venta.precio).alias('total')) 
    result = query.scalar() 
    return result

def get_count_sell_by_ropa():
    query = (
        Venta.select(
            Ropa.categoria.nombre.alias("nombre"),
            fn.COUNT(Venta.id).alias("cantidad"),
        )
        .join(Ropa)
        .join(Categoria)
        .group_by(Categoria.nombre)
        .dicts()
    )
    return query

