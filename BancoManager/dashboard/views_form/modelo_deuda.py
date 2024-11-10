# views.py
from ..forms.modelo_deudas import TarjetaCreditoForm, PrestamoForm, DeudaForm
from django.contrib.auth.decorators import login_required

from .funciones_forms_views import guardar_formulario_post,guardar_formulario_post_sin_user, validar_inconsistencias


@login_required
def crear_tarjeta_credito(request):
    return guardar_formulario_post(TarjetaCreditoForm, request, 'Tarjeta de Crédito', 'crear_tarjeta_credito', 'tarjeta_credito')

@login_required
def crear_prestamo(request):
    return guardar_formulario_post_sin_user(PrestamoForm, request, 'Préstamo', 'crear_prestamo', 'prestamo')

@login_required
def crear_deuda(request):
    inconsistencias = validar_inconsistencias(request, 'Deuda')
    return guardar_formulario_post_sin_user(DeudaForm, request, 'Deuda', 'crear_deuda', 'deuda')


