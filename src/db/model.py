from peewee import *

db = SqliteDatabase("tienda.db")


class Categoria(Model):
    id = AutoField(True)
    nombre = CharField()
    eliminado = BooleanField(default=False)

    class Meta:
        database = db


class Size(Model):
    id = AutoField(True)
    nombre = CharField()
    eliminado = BooleanField(default=False)

    class Meta:
        database = db


class Marca(Model):
    id = AutoField(True)
    nombre = CharField()
    eliminado = BooleanField(default=False)

    class Meta:
        database = db


class Ropa(Model):
    id = AutoField(True)
    precio = FloatField()
    categoria = ForeignKeyField(Categoria)
    size = ForeignKeyField(Size)
    marca = ForeignKeyField(Marca)
    cantidad = IntegerField()
    fecha = DateField("dd/mm/yyyy")
    eliminado = BooleanField(default=False)

    class Meta:
        database = db


class Venta(Model):
    id = AutoField(True)
    fecha = DateField("dd/mm/yyyy")
    ropa = ForeignKeyField(Ropa)
    cantidad = IntegerField()
    precio = IntegerField()
    descuento = IntegerField()
    precio_final = IntegerField()
    dinero_pagado = IntegerField()

    class Meta:
        database = db


class Compra(Model):

    id = AutoField(True)
    fecha = DateField()
    ropa = ForeignKeyField(Ropa)
    cantidad = IntegerField()
    precio = IntegerField()

    class Meta:
        database = db


db.create_tables([Categoria, Size, Marca, Ropa, Venta, Compra])
