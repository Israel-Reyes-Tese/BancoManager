from ..forms.modelo_banco import BancoForm, CuentaBancariaForm
from ..modelo_banco.models_banco import Banco, CuentaBancaria

from django.contrib.auth.decorators import login_required

from .funciones_forms_views import guardar_formulario_post, validar_inconsistencias

from django.http import JsonResponse

def cargar_registros_cuenta_bancaria(request, pk):
    registros = CuentaBancaria.objects.filter(usuario=request.user, pk=pk)
    # Validar que el usuario sea el dueño del registro y que tenga el menos una consulta
    if not registros:
        return JsonResponse({'success': False})
    else:
        lista_registros = []
        for registro in registros:
            lista_registros.append({
                'id': registro.id,
                'nombre': registro.nombre,
                'numeroCuenta': registro.numeroCuenta,
                'tipoCuenta': registro.tipoCuenta,
                'afilacion': registro.afilacion,
                'colorIdentificacion': registro.colorIdentificacion,
                'saldoInicial': registro.saldoInicial,
                'saldoActual': registro.saldoActual,
                'banco': registro.banco.nombre,
                'cvc': registro.cvc,
                'fechaVencimiento': registro.fechaVencimiento,
                'usuario': registro.usuario.id,
                'modelo_principal': 'CuentaBancaria',
            })
        return JsonResponse({
            'success': True,
            'data': lista_registros
        }, safe=False)

@login_required
def crear_banco(request):
    return guardar_formulario_post(BancoForm, request, 'Banco', 'crear_banco', 'banco')


@login_required
def crear_cuenta_bancaria(request):
    return guardar_formulario_post(CuentaBancariaForm, request, 'Cuenta Bancaria', 'crear_cuenta_bancaria', 'cuenta_bancaria')
