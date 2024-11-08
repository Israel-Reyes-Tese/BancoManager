from django.urls import path
from .views import InicioView
from . import views
# Petición asíncrona
from .peticiones_asyn.asyn_finanzas import *
# Formularios
from .views_form.modelo_dinero import crear_ingreso, crear_egreso
from .views_form.modelo_deuda import crear_deuda, crear_prestamo, crear_tarjeta_credito
from .views_form.modelo_banco import crear_banco, crear_cuenta_bancaria
# Formularios asíncronos
from .peticiones_asyn.asyn_forms import ObtenerCuentasicontainsView


urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),  # Vista de inicio
    # Finanzas
    path('deudas/', views.deudas, name='deudas'),
    path('ingresos/', views.ingresos, name='ingresos'),
    path('egresos/', views.egresos, name='egresos'),
    path('bancos/', views.bancos, name='bancos'),
    path('prestamos/', views.prestamos, name='prestamos'),
    path('cuentas/', views.cuentas, name='cuentas'),
    path('mi_cuenta/', views.mi_cuenta, name='mi_cuenta'),
    # Salir - Ingresar
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # Petición asíncrona
    path('api/cuentas/', listar_cuentas, name='listar_cuentas'),  # Ruta para la API
    path('api/transacciones_mes/', obtener_transacciones_mes, name='obtener_transacciones_mes'),  # Nueva ruta
    path('api/refrescar_tablas_transacciones/', RefrescarTablasTransacciones, name='refrescar_tablas_transacciones'),
    # Transacciones ...
    path('api/filtrar_transacciones/', FiltrarTransaccionesView.as_view(), name='filtrar_transacciones'),
    path('api/ordenar_transacciones/', OrdenarTransaccionesView.as_view(), name='ordenar_transacciones'),
    # Cuenta a vencer
    path('api/refrescar_deudas/', RefrescarDeudasView.as_view(), name='refrescar_deudas'),
    path('api/filtrar_deudas/', FiltrarDeudasView.as_view(), name='filtrar_deudas'),
    # Formularios
    path('crear_ingreso/', crear_ingreso, name='crear_ingreso'),
    path('crear_egreso/', crear_egreso, name='crear_egreso'),
    path('crear_deuda/', crear_deuda, name='crear_deuda'),
    path('crear_prestamo/', crear_prestamo, name='crear_prestamo'),
    path('crear_tarjeta_credito/', crear_tarjeta_credito, name='crear_tarjeta_credito'),
    path('crear_banco/', crear_banco, name='crear_banco'),	
    path('crear_cuenta_bancaria/', crear_cuenta_bancaria, name='crear_cuenta_bancaria'),
    # Formularios async
    path('api/buscar_dinamica_cuentas/', ObtenerCuentasicontainsView.as_view(), name='buscar_dinamica_cuentas'),

]