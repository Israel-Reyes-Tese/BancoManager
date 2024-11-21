from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from ..modelo_deudas.models_deudas import Deuda, Prestamo  # Importar modelos necesarios
from ..utils.generales import *  # Importar funciones utilitarias

from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.conf import settings

from ..views import InicioHelper


class BuscarDeudasView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return BuscarInformacionFechasView(request, Deuda, values=('id', 'monto', 'descripcion', 'fecha_vencimiento', 'tipo_deuda', 'usuario_deudor__username'), retorno_json=True)
    
class BuscarPrestamosView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return BuscarInformacionFechasView(request, Prestamo, values=('id', 'monto_total', 'descripcion', 'fecha_inicio', 'tasa_interes', 'usuario_prestamista__username'), retorno_json=True)


def InformacionDeudasView(request, retorno_json=True, modelo_principal="Deuda"):
    helper = InicioHelper()
    if retorno_json:
        deuda, total_deudas = helper.obtener_deudas(request.user, formato_query=False)
    else:
        deuda, total_deudas = helper.obtener_deudas(request.user, formato_query=True)
    context = {
        "usuario": request.user.username,

        "deudas": deuda,

        "total_deuda": total_deudas,
        
        "modelo_principal": modelo_principal,
    }
    if retorno_json:
        return JsonResponse(context)
    else:
        return context

class DeudaInicioView(LoginRequiredMixin, View):
    template_name = 'finanzas/deudas.html'
    login_url = '/login/'  # URL de redirección para usuarios no autenticados
    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, InformacionDeudasView(request, retorno_json=False, modelo_principal="Deuda"))

        except Exception as e:
            messages.error(request, _("Ocurrió un error al cargar las deudas."))
            print(f"Error en la vista DeudaInicioView: {e}")  # Registro del error
            return render(request, self.template_name)  # Renderiza sin datos si ocurre un error
        
class PrestamoInicioView(LoginRequiredMixin, View):
    template_name = 'finanzas/prestamos.html'
    login_url = '/login/'  # URL de redirección para usuarios no autenticados
    def get(self, request, *args, **kwargs):
        try:
            context = InformacionDeudasView(request, retorno_json=False, modelo_principal="Prestamo")
            return render(request, self.template_name, context)

        except Exception as e:
            messages.error(request, _("Ocurrió un error al cargar los préstamos."))
            print(f"Error en la vista PrestamoInicioView: {e}")  # Registro del error
            return render(request, self.template_name)  # Renderiza sin datos si ocurre un error
