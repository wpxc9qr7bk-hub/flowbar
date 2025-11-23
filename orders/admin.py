from django.contrib import admin
from .models import Pedidos, DetallePedido, Asignado

admin.site.register(Pedidos)
admin.site.register(DetallePedido)
admin.site.register(Asignado)