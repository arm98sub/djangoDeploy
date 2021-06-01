from django.db import models
from datetime import date
from datetime import datetime
from usuarios.models import Usuario


class Videojuego(models.Model):
    titulo = models.CharField('Título', max_length=50, unique=True)
    anio = models.IntegerField('Año')
    categoria = models.ForeignKey("videojuego.Categoria", verbose_name='Categoría', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField("Unidades")
    descripcion = models.CharField('Descripción', max_length=250, null=True, blank=True)

    def __str__(self):
        return self.titulo


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    

class Venta(models.Model):
    fecha = models.DateField(auto_now_add = True)
    usuario = models.ForeignKey("usuarios.Usuario",verbose_name=("Usuario"), on_delete= models.CASCADE)

class DetalleVenta(models.Model):
    articulo = models.ForeignKey("videojuego.Videojuego", verbose_name=("Videojuego"), on_delete=models.CASCADE)
    venta = models.ForeignKey("videojuego.Venta", verbose_name=("Videojuego"), on_delete=models.CASCADE)

    
