from django.urls import path
from .views import InicioView
from . import views
# Petición asíncrona
from .peticiones_asyn.asyn_finanzas import *
# Formularios
from .views_form.modelo_dinero import *
from .views_form.modelo_deuda import crear_deuda, crear_prestamo, crear_tarjeta_credito
from .views_form.modelo_banco import crear_banco, crear_cuenta_bancaria
from .views_form.modelo_usuario import crear_usuario
# Formularios asíncronos
from .peticiones_asyn.asyn_forms import *
# Views inicio
from .views_inicio.modelo_dinero import *
from .views_inicio.modelo_bancos import *
urlpatterns = [
    # Inicio
    path('', InicioView.as_view(), name='inicio'),  # Vista de inicio



    # Finanzas
    path('deudas/', views.deudas, name='deudas'),

    path('ingresos/', IngresoInicioView.as_view(), name='ingresos'),
    path('egresos/', EgresoInicioView.as_view(), name='egresos'),

    path('cuentas/', CuentasBancaInicioView.as_view(), name='cuentas'),
    path('bancos/', BancoInicioView.as_view(), name='bancos'),

    path('prestamos/', views.prestamos, name='prestamos'),
    path('mi_cuenta/', views.mi_cuenta, name='mi_cuenta'),

    # Salir - Ingresar
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # Petición asíncrona
    path('api/cuentas/', listar_cuentas, name='listar_cuentas'), 
    path('api/usuarios/', listar_usuarios, name='listar_usuarios'), 
    # Petición asíncrona deudas
    path('api/deudas/', listar_deudas, name='listar_deudas'),
    path('api/tarjetas_credito/', listar_tarjetas_credito, name='listar_tarjetas_credito'),
    path('api/prestamos/', listar_prestamos, name='listar_prestamos'),
    # Petición asíncrona ingresos
    path('api/ingresos/', listar_ingresos, name='listar_ingresos'),
    # Petición asíncrona egresos
    path('api/egresos/', listar_egresos, name='listar_egresos'),
    # Petición asíncrona bancos
    path('api/bancos/', listar_bancos, name='listar_bancos'),


    # Petición asíncrona Inicio modelos
    path('api/informacion_ingreso/', InformacionIngresosView, name='informacion_ingresos'),  # Petición asíncrona ingresos
    path('api/informacion_egreso/', InformacionIngresosView, name='informacion_egresos'),  # Petición asíncrona egresos
    path('api/informacion_banco/', InformacionBancosView, name='informacion_banco'),  # Petición asíncrona bancos
    path('api/informacion_cuenta_bancaria/', InformacionCuentasBancariasView, name='informacion_cuenta_bancaria'),  # Petición asíncrona cuentas bancarias



    # Petición asíncrona transacciones

    

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
    # Formularios principales
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    # Fomularios crear rapido
    path('api/crear_rapido_ingreso/', crear_ingreso_rapido, name='crear_rapido_ingreso'),
    path('api/crear_rapido_egreso/', crear_egreso_rapido, name='crear_rapido_egreso'),


    # Eliminar registros
    path('api/eliminar_ingreso/<int:pk>/', eliminar_ingreso, name='eliminar_ingreso'),
    path('api/eliminar_egreso/<int:pk>/', eliminar_egreso, name='eliminar_egreso'),


    # Formularios editables
    path('api/editar_ingreso/<int:pk>/', editar_ingreso, name='editar_ingreso'),
    path('api/editar_egreso/<int:pk>/', editar_egreso, name='editar_egreso'),
    

    # Cargar registros
    path('api/cargar_registros_ingresos/<int:pk>/', cargar_registros_ingresos, name='cargar_registros_ingresos'),
    path('api/cargar_registros_egresos/<int:pk>/', cargar_registros_egresos, name='cargar_registros_egresos'),
    

    # Buscar dinámica 
    path('api/buscar_dinamica_ingresos/', BuscarIngresosView.as_view(), name='buscar_dinamica_ingresos'),
    path('api/buscar_dinamica_egresos/', BuscarEgresosView.as_view(), name='buscar_dinamica_egresos'),
 



    # Formularios async
    path('api/buscar_dinamica_cuentas/', ObtenerCuentasicontainsView.as_view(), name='buscar_dinamica_cuentas'),
    path('api/buscar_dinamica_usuarios/', ObtenerUsuariosicontainsView.as_view(), name='buscar_dinamica_usuarios'),

    # Formularios async deudas
    path('api/buscar_dinamica_deudas/', ObtenerDeudasicontainsView.as_view(), name='buscar_dinamica_deudas'),
    path('api/buscar_dinamica_tarjetas_credito/', ObtenerTarjetasCreditoicontainsView.as_view(), name='buscar_dinamica_tarjetas_credito'),
    path('api/buscar_dinamica_prestamos/', ObtenerPrestamosicontainsView.as_view(), name='buscar_dinamica_prestamos'),
    path('api/buscar_dinamica_bancos/', ObtenerBancosicontainsView.as_view(), name='buscar_dinamica_bancos'),

]