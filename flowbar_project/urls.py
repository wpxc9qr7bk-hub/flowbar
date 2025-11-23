from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 1. Rutas de Login/Logout/Reset (Las dejamos bajo 'accounts')
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 2. Rutas de Registro (Las ponemos bajo 'users/') <--- CAMBIO AQUÍ
    path('users/', include('users.urls')), 
    
    # Modulo de Pedidos
    path('orders/', include('orders.urls')), 
    
    # Portada del sitio (Carta)
    path('', include('menu.urls')), 
]