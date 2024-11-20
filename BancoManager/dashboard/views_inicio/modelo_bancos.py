# views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from ..modelo_banco.models_banco import CuentaBancaria, Banco  # Importar modelos necesarios


from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.conf import settings

from ..views import InicioHelper
# +=======================================================================================+
# | __    __  .___________. __   __           _______.                                    |
# ||  |  |  | |           ||  | |  |         /       |                                    |
# ||  |  |  | `---|  |----`|  | |  |        |   (----`                                    |
# ||  |  |  |     |  |     |  | |  |         \   \                                        |
# ||  `--'  |     |  |     |  | |  `----..----)   |                                       |
# | \______/      |__|     |__| |_______||_______/                                        |
# |                                                                                       |
# | _______  __    __  .__   __.   ______  __    ______   .__   __.  _______      _______.|
# ||   ____||  |  |  | |  \ |  |  /      ||  |  /  __  \  |  \ |  | |   ____|    /       ||
# ||  |__   |  |  |  | |   \|  | |  ,----'|  | |  |  |  | |   \|  | |  |__      |   (----`|
# ||   __|  |  |  |  | |  . `  | |  |     |  | |  |  |  | |  . `  | |   __|      \   \    |
# ||  |     |  `--'  | |  |\   | |  `----.|  | |  `--'  | |  |\   | |  |____ .----)   |   |
# ||__|      \______/  |__| \__|  \______||__|  \______/  |__| \__| |_______||_______/    |
# +=======================================================================================+
from ..utils.generales import *
# +===========================================================================================+
# |.______    __    __       _______.  ______       __    __   _______  _______       ___     |
# ||   _  \  |  |  |  |     /       | /  __  \     |  |  |  | |   ____||       \     /   \    |
# ||  |_)  | |  |  |  |    |   (----`|  |  |  |    |  |  |  | |  |__   |  .--.  |   /  ^  \   |
# ||   _  <  |  |  |  |     \   \    |  |  |  |    |  |  |  | |   __|  |  |  |  |  /  /_\  \  |
# ||  |_)  | |  `--'  | .----)   |   |  `--'  '--. |  `--'  | |  |____ |  '--'  | /  _____  \ |
# ||______/   \______/  |_______/     \_____\_____\ \______/  |_______||_______/ /__/     \__\|
# +===========================================================================================+
class BuscarBancosView(LoginRequiredMixin, View):
    def get(self, request):
        return BuscarInformacion(request, Banco, values=('id', 'nombre'), retorno_json=True, campos_busqueda=('nombre',))
    
class BuscarCuentasBancariasView(LoginRequiredMixin, View):
    def get(self, request):
        return BuscarInformacion(request, CuentaBancaria, values=('id', 'nombre'), retorno_json=True, campos_busqueda=('nombre','numeroCuenta', 'banco__nombre', 'tipoCuenta', 'saldo'))
# +===========================================================================================================+
# | __  .__   __.  _______   ______   .______      .___  ___.      ___        ______  __    ______   .__   __.|
# ||  | |  \ |  | |   ____| /  __  \  |   _  \     |   \/   |     /   \      /      ||  |  /  __  \  |  \ |  ||
# ||  | |   \|  | |  |__   |  |  |  | |  |_)  |    |  \  /  |    /  ^  \    |  ,----'|  | |  |  |  | |   \|  ||
# ||  | |  . `  | |   __|  |  |  |  | |      /     |  |\/|  |   /  /_\  \   |  |     |  | |  |  |  | |  . `  ||
# ||  | |  |\   | |  |     |  `--'  | |  |\  \----.|  |  |  |  /  _____  \  |  `----.|  | |  `--'  | |  |\   ||
# ||__| |__| \__| |__|      \______/  | _| `._____||__|  |__| /__/     \__\  \______||__|  \______/  |__| \__||
# |                                                                                                           |
# |.______        ___      .__   __.   ______   ______                                                        |
# ||   _  \      /   \     |  \ |  |  /      | /  __  \                                                       |
# ||  |_)  |    /  ^  \    |   \|  | |  ,----'|  |  |  |                                                      |
# ||   _  <    /  /_\  \   |  . `  | |  |     |  |  |  |                                                      |
# ||  |_)  |  /  _____  \  |  |\   | |  `----.|  `--'  |                                                      |
# ||______/  /__/     \__\ |__| \__|  \______| \______/                                                       |
# +===========================================================================================================+
def InformacionBancosView(request, retorno_json=True, modelo_principal=""):
    helper = InicioHelper()
    bancos = helper.obtener_bancos(formato_query=False)
    bancos_list = list(bancos.values('id', 'nombre'))
    if retorno_json:
        return JsonResponse({'bancos': bancos_list,
                             'modelo_principal': modelo_principal})
    else:
        return bancos_list

