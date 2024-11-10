from django.http import JsonResponse
from ..modelo_dinero.models_dinero import *  # Importa el modelo 
# Modelo usuario
from django.conf import settings
from usuario.models import usuario
# Modelo deuda
from ..modelo_deudas.models_deudas import *
# Modelo cuentas
from ..modelo_banco.models_banco import *

from django.views import View

class ObtenerCuentasicontainsView(View):
   def get(self, request):
        query = request.GET.get('q', '')
        cuentas = CuentaBancaria.objects.filter(usuario=request.user, nombre__icontains=query)
        
        cuentas_data = [{'id': cuenta.id, 'nombre': cuenta.nombre} for cuenta in cuentas]
        return JsonResponse(cuentas_data, safe=False)
   

# Usuarios
class ObtenerUsuariosicontainsView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        usuarios = usuario.objects.filter(username__icontains=query)
        
        usuarios_data = [{'id': usuario.id, 'nombre': usuario.username} for usuario in usuarios]
        return JsonResponse(usuarios_data, safe=False)
    

# Deudas
class ObtenerDeudasicontainsView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        deudas = Deuda.objects.filter(usuario=request.user, nombre__icontains=query)
        
        deudas_data = [{'id': deuda.id, 'nombre': deuda.nombre} for deuda in deudas]
        return JsonResponse(deudas_data, safe=False)
    
class ObtenerTarjetasCreditoicontainsView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        tarjetas = CuentaBancaria.objects.filter(usuario=request.user, nombre__icontains=query)
        tarjetas_data = [{'id': tarjeta.id, 'nombre': tarjeta.nombre} for tarjeta in tarjetas]
        return JsonResponse(tarjetas_data, safe=False)
    

# Prestamos
class ObtenerPrestamosicontainsView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        prestamos = Prestamo.objects.filter(usuario_prestamista=request.user, descripcion__icontains=query)
        
        prestamos_data = [{'id': prestamo.id, 'nombre': prestamo.descripcion} for prestamo in prestamos]
        return JsonResponse(prestamos_data, safe=False)
    
# Bancos 
class ObtenerBancosicontainsView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        bancos = Banco.objects.filter(nombre__icontains=query)
        
        bancos_data = [{'id': banco.id, 'nombre': banco.nombre} for banco in bancos]
        return JsonResponse(bancos_data, safe=False)
    