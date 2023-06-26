from django.contrib import admin
from .models import *

# Register your models here.

# DEJA EN MODO TABLA LA VISUALIZACION EN EL ADMIN
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','imagen','precio','stock','descripcion','tipo','popular','created_at','update_at']
    search_fields = ['nombre']
    list_per_page = 10
    list_filter = ['tipo','precio']
    list_editable = ['precio','stock','descripcion','tipo']

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre','contrasena']
    search_fields = ['codigo']
    list_per_page = 10
    list_filter = ['codigo']

class CarritoAdmin(admin.ModelAdmin):
    list_display = ['codigo','imagen','usuario','cantidad','precio','nombre']
    search_fields = ['usuario']
    list_per_page = 10
    list_filter = ['precio']
    list_editable = ['precio']

class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['usuario','suscrito']
    search_fields = ['usuario']
    list_per_page = 10
    list_filter = ['suscrito']
    list_editable = ['suscrito']

class ContactoAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre','numero','correo']
    search_fields = ['nombre']
    list_per_page = 10
    list_filter = ['codigo']
    list_editable = ['numero','correo']

class RastreoAdmin(admin.ModelAdmin):
    list_display = ['codigo','contacto','f_toma','f_despacho','f_entrega']
    search_fields = ['codigo']
    list_per_page = 10
    list_filter = ['codigo']
    list_editable = ['contacto','f_despacho','f_entrega']

class HistorialAdmin(admin.ModelAdmin):
    list_display = ['orden','tipo','usuario','preciototal']
    search_fields = ['orden']
    list_per_page = 10
    list_filter = ['orden']
    list_editable = ['tipo']

class HistorialCarritoAdmin(admin.ModelAdmin):
    list_display = ['orden','imagen','usuario','cantidad','precio','nombre']
    search_fields = ['orden']
    list_per_page = 10
    list_filter = ['orden']
    



admin.site.register(TipoProducto)
admin.site.register(TipoEstado)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Usuarios,UsuarioAdmin)
admin.site.register(Suscripcion,SuscripcionAdmin)
admin.site.register(Carrito,CarritoAdmin)
admin.site.register(Historial,HistorialAdmin)
admin.site.register(HistorialCarrito,HistorialCarritoAdmin)

