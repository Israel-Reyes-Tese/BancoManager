from ..forms.modelo_banco import BancoForm, CuentaBancariaForm
from django.contrib.auth.decorators import login_required

from .funciones_forms_views import guardar_formulario_post, validar_inconsistencias


@login_required
def crear_banco(request):
    return guardar_formulario_post(BancoForm, request, 'Banco', 'crear_banco', 'banco')


@login_required
def crear_cuenta_bancaria(request):
    return guardar_formulario_post(CuentaBancariaForm, request, 'Cuenta Bancaria', 'crear_cuenta_bancaria', 'cuenta_bancaria')
