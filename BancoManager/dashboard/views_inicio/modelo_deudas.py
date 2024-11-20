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


def InformacionDeudasView(request, retorno_json=True, modelo_principal=""):
    helper = InicioHelper()
    if retorno_json:
        total_deudas, total_prestamos = helper.obtener_totales_deudas_prestamos(request.user)
        deudas_recientes, prestamos_recientes = helper.obtener_transacciones_recientes(request.user, formato_query=False)
        deudas_mensuales, prestamos_mensuales = helper.obtener_datos_graficos_mes_actual(request.user, formato_query=False)
        deudas_descripcion, prestamos_descripcion = helper.filtrar_descripciones_unicas(request.user, formato_query=False)
        todas_deudas, todos_prestamos = helper.obtener_transacciones(request.user, formato_query=False)
    else:
        total_deudas, total_prestamos = helper.obtener_totales_deudas_prestamos(request.user)
        deudas_recientes, prestamos_recientes = helper.obtener_transacciones_recientes(request.user)
        deudas_mensuales, prestamos_mensuales = helper.obtener_datos_graficos_mes_actual(request.user)
        deudas_descripcion, prestamos_descripcion = helper.filtrar_descripciones_unicas(request.user)
        todas_deudas, todos_prestamos = helper.obtener_transacciones(request.user)

    gastos_por_mes, ingresos_por_mes = helper.obtener_gastos_ingresos_por_mes(request.user)
    gastos_acumulados = helper.calcular_acumulados_por_mes(gastos_por_mes)
    ingresos_acumulados = helper.calcular_acumulados_por_mes(ingresos_por_mes)
    ingresos_graficables, egresos_graficables = helper.preparar_datos_graficas(ingresos_acumulados, gastos_acumulados)
    ingresos_por_categoria_graficables = helper.calcular_ingresos_por_categoria(request.user)
    egresos_por_categoria_graficables = helper.calcular_egresos_por_categoria(request.user)
    cuentas = helper.obtener_cuentas(request.user, formato_query=False)
    total_ingresos_mes, total_egresos_mes = helper.obtener_totales_ingresos_egresos_por_mes(request.user, formato_query=False)
    cuentas_ingreso, cuentas_egreso = helper.obtener_cuentas_filtradas(request.user, formato_query=False)

    context = {
        "usuario": request.user.username,

        'total_ingreso': total_deudas,
        'total_egreso': total_prestamos,

        'ingreso_acumulados': total_ingresos_mes,
        'egreso_acumulados': total_egresos_mes,

        'todos_ingreso': todas_deudas,
        'todos_egreso': todos_prestamos,

        'ingreso_graficables': ingresos_graficables,
        'egreso_graficables': egresos_graficables,

        'ingreso_por_categoria_graficables': ingresos_por_categoria_graficables,
        'egreso_por_categoria_graficables': egresos_por_categoria_graficables,

        'ingreso_recientes': deudas_recientes,
        'egreso_recientes': prestamos_recientes,

        'ingreso_mensuales': deudas_mensuales,
        'egreso_mensuales': prestamos_mensuales,
        
        'categorias': deudas_descripcion,
        'categorias_egreso': prestamos_descripcion,

        "modelo_principal": modelo_principal,

        'cuentas': cuentas,

        'cuentas_ingreso': cuentas_ingreso,
        'cuentas_egreso': cuentas_egreso,
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
            context = InformacionDeudasView(request, retorno_json=False, modelo_principal="Deuda")
            return render(request, self.template_name, context)

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
