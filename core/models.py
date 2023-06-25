from django.db import models

# Create your models here.

# ES DONDE CREAN LAS TABLAS
class TipoProducto(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class TipoEstado(models.Model):
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.estado


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=250)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    imagen = models.ImageField(null=True,blank=True)
    popular = models.BooleanField()
    codigo = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.nombre
    
class Usuarios(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(null=False,max_length=100)
    contrasena = models.CharField(null=False,max_length=50)
    def __str__(self):
        return self.nombre
    
class Suscripcion(models.Model):
    usuario = models.CharField(null=False,max_length=100,primary_key=True)
    suscrito = models.BooleanField()

    def __str__(self):
        return self.usuario
    

    
class Carrito(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(null=True,blank=True)
    usuario = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
class HistorialCarrito(models.Model):
    usuario = models.CharField(max_length=40)
    codigo = models.IntegerField()
    cantidad = models.IntegerField()
    nombre = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to="carrito", null=True)
    orden = models.IntegerField()

    def __str__(self):
        return self.usuario

    class Meta:
        db_table = 'db_carrito_historico'


class Historial(models.Model):
    orden = models.IntegerField()
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=50)
    preciototal = models.IntegerField()

    def __str__(self):
        return self.usuario

    class Meta:
        db_table = 'db_historia'

class Contacto(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(null=False,max_length=100)
    numero = models.IntegerField(null=False)
    correo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
