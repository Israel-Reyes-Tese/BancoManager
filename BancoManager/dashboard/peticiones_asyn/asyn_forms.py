from django.http import JsonResponse
from ..modelo_dinero.models_dinero import CuentaBancaria  # Importa el modelo 
from django.views import View

class ObtenerCuentasicontainsView(View):
   def get(self, request):
        query = request.GET.get('q', '')
        cuentas = CuentaBancaria.objects.filter(usuario=request.user, nombre__icontains=query)
        
        cuentas_data = [{'id': cuenta.id, 'nombre': cuenta.nombre} for cuenta in cuentas]
        return JsonResponse(cuentas_data, safe=False)