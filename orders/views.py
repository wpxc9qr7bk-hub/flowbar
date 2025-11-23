from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# CORRECCIÓN: Importamos solo lo que existe.
from .models import Pedidos, DetallePedido
from menu.models import Producto
from users.models import Cliente, Trabajador
from .logic import assign_bartender_algorithm
from datetime import datetime
from django.db import transaction
from django.http import JsonResponse

@login_required
@transaction.atomic
def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('ver_carrito')
        
    user = request.user
    cliente_final = None

    # PASO 1: Intentar obtener el cliente ya asociado al usuario
    if user.cliente_asociado:
        cliente_final = user.cliente_asociado
        print(f"Usando cliente asociado existente: ID {cliente_final.id_cliente}")

    # PASO 2: Si no tiene asociación, buscar o crear
    else:
        print("Usuario sin cliente asociado. Iniciando búsqueda/creación...")
        
        # Buscamos si existe un cliente con el mismo nombre en la tabla 'cliente'
        cliente_existente = Cliente.objects.filter(nom_cliente=user.username).first()
        
        if cliente_existente:
            # Lo encontramos: Lo asociamos al usuario para la próxima vez
            cliente_final = cliente_existente
            user.cliente_asociado = cliente_final
            user.save() # GUARDAMOS LA RELACIÓN EN LA BD
            print(f"Cliente encontrado por nombre y vinculado: ID {cliente_final.id_cliente}")
        else:
            # No existe: Creamos uno nuevo
            cliente_final = Cliente.objects.create(nom_cliente=user.username)
            user.cliente_asociado = cliente_final
            user.save() # GUARDAMOS LA RELACIÓN EN LA BD
            print(f"Nuevo cliente creado y vinculado: ID {cliente_final.id_cliente}")

    # --- AQUÍ YA TENEMOS 'cliente_final' GARANTIZADO ---

    assigned_bartender = assign_bartender_algorithm()
    
    if not assigned_bartender:
        # Fallback de emergencia por si no hay bartenders
        assigned_bartender = Trabajador.objects.first()
    
    if not assigned_bartender:
         return render(request, 'orders/error.html', {'message': 'No hay personal disponible.'})

    # Guardamos el pedido usando el ID del cliente correcto
    nuevo_pedido = Pedidos.objects.create(
        id_cliente=cliente_final,  # <--- Usamos el objeto cliente recuperado/creado
        id_trabajador=assigned_bartender,
        fecha_hora=datetime.now(),
        forma_pago='Tarjeta',
        estado='PREPARACION'
    )

    # ... (resto del código: crear detalles, limpiar carrito, etc.)
    for product_id_str, quantity in cart.items():
        product = Producto.objects.get(id_producto=int(product_id_str))
        DetallePedido.objects.create(
            id_pedido=nuevo_pedido,
            id_producto=product,
            cantidad=quantity
        )
        
    del request.session['cart']
    request.session.modified = True
    
    return redirect('order_status', pedido_id=nuevo_pedido.id_pedido)

@login_required
def order_status(request, pedido_id):
    pedido = get_object_or_404(Pedidos, id_pedido=pedido_id)
    
    # Usamos la columna estado
    if pedido.estado == 'LISTO':
        return render(request, 'orders/status_listo.html', {'pedido': pedido})

    context = {
        'pedido': pedido,
        'bartender_name': pedido.id_trabajador.nom_trabajador,
        'pedido_id': pedido.id_pedido
    }
    return render(request, 'orders/status_pedido.html', context)

@login_required
def panel_bartender(request):
    if not request.user.is_staff and not getattr(request.user, 'is_bartender', False):
         return render(request, 'orders/error.html', {'message': 'Acceso denegado.'})
    
    try:
        trabajador = Trabajador.objects.get(nom_trabajador=request.user.username)
    except Trabajador.DoesNotExist:
        trabajador = Trabajador.objects.first()

    # Filtramos usando la columna estado
    mis_pedidos = Pedidos.objects.filter(
        id_trabajador=trabajador, 
        estado='PREPARACION'
    ).order_by('-fecha_hora')[:10]
    
    pedidos_con_detalle = []
    for p in mis_pedidos:
        detalles = DetallePedido.objects.filter(id_pedido=p)
        items = []
        for d in detalles:
            items.append(f"{d.cantidad}x {d.id_producto.descripcion}")
            
        pedidos_con_detalle.append({
            'info': p,
            'items': items,
            'hora': p.fecha_hora
        })

    return render(request, 'orders/panel_bartender.html', {
        'pedidos': pedidos_con_detalle,
        'trabajador': trabajador
    })

@login_required
def marcar_listo(request, pedido_id):
    pedido = get_object_or_404(Pedidos, id_pedido=pedido_id)
    pedido.estado = 'LISTO' # Actualizamos la columna
    pedido.save()
    return redirect('panel_bartender')

def check_order_status(request, pedido_id):
    pedido = Pedidos.objects.get(id_pedido=pedido_id)
    # Verificamos la columna
    return JsonResponse({'listo': (pedido.estado == 'LISTO')})