from django.urls import path
from .views import InicioView
from . import views
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
]