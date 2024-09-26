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
    current_month = fn.strftime("%m", fn.datetime("now"))
    query = Venta.select(fn.SUM(Venta.cantidad * Venta.precio).alias("total")).where(
        fn.strftime("%m", Venta.fecha) == current_month
    )
    result = query.scalar()
    return result

def get_count_sell_by_ropa():
    current_month = fn.strftime("%m", fn.datetime("now"))
    query = (
        Venta.select(
            Categoria.nombre.alias("nombre"),
            fn.COUNT(Venta.id).alias("cantidad"),
        )
        .join(Ropa)
        .join(Categoria)
        .where(fn.strftime("%m", Venta.fecha) == current_month)
        .group_by(Categoria.nombre)
        .dicts()
    )
    return query


def check_ventas():
    query = Venta.select().count()
    return query > 0