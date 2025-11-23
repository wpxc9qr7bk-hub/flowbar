from django.db import models

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto'

    def __str__(self):
        return self.descripcion or "Producto sin nombre"
