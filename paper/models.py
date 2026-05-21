from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    telefono = models.CharField(max_length=20, blank=False, null=False)
    direccion = models.CharField(max_length=200, blank=False, null=False)
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Producto(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False   )

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    fecha = models.DateTimeField(auto_now_add=True)
    class Estado_choices(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_PROCESO = 'EN_PROCESO', 'En Proceso'
        ENTREGADO = 'ENTREGADO', 'Entregado'
        CANCELADO = 'CANCELADO', 'Cancelado'
    estado = models.CharField(max_length=20, choices=Estado_choices.choices, default=Estado_choices.PENDIENTE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=False, null=False)   

    def actualizar_total(self):
        """Actualiza el total del pedido sumando todos los subtotales de sus detalles"""
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
        self.save(update_fields=['total'])  # update_fields evita actualizar otros campos
        return total
    
    def __str__(self):
        return f'Pedido  {self.id} {self.cliente.nombre} para {self.estado}'
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(blank=False, null=False   )
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False   )
   
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def save(self, *args, **kwargs):
        """Guarda el detalle y actualiza el total del pedido"""
        super().save(*args, **kwargs)
        # Actualizar el total del pedido después de guardar
        self.pedido.actualizar_total()

    def delete(self, *args, **kwargs):
        """Elimina el detalle y actualiza el total del pedido"""
        pedido = self.pedido
        super().delete(*args, **kwargs)
        pedido.actualizar_total()

    def __str__(self):
        return f'{self.cantidad} {self.producto.nombre} a {self.subtotal} '
    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'