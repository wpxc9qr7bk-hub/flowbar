from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from django.db.models import Q 

def obtener_carrito(request):
    cart = request.session.get('cart', {})
    return sum(cart.values())

def carta(request):
    # "Todos": Muestra todo
    tragos = Producto.objects.all()
    return render(request, 'menu/carta.html', {
        'tragos': tragos, 
        'cart_count': obtener_carrito(request),
        'categoria_actual': 'todos'
    })

def categoria_tragos(request):
    # Tragos: Piscola, Cuba Libre, Ramazzotti, Tropical Gin
    nombres = ['Piscola', 'Cuba Libre', 'Ramazzotti', 'Tropical Gin']
    
    query = Q()
    for nombre in nombres:
        query |= Q(descripcion__icontains=nombre)
        
    tragos = Producto.objects.filter(query)
    
    return render(request, 'menu/carta.html', {
        'tragos': tragos, 
        'cart_count': obtener_carrito(request),
        'categoria_actual': 'tragos'
    })

def categoria_cervezas(request):
    # Cervezas: Cerveza Corona
    # Usamos 'Corona' para ser más flexibles, o puedes poner 'Cerveza Corona' exacto
    tragos = Producto.objects.filter(descripcion__icontains='Corona')
    
    return render(request, 'menu/carta.html', {
        'tragos': tragos, 
        'cart_count': obtener_carrito(request),
        'categoria_actual': 'cervezas'
    })

def categoria_botellas(request):
    # Botellas: Whisky, Vodka, Ron
    nombres = ['Whisky', 'Vodka', 'Ron']
    
    query = Q()
    for nombre in nombres:
        query |= Q(descripcion__icontains=nombre)
        
    # Filtramos por los nombres y EXCLUIMOS lo que tenga "Corona"
    tragos = Producto.objects.filter(query).exclude(descripcion__icontains='Corona')
    
    return render(request, 'menu/carta.html', {
        'tragos': tragos, 
        'cart_count': obtener_carrito(request),
        'categoria_actual': 'botellas'
    })

def categoria_sinalcohol(request):
    # Sin Alcohol: Coca-Cola, Sprite
    nombres = ['Coca-Cola', 'Sprite']
    
    query = Q()
    for nombre in nombres:
        query |= Q(descripcion__icontains=nombre)
        
    tragos = Producto.objects.filter(query)
    
    return render(request, 'menu/carta.html', {
        'tragos': tragos, 
        'cart_count': obtener_carrito(request),
        'categoria_actual': 'sinalcohol'
    })

# --- FUNCIONES DEL CARRITO (Sin cambios) ---
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'carta'))

def ver_carrito(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0
    for product_id, quantity in cart.items():
        try:
            product = Producto.objects.get(id_producto=product_id)
        except Producto.DoesNotExist:
            continue
        subtotal = product.precio * quantity
        total_price += subtotal
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'menu/carrito.html', {'items': items, 'total_price': total_price})
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        # Si la cantidad es mayor a 1, restamos uno (opcional)
        # O eliminamos el item completo directamente (lo más común)
        # Aquí haremos que elimine el item completo:
        del cart[product_id_str]
        
    request.session['cart'] = cart
    request.session.modified = True
    
    # Redirigimos de vuelta al carrito para ver el cambio
    return redirect('ver_carrito')