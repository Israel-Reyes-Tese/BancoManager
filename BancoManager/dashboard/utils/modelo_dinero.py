from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..modelo_dinero.models_dinero import Ingreso
from django.db.models import Q
from django.utils import timezone


def BuscarInformacionFechasView(request, modelo, values=(), retorno_json=True):
    query = request.GET.get('query', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    modelo_principal = modelo.objects.filter(usuario=request.user)
    if query:
        modelo_principal = modelo_principal.filter(
            Q(descripcion__icontains=query) |
            Q(fuente__icontains=query)
        )
    if fecha_desde:
        modelo_principal = modelo_principal.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        modelo_principal = modelo_principal.filter(fecha__lte=fecha_hasta)
    modelo_list = list(modelo_principal.values(*values))
    # Transformar el nombre del modelo a algo más amigable
    modelo = modelo.__name__.lower()
    if retorno_json:
        return JsonResponse({f'{modelo}': modelo_list})
    else:
        return modelo_list        









