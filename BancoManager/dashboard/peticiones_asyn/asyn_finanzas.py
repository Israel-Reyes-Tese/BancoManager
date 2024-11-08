from django.http import JsonResponse
from django.views import View

from ..modelo_banco.models_banco import CuentaBancaria  # Asegúrate de que la ruta sea correcta
from ..modelo_dinero.models_dinero import Ingreso, Egreso  # Asegúrate de que la ruta sea correcta
from ..modelo_deudas.models_deudas import Deuda  # Asegúrate de que la ruta sea correcta


from ..views import InicioHelper  # Asegúrate de importar la clase InicioHelper

def listar_cuentas(request):
    if request.method == 'GET':
        usuario = request.user  # Obtén el usuario autenticado
        cuentas = CuentaBancaria.objects.filter(usuario=usuario)  # Filtrar cuentas por usuario
        cuentas_data = []  # Lista para almacenar los datos de las cuentas

        for cuenta in cuentas:
            cuentas_data.append({
                'id': cuenta.id,
                "nombre": cuenta.nombre,
                'banco': cuenta.banco.nombre,
                'numeroCuenta': cuenta.numeroCuenta,
                'saldoActual': str(cuenta.saldoActual),  # Convertimos a string para JSON
                'tipoCuenta': cuenta.tipoCuenta,
                'afilacion': cuenta.afilacion,
                "colorIdentificacion": cuenta.colorIdentificacion,
                # Parte adicional
                'cvc': cuenta.cvc,
                'fechaVencimiento': cuenta.fechaVencimiento,

            
            
            })

        return JsonResponse({'cuentas': cuentas_data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_transacciones_mes(request):
    if request.method == 'GET':
        usuario = request.user  # Obtén el usuario autenticado
        helper = InicioHelper()  # Crea una instancia del helper
        
        # Llama a las funciones necesarias para obtener los totales
        total_ingresos, total_egresos = helper.obtener_totales_ingresos_egresos(usuario)
        top_fuentes_ingresos, top_propositos_egresos = helper.obtener_fuentes_propositos_comunes(request.user)
        top_fuentes_ingresos_lista = []
        top_propositos_egresos_lista = []
        # Adaptar la respuesta a una lista
        for fuente_ingresos in top_fuentes_ingresos:
            top_fuentes_ingresos_lista.append({
                "fuente" : fuente_ingresos['fuente'],
                "count" : fuente_ingresos['count']
                })
            

        for proposito_egresos in top_propositos_egresos:
            top_propositos_egresos_lista.append({
                "fuente" : proposito_egresos['proposito'],
                "count" : proposito_egresos['count']
                })

        print("Obtener transacciones del mes \n" + "Total ingresos",str(total_ingresos) + "\n" + "Total egresos", 
              str(total_egresos) + "\n" + "Top fuentes ingresos", str(top_fuentes_ingresos_lista) + "\n" + "Top fuentes egresos",str(top_propositos_egresos_lista))

        return JsonResponse({'total_ingresos': total_ingresos, 'total_egresos': total_egresos,
                             'top_fuentes_ingresos': top_fuentes_ingresos_lista, 'top_propositos_egresos': top_propositos_egresos_lista})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def RefrescarTablasTransacciones(request):
    if request.method == 'GET':
        helper = InicioHelper()
        usuario = request.user  # Obtén el usuario autenticado

        # Obtener todos los ingresos y egresos
        ingresos, egresos = helper.obtener_transacciones(usuario)
        # Convertir QuerySets a listas y unirlas
        egresos_list = list(egresos)
        ingresos_list = list(ingresos)
        transacciones = egresos_list + ingresos_list


        # Serializar datos
        transacciones_data = [{
            'fecha': transaccion.fecha.strftime('%Y-%m-%d'),
            'descripcion': transaccion.descripcion,
            'cantidad': str(transaccion.cantidad),
            'proposito': getattr(transaccion, 'proposito', getattr(transaccion, 'fuente', '')),
            'id': transaccion.id,
            'tipo': transaccion.tipo,
        } for transaccion in transacciones]

        return JsonResponse(transacciones_data, safe=False)
    

class FiltrarTransaccionesView(View):
    def get(self, request):
        categoria = request.GET.get('categoria', 'todas')  # Obtén la categoría del query
        helper = InicioHelper()
        usuario = request.user

        if categoria == 'todas':
            ingresos, egresos = helper.obtener_transacciones(usuario)
        else:
            ingresos = Ingreso.objects.filter(usuario=usuario, fuente=categoria)
            egresos = Egreso.objects.filter(usuario=usuario, proposito=categoria)

        # Convertir QuerySets a listas y unirlas
        egresos_list = list(egresos)
        ingresos_list = list(ingresos)
        transacciones = egresos_list + ingresos_list


        # Serializar datos
        transacciones_data = [{
            'fecha': transaccion.fecha.strftime('%Y-%m-%d'),
            'descripcion': transaccion.descripcion,
            'cantidad': str(transaccion.cantidad),
            'proposito': getattr(transaccion, 'proposito', getattr(transaccion, 'fuente', '')),
            'id': transaccion.id,
            'tipo': transaccion.tipo,
        } for transaccion in transacciones]

        return JsonResponse(transacciones_data, safe=False)
    
class OrdenarTransaccionesView(View):
    def get(self, request):
        orden = request.GET.get('orden', 'fecha')  # Orden por defecto
        tipo_orden = request.GET.get('tipo', 'asc')  # Tipo de orden (ascendente o descendente)
        helper = InicioHelper()
        usuario = request.user

        # Obtener todas las transacciones
        ingresos = Ingreso.objects.filter(usuario=usuario)
        egresos = Egreso.objects.filter(usuario=usuario)
        # Transformar la categoria a segun si es ingreso o egreso 

        if orden == 'categoria':
            orden_ingresos = 'fuente' if ingresos else 'fuente'
            orden_egresos = 'proposito' if egresos else 'proposito'
        else:
            orden_ingresos = orden
            orden_egresos = orden

        # Ordenar según el tipo y criterio
        if tipo_orden == 'asc':
            ingresos = ingresos.order_by(orden_ingresos)
            egresos = egresos.order_by(orden_egresos)

        else:
            ingresos = ingresos.order_by('-' + orden_ingresos)
            egresos = egresos.order_by('-' + orden_egresos)
        # Convertir QuerySets a listas y unirlas
        egresos_list = list(egresos)
        ingresos_list = list(ingresos)
        transacciones = egresos_list + ingresos_list

        # Serializar datos
        transacciones_data = [{
            'fecha': transaccion.fecha.strftime('%Y-%m-%d'),
            'descripcion': transaccion.descripcion,
            'cantidad': str(transaccion.cantidad),
            'proposito': getattr(transaccion, 'proposito', getattr(transaccion, 'fuente', '')),
            'id': transaccion.id,
            'tipo': transaccion.tipo,
        } for transaccion in transacciones]
        # Validar si el orden es tipo ordenar los datos finales
        if orden == 'tipo':
            if tipo_orden == 'asc':
                transacciones_data = sorted(transacciones_data, key=lambda x: x['tipo'])
            else:
                transacciones_data = sorted(transacciones_data, key=lambda x: x['tipo'], reverse=True)


                
        print("Order by", transacciones_data, "orden", orden)
        return JsonResponse(transacciones_data, safe=False)
    
# Vista de cuentas proximas a vencer
class RefrescarDeudasView(View):
    def get(self, request):
        helper = InicioHelper()
        deudas = helper.obtener_deudas_proximas(request.user)
        # Serializa datos similares al filtro
        deudas_data = [{
            'id': deuda.id,
            'descripcion': deuda.descripcion,
            'cantidad': str(deuda.monto),
            'fechaVencimiento': deuda.fecha_vencimiento.strftime('%Y-%m-%d'),
            'estado': deuda.estado,
            "tipo": deuda.tipo_deuda,
        } for deuda in deudas]

        return JsonResponse({'cuentas': deudas_data})


class FiltrarDeudasView(View):
    def get(self, request):
        estado = request.GET.get('estado', 'todas')
        helper = InicioHelper()
        deudas = helper.obtener_deudas_proximas(request.user)

        if estado != 'todas':
            if estado == "pendiente":
                estado = True
            else:
                estado = False
            deudas = deudas.filter(estado=estado)

        # Serializa los datos
        deudas_data = [{
            'id': deuda.id,
            'descripcion': deuda.descripcion,
            'cantidad': str(deuda.monto),
            'fechaVencimiento': deuda.fecha_vencimiento.strftime('%Y-%m-%d'),
            'estado': deuda.estado,
            "tipo": deuda.tipo_deuda,
        } for deuda in deudas]

        return JsonResponse({'cuentas': deudas_data})