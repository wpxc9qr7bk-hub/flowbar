from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from orders.models import Pedidos, DetallePedido
from users.models import Cliente # Importamos el modelo Cliente
from orders.models import Pedidos, DetallePedido

# Vista de Registro MEJORADA
class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm 
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        # 1. Guardamos el usuario de Django (auth_user)
        self.object = form.save()
        
        # 2. Creamos un Cliente en la tabla SQL (cliente) con el mismo nombre
        nuevo_cliente_sql = Cliente.objects.create(
            nom_cliente=self.object.username
        )
        
        # 3. Los vinculamos
        self.object.cliente_asociado = nuevo_cliente_sql
        self.object.save()
        
        return super().form_valid(form)

# ... (login_success y perfil siguen igual) ...
@login_required
def login_success(request):
    user = request.user
    es_bartender = getattr(user, 'is_bartender', False)
    if es_bartender or user.is_staff:
        return redirect('panel_bartender')
    return redirect('carta')

@login_required
def perfil(request):
    return render(request, 'users/perfil.html', {'user': request.user})

# Vista de Historial CORREGIDA (Ahora es privada)
@login_required
def historial_pedidos(request):
    try:
        user = request.user
        cliente_actual = None
        
        # 1. Intentar obtener el cliente vinculado (usando el nombre de relación correcto)
        # Si en models.py definiste related_name='usuario_django', la relación inversa desde User es 'cliente_asociado'
        if hasattr(user, 'cliente_asociado'):
            cliente_actual = user.cliente_asociado

        # 2. Si no tiene vínculo, intentamos buscar un cliente con el mismo nombre
        if not cliente_actual:
            cliente_actual = Cliente.objects.filter(nom_cliente=user.username).first()
            
            # Si lo encontramos, lo vinculamos para el futuro
            if cliente_actual:
                user.cliente_asociado = cliente_actual
                user.save()

        # 3. Si AÚN no tiene cliente, LO CREAMOS AHORA MISMO
        if not cliente_actual:
            cliente_actual = Cliente.objects.create(nom_cliente=user.username)
            user.cliente_asociado = cliente_actual
            user.save()

        # 4. Buscamos los pedidos de este cliente
        mis_pedidos = Pedidos.objects.filter(id_cliente=cliente_actual).order_by('-fecha_hora')
        
        historial = []
        for p in mis_pedidos:
            detalles = DetallePedido.objects.filter(id_pedido=p)
            total = sum(d.id_producto.precio * d.cantidad for d in detalles)
            esta_listo = (p.estado == 'LISTO')
            estado_texto = "Listo para retirar" if esta_listo else "En preparación"
            
            historial.append({
                'pedido': p,
                'detalles': detalles,
                'total': total,
                'estado': estado_texto,
                'esta_listo': esta_listo
            })
            
    except Exception as e:
        print(f"Error al cargar historial: {e}")
        historial = []

    return render(request, 'users/historial.html', {'historial': historial})