def InformacionCuentasBancariasView(request, retorno_json=True, modelo_principal=""):
    helper = InicioHelper()
    modelo_principal = "Cuenta_bancaria"
    cuentas = helper.obtener_cuentas_bancarias(request.user, formato_query=False)
    # Data extra de apoyo
    total_ingresos, total_egresos = helper.obtener_totales_ingresos_egresos(request.user) 
    ingresos_recientes, egresos_recientes = helper.obtener_transacciones_recientes(request.user, formato_query=False)
    #     $('#resumen-rapido').text(`${data.cuentas.length} cuentas, ${data.tarjetas_credito.length} tarjeta(s) de crédito, ${data.prestamos.length} préstamo(s) activos.`);
    tarjetas_credito = helper.obtener_tarjetas_credito(request.user, formato_query=False)
    prestamos = helper.obtener_prestamos(request.user, formato_query=False)
    deudas = helper.obtener_deudas(request.user, formato_query=False)

    # Graficas
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
    # Preparar el contexto para el template
    context = {
        "usuario": request.user.username,
        "cuentas": cuentas,
        "modelo_principal": modelo_principal,
        "deudas": deudas,
        # DATOS DE APOYO
        "total_cuenta_bancaria": total_ingresos,
        "cuenta_bancaria_recientes": ingresos_recientes,
        "tarjetas_credito": tarjetas_credito,
        "prestamos": prestamos,
        'cuenta_bancaria_graficables': ingresos_graficables,


    }
    
    if retorno_json:
        return JsonResponse(context)
    else:
        return cuentas



class BancoInicioView(LoginRequiredMixin, View):
    template_name = 'finanzas/banco.html'
    login_url = '/login/'
    # Obtener el usuario autenticado
    def get(self, request, *args, **kwargs):
        try:
            bancos = Banco.objects.all()
            context = {
                "usuario": request.user.username,
                "bancos": bancos,
                "modelo_principal": "Banco"
            }
            print("Datos de bancos cargados correctamente.", context)
        except Exception as e:
            messages.error(request, _('Error al cargar la información de los bancos.'))
            return render(request, self.template_name, {})


class CuentasBancaInicioView(LoginRequiredMixin, View):
    template_name = 'finanzas/cuenta.html'
    login_url = '/login/'  # URL de redirección para usuarios no autenticados
    # Obtener el usuario autenticado
    def get(self, request, *args, **kwargs):
        try:
            helper = InicioHelper()
            cuentas_bancarias = helper.obtener_cuentas_bancarias(request.user, formato_query=False)
            # Data extra de apoyo
            total_ingresos, total_egresos = helper.obtener_totales_ingresos_egresos(request.user) 
            context = {
                "usuario": request.user.username,
                "cuentas_bancarias": cuentas_bancarias,
                "modelo_principal": "Cuenta_bancaria",
                "total_cuentas_bancarias": total_ingresos,
            }
            print("Datos de cuentas bancarias cargados correctamente.", context)
            return render(request, self.template_name, context)
        except Exception as e:
            messages.error(request, _('Error al cargar la información de las cuentas bancarias.'))
            return render(request, self.template_name, {})
