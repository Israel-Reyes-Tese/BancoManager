# views.py
from ..forms.modelo_dinero import IngresoForm, EgresoForm
from ..modelo_dinero.models_dinero import Ingreso, Egreso

from ..modelo_banco.models_banco import CuentaBancaria

from django.contrib.auth.decorators import login_required

from .funciones_forms_views import *

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime

@login_required
def crear_ingreso(request):
    return guardar_formulario_post(IngresoForm, request, 'Ingreso', 'crear_ingreso', 'ingreso')

@login_required
def crear_ingreso_rapido(request):
    print("Crear ingreso rápido", request.POST)
    # Transformar el cuenta a un objeto 
    cuenta = get_object_or_404(CuentaBancaria, pk=request.POST.get('cuenta'))

    # Cuenta por defecto
    data_extra = {
        "cantidad": request.POST.get('cantidad'),
        'cuenta': cuenta,
        "fuente": request.POST.get('fuente'),
        "descripcion": "Ingreso rápido",
        "fecha": datetime.date.today(),
        "usuario": request.user,
        "tipo": "Ingreso",
    } 
    return guardar_formulario_data_preterminada(Ingreso, request, 'Ingreso', data_extra)


@login_required
def crear_egreso(request):
    return guardar_formulario_post(EgresoForm, request, 'Egreso', 'crear_egreso', 'egreso')


# Editar ingreso


def cargar_registros_ingresos(request, pk):
    registros = Ingreso.objects.filter(usuario=request.user, pk=pk)
    # Validar que el usuario sea el dueño del registro y que tenga el menos una consulta
    if not registros:
        return JsonResponse({'success': False})
    else:
        lista_registros = []
        for registro in registros:
            lista_registros.append({
                'id': registro.id,
                'cantidad': registro.cantidad,
                'descripcion': registro.descripcion,
                'fecha': registro.fecha,
                'fuente': registro.fuente,
                'cuenta': registro.cuenta.id,
                'usuario': registro.usuario.id,
                'tipo': registro.tipo,
                'fechaIngreso': registro.fechaIngreso,
                'cuenta_nombre': registro.cuenta.nombre,
            })

        return JsonResponse({
            'success': True,
            'data': lista_registros
        }, safe=False)



@login_required
def editar_ingreso(request, pk):
    return editar_formulario_get_or_post(IngresoForm, request, Ingreso, 'ingreso', 'Ingreso_Actualizado', pk , 'editar_ingreso')


@login_required
def actualizar_ingreso(request, pk):
    return editar_formulario_get_or_post(IngresoForm, request, Ingreso, 'ingreso', 'Ingreso_Actualizado', pk , 'editar_ingreso')


@login_required
def eliminar_ingreso(request, pk):
    return eliminar_registro_Get_or_post(request, Ingreso, pk, 'eliminar_ingreso', 'Ingreso_Eliminado')