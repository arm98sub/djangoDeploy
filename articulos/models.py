from django.db import models


class Articulo(model.Model):
    nombre = models.CharField("Articulo",max_length =150)
    descripcion = models.CharField("Descripcion", max_length= 300)