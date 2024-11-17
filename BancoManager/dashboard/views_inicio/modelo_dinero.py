# views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from ..modelo_dinero.models_dinero import Ingreso, Egreso  # Importar modelos necesarios
from ..utils.modelo_dinero import *  # Importar funciones utilitarias

from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.conf import settings

from ..views import InicioHelper




class BuscarIngresosView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return BuscarInformacionFechasView(request, Ingreso, values=('id', 'cantidad', 'descripcion', 'fecha', 'fuente', 'cuenta__nombre'), retorno_json=True)
    
class BuscarEgresosView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return BuscarInformacionFechasView(request, Egreso, values=('id', 'cantidad', 'descripcion', 'fecha', 'proposito', 'cuenta__nombre'), retorno_json=True)


def InformacionIngresosView(request, retorno_json=True, modelo_principal=""):
    helper = InicioHelper()
    if retorno_json:
        total_ingresos, total_egresos = helper.obtener_totales_ingresos_egresos(request.user)
        ingresos_recientes, egresos_recientes = helper.obtener_transacciones_recientes(request.user, formato_query=False)
        # Obtener datos para gráficas y estadísticas
        ingresos_mensuales, egresos_mensuales = helper.obtener_datos_graficos_mes_actual(request.user, formato_query=False)
        ingresos_descripcion, egresos_descripcion = helper.filtrar_descripciones_unicas(request.user, formato_query=False)
        todos_ingresos, todos_egresos = helper.obtener_transacciones(request.user, formato_query=False)
    else:
        total_ingresos, total_egresos = helper.obtener_totales_ingresos_egresos(request.user)
        ingresos_recientes, egresos_recientes = helper.obtener_transacciones_recientes(request.user)
        # Obtener datos para gráficas y estadísticas
        ingresos_mensuales, egresos_mensuales = helper.obtener_datos_graficos_mes_actual(request.user)
        ingresos_descripcion, egresos_descripcion = helper.filtrar_descripciones_unicas(request.user)
        todos_ingresos, todos_egresos = helper.obtener_transacciones(request.user)

    # Obtener gastos e ingresos de los últimos 12 meses
    gastos_por_mes, ingresos_por_mes = helper.obtener_gastos_ingresos_por_mes(request.user)
    # Crear un diccionario para almacenar el total acumulado por mes
    gastos_acumulados = helper.calcular_acumulados_por_mes(gastos_por_mes)
    ingresos_acumulados = helper.calcular_acumulados_por_mes(ingresos_por_mes)
    # Preparar datos para las gráficas comparativas mensuales
    ingresos_graficables, egresos_graficables = helper.preparar_datos_graficas(ingresos_acumulados, gastos_acumulados)
    # Preparar datos para las gráficas ingresos por categoría
    ingresos_por_categoria_graficables = helper.calcular_ingresos_por_categoria(request.user)
    egresos_por_categoria_graficables = helper.calcular_egresos_por_categoria(request.user)
    # Obtener las cuentas del usuario
    cuentas = helper.obtener_cuentas(request.user, formato_query=False) 
    # Preparar el contexto para el template
    total_ingresos_mes, total_egresos_mes = helper.obtener_totales_ingresos_egresos_por_mes(request.user, formato_query=False)
    # Cuentas del ingreso y egreso
    cuentas_ingreso, cuentas_egreso = helper.obtener_cuentas_filtradas(request.user, formato_query=False)

    context = {
        "usuario": request.user.username,

        'total_ingreso': total_ingresos,
        'total_egreso': total_egresos,

        'ingreso_acumulados': total_ingresos_mes,
        'egreso_acumulados': total_egresos_mes,

        'todos_ingreso': todos_ingresos,
        'todos_egreso': todos_egresos,

        'ingreso_graficables': ingresos_graficables,
        'egreso_graficables': egresos_graficables,

        'ingreso_por_categoria_graficables': ingresos_por_categoria_graficables,
        'egreso_por_categoria_graficables': egresos_por_categoria_graficables,

        'ingreso_recientes': ingresos_recientes,
        'egreso_recientes': egresos_recientes,

        'ingreso_mensuales': ingresos_mensuales,
        'egreso_mensuales': egresos_mensuales,
        
        'categorias': ingresos_descripcion,
        'categorias_egreso': egresos_descripcion,

        "modelo_principal": modelo_principal,

        'cuentas': cuentas,

        'cuentas_ingreso': cuentas_ingreso,
        'cuentas_egreso': cuentas_egreso,
    }

    if retorno_json:
        return JsonResponse(context)
    else:
        return context

class IngresoInicioView(LoginRequiredMixin, View):
    template_name = 'finanzas/ingresos.html'
    login_url = '/login/'  # URL de redirección para usuarios no autenticados
    # Obtener el usuario autenticado
    def get(self, request, *args, **kwargs):
        try:
            context = InformacionIngresosView(request, retorno_json=False, modelo_principal="Ingreso")
            return render(request, self.template_name, context)

        except Exception as e:
            messages.error(request, _("Ocurrió un error al cargar los ingresos."))
            print(f"Error en la vista IngresoInicioView: {e}")  # Registro del error
            return render(request, self.template_name)  # Renderiza sin datos si ocurre un error
        

class EgresoInicioView(LoginRequiredMixin, View):
    template_name = 'finanzas/egresos.html'
    login_url = '/login/'  # URL de redirección para usuarios no autenticados
    # Obtener el usuario autenticado
    def get(self, request, *args, **kwargs):
        try:
            context = InformacionIngresosView(request, retorno_json=False, modelo_principal="Egreso")
            return render(request, self.template_name, context)

        except Exception as e:
            messages.error(request, _("Ocurrió un error al cargar los egresos."))
            print(f"Error en la vista EgresoInicioView: {e}")  # Registro del error
            return render(request, self.template_name)  # Renderiza sin datos si ocurre un error
