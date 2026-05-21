from django.contrib import admin
from .models import Cliente, Producto, Pedido, DetallePedido

#cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono')

#producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')

#pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha', 'estado', 'total')

#detalle pedido
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario',)
    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Subtotal'
