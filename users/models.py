from django.db import models
from django.contrib.auth.models import AbstractUser

# --- MODELOS LEGACY (Tus tablas SQL) ---
# Estos modelos representan las tablas que ya tenías en tu base de datos 'proyecto'.
# Usamos managed = False para que Django no intente modificarlas.

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    ubi_sucursal = models.CharField(max_length=40, blank=True, null=True)
    nom_sucursal = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sucursal'
    
    def __str__(self):
        return self.nom_sucursal

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nom_cliente = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'

    def __str__(self):
        return self.nom_cliente

class Trabajador(models.Model):
    id_trabajador = models.AutoField(primary_key=True)
    id_sucursal = models.ForeignKey(Sucursal, models.DO_NOTHING, db_column='id_sucursal', blank=True, null=True)
    nom_trabajador = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trabajador'

    def __str__(self):
        return self.nom_trabajador

# --- USUARIO DE DJANGO (Modificado) ---
# Este modelo extiende el usuario base de Django para agregar campos extra.

class User(AbstractUser):
    is_bartender = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # NUEVO CAMPO: Conecta el usuario de Django (login) con el Cliente SQL (pedidos)
    # Usamos OneToOneField porque un usuario de login debería ser un único cliente en la BD.
    cliente_asociado = models.OneToOneField(
        Cliente, 
        on_delete=models.SET_NULL, # Si se borra el cliente, no borramos el usuario
        null=True, 
        blank=True,
        related_name='usuario_django' # Permite acceder desde Cliente al usuario: cliente.usuario_django
    )

    def __str__(self):
        return self.username