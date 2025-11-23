from django.db import models

class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    
    # Claves foráneas
    id_sucursal = models.ForeignKey('users.Sucursal', models.DO_NOTHING, db_column='id_sucursal', blank=True, null=True)
    id_cliente = models.ForeignKey('users.Cliente', models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    
    id_trabajador = models.ForeignKey(
        'users.Trabajador', 
        models.DO_NOTHING, 
        db_column='id_trabajador', 
        blank=True, 
        null=True,
        related_name='pedidos'
    )
    
    fecha_hora = models.DateTimeField(blank=True, null=True)
    
    OPCIONES_PAGO = (
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
    )
    forma_pago = models.CharField(max_length=13, choices=OPCIONES_PAGO, blank=True, null=True)

    # Columna de estado
    OPCIONES_ESTADO = [
        ('PREPARACION', 'En Preparación'),
        ('LISTO', 'Listo para Retirar'),
        ('ENTREGADO', 'Entregado'),
    ]
    estado = models.CharField(max_length=20, choices=OPCIONES_ESTADO, default='PREPARACION')

    class Meta:
        managed = True
        db_table = 'pedidos'

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.estado}"


class DetallePedido(models.Model):
    # Asumimos que ya ejecutaste el script arreglar_db.py para tener la columna 'id'
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, db_column='id_pedido')
    id_producto = models.ForeignKey('menu.Producto', on_delete=models.CASCADE, db_column='id_producto')
    
    # Ahora 'cantidad' acepta valores nulos (null=True) y vacíos en formularios (blank=True)
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'detalle_pedido'


class Asignado(models.Model):
    # --- CORRECCIÓN AQUÍ ---
    # Agregamos null=True al campo id_pedido para permitir valores nulos
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, db_column='id_pedido', null=True) 
    # También lo aplicamos a otros campos por si acaso, para facilitar la migración si hay datos incompletos
    id_producto = models.ForeignKey('menu.Producto', on_delete=models.CASCADE, db_column='id_producto', null=True)
    id_trabajador = models.ForeignKey('users.Trabajador', on_delete=models.CASCADE, db_column='id_trabajador', null=True)

    class Meta:
        managed = True
        db_table = 'asignado'