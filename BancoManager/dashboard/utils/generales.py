from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..modelo_banco.models_banco import *
from django.db.models import Q
from django.utils import timezone

from ..modelo_banco.models_banco import Banco, CuentaBancaria


def BuscarInformacion(request, modelo, values=(), retorno_json=True, campos_busqueda=()):
    query = request.GET.get('query', '')
    modelo_principal = modelo.objects.filter(usuario=request.user)
    if query:
        for campo in campos_busqueda:
            modelo_principal = modelo_principal.filter(
                Q(**{campo: query})
            )
    modelo_list = list(modelo_principal.values(*values))
    # Transformar el nombre del modelo a algo más amigable
    modelo = modelo.__name__.lower()
    if retorno_json:
        return JsonResponse({f'{modelo}': modelo_list})
    else:
        return modelo_list