from django.urls import path, include
from .views import *
from rest_framework import routers

#RUTAS DEL API
router = routers.DefaultRouter()
router.register('productos',ProductoViewset)
router.register('tipoproductos',TipoProductoViewset)


urlpatterns = [
    #API
    path('api/', include(router.urls)),
    #RUTAS
    path('', index, name="index"),
    path('indexapi/', indexapi, name="indexapi"),
    path('suscripcion/', suscripcion, name="suscripcion"),
    path('cart/', cart, name="cart"),
    path('contacto/', contacto, name="contacto"),
    path('tienda/', tienda, name="tienda"),
    path('registrar/', registrar, name="registrar"),
    path('historial/', historial, name="historial"),
    path('usuarios/', usuarios, name="usuarios"),
    path('detalle_historial/', detalle_historial, name="detalle_historial"),

    #CRUD
    path('add/', add, name="add"),
    path('update/<id>/', update, name="update"),
    path('delete/<id>/', deleteProducto, name="delete"),
    #CRUDCONTACTO
    path('addContacto/', addContacto, name="addContacto"),
    path('updateContacto/<codigo>/', updateContacto, name="updateContacto"),
    path('deleteContacto/<codigo>/', deleteContacto, name="deleteContacto")
]