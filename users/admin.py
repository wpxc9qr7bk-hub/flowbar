from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cliente, Trabajador, Sucursal

# Configuración para ver tus campos personalizados en el Admin
class CustomUserAdmin(UserAdmin):
    model = User
    # Agregamos una sección "Información Adicional" con tus campos
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('is_bartender', 'avatar')}),
    )
    
    list_display = ['username', 'email', 'is_bartender', 'is_staff']

# Registramos el usuario con la configuración nueva
admin.site.register(User, CustomUserAdmin)

# Registramos las otras tablas
admin.site.register(Cliente)
admin.site.register(Trabajador)
admin.site.register(Sucursal)