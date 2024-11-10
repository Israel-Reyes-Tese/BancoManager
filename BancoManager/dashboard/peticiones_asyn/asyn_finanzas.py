from django.http import JsonResponse
from django.views import View

from ..modelo_banco.models_banco import CuentaBancaria, Banco # Asegúrate de que la ruta sea correcta
from ..modelo_dinero.models_dinero import Ingreso, Egreso  # Asegúrate de que la ruta sea correcta
from ..modelo_deudas.models_deudas import Deuda, Prestamo, TarjetaCredito  # Asegúrate de que la ruta sea correcta
# Usuario
from django.conf import settings
from usuario.models import usuario

from ..views import InicioHelper  # Asegúrate de importar la clase InicioHelper
# Cuentas
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

def listar_bancos(request):
    if request.method == 'GET':
        usuario = request.user  # Obtén el usuario autenticado
        bancos = Banco.objects.all()  # Obtén todos los bancos
        bancos_data = []  # Lista para almacenar los datos de los bancos

        for banco in bancos:
            bancos_data.append({
                'id': banco.id,
                'nombre': banco.nombre,
                'direccion': banco.direccion,
                'telefono': banco.telefono,
            })

        return JsonResponse({'bancos': bancos_data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Funciones de cuentas
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
    

# Usuarios
def listar_usuarios(request):
    if request.method == 'GET':
        usuario_OBJ = usuario.objects.all()  # Obtén todos los usuarios
        usuarios_data = []  # Lista para almacenar los datos de los usuarios

        for usuario_items in usuario_OBJ:
            usuarios_data.append({
                'id': usuario_items.id,
                'nombre_usuario': usuario_items.username,
                'nombre': usuario_items.first_name,
                'apellido': usuario_items.last_name,
                'correo': usuario_items.email,
            })

        return JsonResponse({'usuarios': usuarios_data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Funciones de usuarios


# Deudas

def listar_deudas(request):
    if request.method == 'GET':
        usuario = request.user  # Obtén el usuario autenticado
        deudas = Deuda.objects.filter(usuario_deudor=usuario)  # Filtrar deudas por usuario
        deudas_data = []  # Lista para almacenar los datos de las deudas

        for deuda in deudas:
            deudas_data.append({
                'id': deuda.id,
                'descripcion': deuda.descripcion,
                'monto': str(deuda.monto),  # Convertimos a string para JSON
                'fecha_vencimiento': deuda.fecha_vencimiento.strftime('%Y-%m-%d'),
                'estado': deuda.estado,
                'tipo_deuda': deuda.tipo_deuda,
            })

        return JsonResponse({'deudas': deudas_data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def listar_prestamos(request):
    if request.method == 'GET':
        usuario = request.user  # Obtén el usuario autenticado
        prestamos = Prestamo.objects.filter(usuario_prestamista=usuario)  # Filtrar prestamos por usuario
        prestamos_data = []  # Lista para almacenar los datos de los prestamos

        for prestamo in prestamos:
            prestamos_data.append({
                'id': prestamo.id,
                'descripcion': prestamo.descripcion,
                'monto_total': str(prestamo.monto_total),  # Convertimos a string para JSON
                'tasa_interes': str(prestamo.tasa_interes),
                'fecha_inicio': prestamo.fecha_inicio.strftime('%Y-%m-%d'),
                'usuario_prestamista': prestamo.usuario_prestamista.username,
                'fechaIngreso': prestamo.fechaIngreso.strftime('%Y-%m-%d %H:%M:%S'),
            })

        return JsonResponse({'prestamos': prestamos_data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def listar_tarjetas_credito(request):
    if request.method == 'GET':
        usuario = request.user  # Obtén el usuario autenticado
        # Filtrar deudas por usuario
        deudas = Deuda.objects.filter(usuario_deudor=usuario)
         # Filtrar tarjetas de crédito por deudas valores unicos
        tarjetas_credito =  TarjetaCredito.objects.filter(deuda__in=deudas).distinct()
        tarjetas_credito_data = []  # Lista para almacenar los datos de las tarjetas de crédito

        for tarjeta in tarjetas_credito:
            tarjetas_credito_data.append({
                'id': tarjeta.id,
                'numero_tarjeta': tarjeta.numero_tarjeta,
                'nombre_titular': tarjeta.nombre_titular,
                'fecha_vencimiento': tarjeta.fecha_vencimiento.strftime('%Y-%m-%d'),
                'colorIdentificacion': tarjeta.colorIdentificacion,
                'limite': str(tarjeta.limite),
            })

        return JsonResponse({'tarjetas_credito': tarjetas_credito_data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Funciones de deudas


# Dinero 
def listar_ingresos(request):
    if request.method == 'GET':
        usuario = request.user  # Obtén el usuario autenticado
        ingresos = Ingreso.objects.filter(usuario=usuario)  # Filtrar ingresos por usuario
        ingresos_data = []  # Lista para almacenar los datos de los ingresos

        for ingreso in ingresos:
            ingresos_data.append({
                'id': ingreso.id,
                'descripcion': ingreso.descripcion,
                'cantidad': str(ingreso.cantidad),  # Convertimos a string para JSON
                'fuente': ingreso.fuente,
                'fecha': ingreso.fecha.strftime('%Y-%m-%d'),
            })

        return JsonResponse({'ingresos': ingresos_data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def listar_egresos(request):
    if request.method == 'GET':
        usuario = request.user  # Obtén el usuario autenticado
        egresos = Egreso.objects.filter(usuario=usuario)  # Filtrar egresos por usuario
        egresos_data = []  # Lista para almacenar los datos de los egresos

        for egreso in egresos:
            egresos_data.append({
                'id': egreso.id,
                'descripcion': egreso.descripcion,
                'cantidad': str(egreso.cantidad),  # Convertimos a string para JSON
                'proposito': egreso.proposito,
                'fecha': egreso.fecha.strftime('%Y-%m-%d'),
            })

        return JsonResponse({'egresos': egresos_data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)



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