from django.urls import path
from . import views

urlpatterns = [
    # Rutas de Categorías
    path('', views.carta, name='carta'),             # Todos
    path('tragos/', views.categoria_tragos, name='cat_tragos'),
    path('cervezas/', views.categoria_cervezas, name='cat_cervezas'),
    path('botellas/', views.categoria_botellas, name='cat_botellas'),     # Nueva
    path('sinalcohol/', views.categoria_sinalcohol, name='cat_sinalcohol'), # Nueva

    # Rutas funcionales
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'), # <--- NUEVA RUTA
]