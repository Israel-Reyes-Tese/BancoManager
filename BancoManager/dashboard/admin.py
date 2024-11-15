from django.contrib import admin
from .modelo_banco.models_banco import Banco
from .modelo_dinero.models_dinero import CuentaBancaria, Ingreso, Egreso
from .modelo_deudas.models_deudas import Deuda, TarjetaCredito, Prestamo


from .modelo_utils.modelo_inter import *
from .modelo_auditlog.modelo_auditlog import *

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')
    search_fields = ('nombre', 'direccion')
    list_filter = ('nombre',)
    ordering = ('nombre',)
    list_select_related = True
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        for banco in queryset:
            banco.verified = True  # Suponiendo que hay un campo llamado 'verified'
            banco.save()
        self.message_user(request, "Selected banks have been verified.")
    mark_as_verified.short_description = "Mark selected banks as verified"

@admin.register(CuentaBancaria)
class CuentaBancariaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numeroCuenta', 'tipoCuenta', 'banco', 'usuario', 'saldoActual')
    search_fields = ('nombre', 'numeroCuenta', 'usuario__email')
    list_filter = ('tipoCuenta', 'banco')
    ordering = ('nombre',)
    readonly_fields = ('saldoInicial', 'saldoActual')  # Assuming these fields should be read-only
    list_select_related = True
    autocomplete_fields = ('usuario',)
    actions = ['reset_account_balance']

    def reset_account_balance(self, request, queryset):
        for cuenta in queryset:
            cuenta.saldoActual = 0  # Reset balance
            cuenta.save()
        self.message_user(request, "Selected accounts have been reset to zero balance.")
    reset_account_balance.short_description = "Reset balance for selected accounts"

    def get_queryset(self, request):
        """Customize queryset to show only related accounts for the current user in the admin."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)  # Filter by logged-in user

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('cantidad', 'fecha', 'fuente', 'cuenta', 'descripcion', 'usuario')
    search_fields = ('fuente', 'cantidad', 'usuario__email')
    list_filter = ('fecha', 'cuenta__banco')
    ordering = ('-fecha',)
    date_hierarchy = 'fecha'
    list_select_related = True

@admin.register(Egreso)
class EgresoAdmin(admin.ModelAdmin):
    list_display = ('cantidad', 'fecha', 'proposito', 'cuenta', 'usuario')
    search_fields = ('proposito', 'cantidad', 'usuario__email')
    list_filter = ('fecha', 'cuenta__banco')
    ordering = ('-fecha',)
    date_hierarchy = 'fecha'
    list_select_related = True

@admin.register(Deuda)
class DeudaAdmin(admin.ModelAdmin):
    list_display = ('usuario_deudor', 'monto', 'tipo_deuda', 'fecha_creacion', 'estado')
    search_fields = ('usuario_deudor__email', 'monto', 'descripcion')
    list_filter = ('tipo_deuda', 'estado', 'fecha_creacion')
    ordering = ('-fecha_creacion',)
    readonly_fields = ('fecha_creacion',)  # Assuming this cannot be changed after creation
    date_hierarchy = 'fecha_creacion'
    list_select_related = True
    autocomplete_fields = ('usuario_deudor',)  # Assuming we want autocomplete for user

@admin.register(TarjetaCredito)
class TarjetaCreditoAdmin(admin.ModelAdmin):
    list_display = ('numero_tarjeta', 'nombre_titular', 'fecha_vencimiento', 'limite')
    search_fields = ('numero_tarjeta', 'nombre_titular')
    list_filter = ('fecha_vencimiento',)
    ordering = ('-fecha_vencimiento',)
    list_select_related = True

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('monto_total', 'tasa_interes', 'fecha_inicio', 'usuario_prestamista')
    search_fields = ('monto_total', 'usuario_prestamista__email')
    list_filter = ('fecha_inicio',)
    ordering = ('-fecha_inicio',)
    list_select_related = True