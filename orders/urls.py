from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('status/<int:pedido_id>/', views.order_status, name='order_status'),
    
    # Nuevas rutas para el Bartender
    path('panel/', views.panel_bartender, name='panel_bartender'),
    path('listo/<int:pedido_id>/', views.marcar_listo, name='marcar_listo'),
    path('api/check_status/<int:pedido_id>/', views.check_order_status, name='check_status'),
]