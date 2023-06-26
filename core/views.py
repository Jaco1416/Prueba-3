from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .serializers import *
from rest_framework import viewsets
import requests

#FUNCION GENERICA QUE VALIDA EL GRUPO DEL USUARIO
def validar_grupo(nombre_grupo):
    def decorator(view_fuc):
        user_passes_test(lambda user: user.groups.filter(name = nombre_grupo).exists())
        def wrapper(request, *arg, **kwargs):
            return view_fuc(request, *arg, **kwargs)
        return wrapper
    return decorator

#@validar_grupo('aqui nombre grupo')

#NOS PERMITE MOSTRAR LA INFO
class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    #queryset = Producto.objetcs
    serializer_class = ProductoSerializer

class TipoProductoViewset(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    #queryset = Producto.objetcs
    serializer_class = TipoProductoSerializer

class TipoEstadoViewset(viewsets.ModelViewSet):
    queryset = TipoEstado.objects.all()
    #queryset = Producto.objetcs
    serializer_class = TipoEstadoSerializer


# VISTAS.
def index(request):
    productosAll = Producto.objects.all() # SELECT * FROM producto
    data = {
        'listaProductos' : productosAll
    }
    if request.method == 'POST':
        prod = Carrito()
        codigoprod = request.POST.get('codigop')
        stock = request.POST.get('stocks')
        precio = request.POST.get('precio')
        nombre = request.POST.get('nombre')
        usuarioprod = request.POST.get('txtUsuario')
        imagen = request.POST.get('imagen')
        if Carrito.objects.filter(Q(codigo=codigoprod) & Q(usuario=usuarioprod)  & Q(nombre=nombre)).exists(): 
            product = Carrito.objects.get(Q(codigo=codigoprod)& Q(usuario=usuarioprod) & Q(nombre=nombre))
            product.cantidad += int(stock)
            product.precio =  int(precio)
            product.save()
        else:
            prod.codigo = request.POST.get('codigop')
            prod.nombre = request.POST.get('nombre')
            prod.precio = int(stock) * int(precio)
            prod.imagen = request.POST.get('imagen')
            prod.cantidad = request.POST.get('stocks')
            prod.usuario = request.POST.get('txtUsuario')
            prod.save()


        stocks = request.POST.get('stocks')
        codigop = request.POST.get('codigop')
        producto = Producto.objects.get(codigo=int(codigop))
        producto.stock -= int(stocks)
        producto.save()
        
    return render(request, 'core/index.html', data)

def indexapi(request):
    #obtiene los datos del api
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    respuesta2 = requests.get('https://rickandmortyapi.com/api/character')
    respuesta3 = requests.get('https://mindicador.cl/api')
    #transformar el json
    producto = respuesta.json()
    aux = respuesta2.json()
    moneda = respuesta3.json()
    personajes = aux['results']

    data = {
        'listaProductos' : producto,
        'personajes' : personajes,
        'moneda' : moneda,
    }
      
    return render(request, 'core/indexapi.html', data)

# CRUD
@login_required
def add(request):
    data = {
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            data['msj'] = "Producto guardado correctamente"

    return render(request, 'core/add_product.html', data)

@login_required
def update(request, id):
    producto = Producto.objects.get(id=id) # OBTIENE UN PRODUCTO POR EL ID
    data = {
        'form' : ProductoForm(instance=producto) # CARGAMOS EL PRODUCTO EN EL FORMULARIO
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES) # NUEVA INFORMACION
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            data['msj'] = "Producto actualizado correctamente"
            data['form'] = formulario # CARGA LA NUEVA INFOR EN EL FORMULARIO

    return render(request, 'core/update_product.html', data)

@login_required
def deleteProducto(request, id):
    producto = Producto.objects.get(id=id) # OBTIENE UN PRODUCTO POR EL ID
    producto.delete()

    return redirect(to="index")


@login_required
def suscripcion(request):
    suscripcionAll = Suscripcion.objects.all()
    datos = {
        'suscripciones' : suscripcionAll
    }
    if request.method == 'POST':
        usuarios = Suscripcion()
        usuarios.usuario = request.user.get_username()
        usuarios.suscrito = request.POST.get('estado')
        group = Group.objects.get(name='Suscrito')
        group.user_set.add(usuarios.usuario)
        usuarios.save()

    return render(request, 'core/suscripcion.html', datos)


def tienda(request):
    productosAll = Producto.objects.all() # SELECT * FROM producto
    data = {
        'listaProductos' : productosAll
    }
    if request.method == 'POST':
        prod = Carrito()
        codigoprod = request.POST.get('codigop')
        stock = request.POST.get('stocks')
        precio = request.POST.get('precio')
        imagen = request.POST.get('imagen')
        nombre = request.POST.get('nombre')
        if Carrito.objects.filter(Q(codigo=codigoprod)  & Q(nombre=nombre)).exists(): 
            product = Carrito.objects.get(Q(codigo=codigoprod) & Q(nombre=nombre))
            product.cantidad += int(stock)
            product.precio =  int(precio)
            product.save()
        else:
            prod.codigo = request.POST.get('codigop')
            prod.nombre = request.POST.get('nombre')
            prod.precio = int(stock) * int(precio)
            prod.imagen = request.POST.get('imagen')
            prod.cantidad = request.POST.get('stocks')
            prod.usuario = request.POST.get('txtUsuario')
            prod.save()
            
        stocks = request.POST.get('stocks')
        codigop = request.POST.get('codigop')
        producto = Producto.objects.get(codigo=int(codigop))
        producto.stock -= int(stocks)
        producto.save()
        
    return render(request, 'core/tienda.html', data)

@login_required
def cart(request):
    carritoAll = Carrito.objects.all() # SELECT * FROM producto
    respuesta3 = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta3['serie'][0]['valor']
    total = 0
    totalDef = 0
    descuento = 0
    
    for i in carritoAll: 
        total += i.precio * i.cantidad

    
    totalDef = (total/valor_usd)    
    
    
    
         
    data = {
        'listaCarrito' : carritoAll,'totalDef' : round(totalDef, 2), 'descuento' : descuento, 'total' : total,
    }
    if request.method == 'POST':
        productos = Carrito()
        productos.id = request.POST.get('id')
        prod = productos.delete()
        if prod[0] == 0:
            codigop = request.POST.get('codigop')
            stock = request.POST.get('stocks')
            producto = Producto.objects.get(codigo=int(codigop))
            producto.stock += int(stock)
            producto.save()
   
    return render(request, 'core/cart.html',data)

def pagar(request, usuario):
        
    if request.method == 'POST':
        carrito = Carrito()
        carrito.usuario = request.POST.get('txtUsuario')
        carrito.codigo = request.POST.get('codigo')
        carrito.cantidad = request.POST.get('stocks')
        carrito.nombre = request.POST.get('nombre')
        carrito.precio = request.POST.get('txtUsuario')
        carrito.imagen = request.POST.get('imagen')
        orden = 0 
        HistorialCarrito.save()
        if Carrito.usuario == usuario :
            orden += 1 
            HistorialCarrito.save()
            Carrito.delete() 
    

    return render(request, 'core/cart.html')
    


def registrar(request):
    datos = {
        'form' : RegistroUsuarioForm()
    }
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            group = Group.objects.get(name='cliente')
            group.user_set.add(usuario)
            suscrito = Suscripcion()
            suscrito.usuario = request.POST.get('username')
            suscrito.suscrito = False
            suscrito.save()
            formulario.save()
            messages.success(request,'Usuario guardado correctamente!')
    return render(request, 'registration/registrar.html', datos)

@login_required
def checkout(request):
    return render(request, 'core/checkout.html')

@login_required
def contacto(request):
    contactoAll = Contacto.objects.all()
    data = {
        'listaContacto' : contactoAll
    }
    return render(request, 'core/contacto.html', data)


# CRUD
@login_required
def addContacto(request):
    data = {
        'form' : ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(request.POST, files=request.FILES) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            data['msj'] = "Contacto guardado correctamente"

    return render(request, 'core/add_contacto.html', data)

@login_required
def updateContacto(request, codigo):
    contacto = Contacto.objects.get(codigo=codigo) # OBTIENE UN PRODUCTO POR EL ID
    data = {
        'form' : ContactoForm(instance=contacto) # CARGAMOS EL PRODUCTO EN EL FORMULARIO
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST, instance=contacto, files=request.FILES) # NUEVA INFORMACION
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            data['msj'] = "Contacto actualizado correctamente"
            data['form'] = formulario # CARGA LA NUEVA INFOR EN EL FORMULARIO

    return render(request, 'core/update_contacto.html', data)

@login_required
def deleteContacto(request, codigo):
    contacto = Contacto.objects.get(codigo=codigo) # OBTIENE UN PRODUCTO POR EL ID
    contacto.delete()

    return redirect(to="index")


def usuarios(request):
    usuariosAll = usuarios.objects.all()
    data = {
        'listaUsuarios' : usuariosAll
    }
    return render(request,'core/usuarios.html', data)

@login_required
def historial(request):
    historialAll = Historial.objects.all()
    data = {
        'listaHistorial' : historialAll 
    }

    return render(request,'core/historial.html', data)

@login_required
def detalle_historial(request):
    historialcarritoAll = HistorialCarrito.objects.all()
    data = {
        'listaHistorialCarrito' : historialcarritoAll 
    }

    return render(request,'core/detalle_historial.html', data)