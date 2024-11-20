
# views.py
from .funciones_forms_views import *

from ..forms.modelo_banco import BancoForm, CuentaBancariaForm
from ..modelo_banco.models_banco import Banco, CuentaBancaria

from django.contrib.auth.decorators import login_required

from .funciones_forms_views import guardar_formulario_post, validar_inconsistencias

from django.http import JsonResponse
import datetime

# +===========================================================================================================+
def cargar_registros_banco(request, pk):
    registros = Banco.objects.all()
    # Validar que el usuario sea el dueño del registro y que tenga el menos una consulta
    if not registros:
        return JsonResponse({'success': False})
    else:
        lista_registros = []
        for registro in registros:
            lista_registros.append({
                'id': registro.id,
                'nombre': registro.nombre,
                'direccion': registro.direccion,
                'telefono': registro.telefono,
                'fechaIngreso': registro.fechaIngreso,
                'modelo': 'Banco',
            })
        return JsonResponse({
            'success': True,
            'data': lista_registros
        }, safe=False)

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
                'banco_id': registro.banco.id,
                'cvc': registro.cvc,
                'fechaVencimiento': registro.fechaVencimiento,
                'usuario': registro.usuario.username,
                'usuario_id': registro.usuario.id,
                'modelo': "Cuenta_bancaria",
            })
        return JsonResponse({
            'success': True,
            'data': lista_registros
        }, safe=False)
# +===========================================================================================================+


# Banco
@login_required
def crear_banco(request):
    return guardar_formulario_post(BancoForm, request, 'Banco', 'crear_banco', 'banco')

@login_required
def crear_banco_rapido(request):
    print("Crear banco rápido", request.POST)
    data_extra = {
        "nombre": request.POST.get('nombre'),
        'direccion': "-",
        "telefono": "-",
        "fechaIngreso": datetime.date.today(),
    } 
    return guardar_formulario_data_preterminada(Banco, request, 'Banco', data_extra)

@login_required
def editar_banco(request, pk):
    return editar_formulario_get_or_post(BancoForm, request, Banco, 'banco', 'Banco_Actualizado', pk , 'editar_banco')

@login_required
def eliminar_banco(request, pk):
    return eliminar_registro_Get_or_post(request, Banco, pk, 'eliminar_banco', 'Banco_Eliminado')




@login_required
def crear_cuenta_bancaria(request):
    return guardar_formulario_post(CuentaBancariaForm, request, 'Cuenta Bancaria', 'crear_cuenta_bancaria', 'cuenta_bancaria')

@login_required
def crear_cuenta_bancaria_rapido(request):
    print("Crear cuenta bancaria rápido", request.POST)
    # Transformar el banco a un objeto 
    banco = get_object_or_404(Banco, pk=request.POST.get('banco'))
    # Cuenta por defecto
    data_extra = {
        "nombre": request.POST.get('nombre'),
        'numeroCuenta': request.POST.get('numeroCuenta'),
        "tipoCuenta": request.POST.get('tipoCuenta'),
        "afilacion": request.POST.get('afilacion'),
        "colorIdentificacion": request.POST.get('colorIdentificacion'),
        "saldoInicial": request.POST.get('saldoInicial'),
        "saldoActual": request.POST.get('saldoActual'),
        "banco": banco,
        "cvc": request.POST.get('cvc'),
        "fechaVencimiento": request.POST.get('fechaVencimiento'),
        "usuario": request.user,
        "fechaIngreso": datetime.date.today(),
    } 
    return guardar_formulario_data_preterminada(CuentaBancaria, request, 'Cuenta_bancaria', data_extra)

@login_required
def editar_cuenta_bancaria(request, pk):
    return editar_formulario_get_or_post(CuentaBancariaForm, request, CuentaBancaria, 'cuenta_bancaria', 'Cuenta_bancaria', pk , 'editar_cuenta_bancaria')


@login_required
def eliminar_cuenta_bancaria(request, pk):
    return eliminar_registro_Get_or_post(request, CuentaBancaria, pk, 'eliminar_cuenta_bancaria', 'Cuenta_Bancaria_Eliminado')