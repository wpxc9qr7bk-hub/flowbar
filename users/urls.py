from django.urls import path
from .views import SignUpView, login_success, perfil, historial_pedidos # <--- Asegúrate de importar la vista

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('redirect/', login_success, name='login_success'),
    path('profile/', perfil, name='perfil'),
    
    # ESTA ES LA RUTA QUE FALTA O NO SE HA LEÍDO:
    path('history/', historial_pedidos, name='historial_pedidos'),
]