from django.shortcuts import render, redirect
from django.views import View
from django.db import models
from django.db.models import Sum, F

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from .modelo_banco.models_banco import Banco
from .modelo_dinero.models_dinero import CuentaBancaria, Ingreso, Egreso
from .modelo_deudas.models_deudas import Deuda, Prestamo, TarjetaCredito

from datetime import datetime, timedelta
import random

def generar_color_unico():
    """Genera un color RGB único."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'rgba({r}, {g}, {b}, 0.5)'


class InicioHelper:
    def obtener_totales_ingresos_egresos(self, usuario, formato_query=True):
        total_ingresos = Ingreso.objects.filter(usuario=usuario).annotate(mes=F('fecha__month')).aggregate(total_ingresos=models.Sum('cantidad'))['total_ingresos'] or 0
        total_egresos = Egreso.objects.filter(usuario=usuario).aggregate(total_egresos=models.Sum('cantidad'))['total_egresos'] or 0
        return total_ingresos, total_egresos
    
    def obtener_totales_ingresos_egresos_por_mes(self, usuario, formato_query=True):
				        # Filtrar las cuenta bancaria de debito o cheque - Sumar los saldos actual de las cuentas
        totales_ingresos = CuentaBancaria.objects.filter(usuario=usuario, tipoCuenta__in=['Cheques', 'Debito'])
        # Sumar los saldos actual de las cuentas
        saldos_actuales = 0
        for total in totales_ingresos:
            saldos_actuales += total.saldoActual
        totales_egresos = CuentaBancaria.objects.filter(usuario=usuario, tipoCuenta='Credito')
        # Sumar los saldos actual de las cuentas
        saldos_actuales_egresos = 0
        for total in totales_egresos:
            saldos_actuales_egresos += total.saldoActual
            
        return saldos_actuales, saldos_actuales_egresos
        
    
    def obtener_totales_actuales(self, usuario, formato_query=True):
        total_ingresos = Ingreso.objects.filter(usuario=usuario).aggregate(total_ingresos=models.Sum('cantidad'))['total_ingresos'] or 0
        total_egresos = Egreso.objects.filter(usuario=usuario).aggregate(total_egresos=models.Sum('cantidad'))['total_egresos'] or 0
        total_deudas = Deuda.objects.filter(usuario_deudor=usuario).aggregate(total_deudas=models.Sum('monto'))['total_deudas'] or 0
        return total_ingresos, total_egresos, total_deudas

    def obtener_cuentas(self, usuario, formato_query=True):
        if formato_query:
            return CuentaBancaria.objects.filter(usuario=usuario)[:3]
        else:
            cuentas = CuentaBancaria.objects.filter(usuario=usuario)
            lista_cuentas = []
            for cuenta in cuentas:
                lista_cuentas.append({
                    'id': cuenta.id,
                    'nombre': cuenta.nombre,
                    'saldo': cuenta.saldoActual
                })
            return lista_cuentas        
    
    def obtener_cuentas_filtradas(self, usuario, formato_query=True):
        total_ingresos = CuentaBancaria.objects.filter(usuario=usuario, tipoCuenta__in=['Cheques', 'Debito'])
        total_egresos = CuentaBancaria.objects.filter(usuario=usuario, tipoCuenta='Credito')
        if formato_query:
            return total_ingresos, total_egresos
        else:
            lista_ingresos = []
            lista_egresos = []
            for ingreso in total_ingresos:
                lista_ingresos.append({
                    "id": ingreso.id,
                    'nombre': ingreso.nombre,
                    
                    'numeroCuenta': ingreso.numeroCuenta,
                    'tipoCuenta': ingreso.tipoCuenta,
                    'afiliacion': ingreso.afilacion,
                    
                    'saldoInicial': ingreso.saldoInicial,
                    'saldoActual': ingreso.saldoActual,
                    
                    'banco': ingreso.banco.nombre,
                    
                    'colorIdentificacion': ingreso.colorIdentificacion,
                    'cvc': ingreso.cvc,
                    'fechaVencimiento': ingreso.fechaVencimiento,
                    'usuario': ingreso.usuario.id,
                    
                    'logo': "media/"+str(ingreso.logo)
                })
            for egreso in total_egresos:
                lista_egresos.append({
                    "id": egreso.id,
                    'nombre': egreso.nombre,
                    
                    'numeroCuenta': egreso.numeroCuenta,
                    'tipoCuenta': egreso.tipoCuenta,
                    'afiliacion': egreso.afilacion,
                    
                    'saldoInicial': egreso.saldoInicial,
                    'saldoActual': egreso.saldoActual,
                    
                    'banco': egreso.banco.nombre,
                    
                    'colorIdentificacion': egreso.colorIdentificacion,
                    'cvc': egreso.cvc,
                    'fechaVencimiento': egreso.fechaVencimiento,
                    'usuario': egreso.usuario.id,
                    
                    'logo': "media/"+str(egreso.logo)
                })
            return lista_ingresos, lista_egresos

    def obtener_transacciones_recientes(self, usuario, formato_query=True):
        ingresos_recentes = Ingreso.objects.filter(usuario=usuario).order_by('-fecha')[:5]
        egresos_recentes = Egreso.objects.filter(usuario=usuario).order_by('-fecha')[:5]

        if formato_query:
            return ingresos_recentes, egresos_recentes
        else:
            lista_ingresos_recientes = []
            lista_egresos_recientes = []
            for ingreso in ingresos_recentes:
                lista_ingresos_recientes.append({
                    'cantidad': float(ingreso.cantidad),
                    'descripcion': ingreso.descripcion,
                    'fecha': ingreso.fecha,
                    'fuente': ingreso.fuente,
                    'cuenta': ingreso.cuenta.nombre
                })
            
            for egreso in egresos_recentes:
                lista_egresos_recientes.append({
                    'cantidad': float(egreso.cantidad),
                    'descripcion': egreso.descripcion,
                    'fecha': egreso.fecha,
                    'fuente': egreso.proposito,
                    'cuenta': egreso.cuenta.nombre
                })

            return lista_ingresos_recientes, lista_egresos_recientes
       
    def obtener_transacciones(self, usuario, formato_query=True):
        ingresos = Ingreso.objects.filter(usuario=usuario)
        egresos = Egreso.objects.filter(usuario=usuario)
        if formato_query:
            return ingresos, egresos
        else:
            lista_ingresos = []
            lista_egresos = []
            for ingreso in ingresos:
                lista_ingresos.append({
                    "id": ingreso.id,
                    'cantidad': float(ingreso.cantidad),
                    'descripcion': ingreso.descripcion,
                    'fecha': ingreso.fecha.strftime('%Y-%m-%d'),
                    'fuente': ingreso.fuente,
                    'cuenta': ingreso.cuenta.nombre
                })
            for egreso in egresos:
                lista_egresos.append({
                    "id": egreso.id,
                    'cantidad': float(egreso.cantidad),
                    'descripcion': egreso.descripcion,
                    'fecha': egreso.fecha.strftime('%Y-%m-%d'),
                    'fuente': egreso.proposito,
                    'cuenta': egreso.cuenta.nombre
                })
            return lista_ingresos, lista_egresos
        
    def obtener_gastos_por_mes(self, usuario):
        twelve_months_ago = datetime.now() - timedelta(days=365)
        return Egreso.objects.filter(usuario=usuario, fecha__gte=twelve_months_ago)

    def obtener_fuentes_propositos_comunes(self, usuario, limitar_resultados=True):
        if limitar_resultados:
            top_fuentes_ingresos = Ingreso.objects.filter(usuario=usuario).values('fuente').annotate(count=models.Count('fuente')).order_by('-count')[:4]
            top_propositos_egresos = Egreso.objects.filter(usuario=usuario).values('proposito').annotate(count=models.Count('proposito')).order_by('-count')[:4]
        else:
            top_fuentes_ingresos = Ingreso.objects.filter(usuario=usuario).values('fuente').annotate(count=models.Count('fuente')).order_by('-count')
            top_propositos_egresos = Egreso.objects.filter(usuario=usuario).values('proposito').annotate(count=models.Count('proposito')).order_by('-count')
        return top_fuentes_ingresos, top_propositos_egresos

    def obtener_datos_graficos_mes_actual(self, usuario, formato_query=True):
        month = datetime.now().month
        year = datetime.now().year
        ingresos_mensuales = Ingreso.objects.filter(usuario=usuario, fecha__month=month, fecha__year=year)
        egresos_mensuales = Egreso.objects.filter(usuario=usuario, fecha__month=month, fecha__year=year)
        if formato_query:
            return ingresos_mensuales, egresos_mensuales
        else:
            lista_ingresos_mensuales = []
            lista_egresos_mensuales = []
            for ingreso in ingresos_mensuales:
                lista_ingresos_mensuales.append({
                    'cantidad': float(ingreso.cantidad),
                    'descripcion': ingreso.descripcion,
                    'fecha': ingreso.fecha,
                    'fuente': ingreso.fuente,
                    'cuenta': ingreso.cuenta.nombre
                })

            for egreso in egresos_mensuales:
                lista_egresos_mensuales.append({
                    'cantidad': float(egreso.cantidad),
                    'descripcion': egreso.descripcion,
                    'fecha': egreso.fecha,
                    'proposito': egreso.proposito,
                    'cuenta': egreso.cuenta.nombre
                })
            return lista_ingresos_mensuales, lista_egresos_mensuales
            
    def obtener_gastos_ingresos_por_mes(self, usuario):
        twelve_months_ago = datetime.now() - timedelta(days=365)
        gastos_por_mes = Egreso.objects.filter(usuario=usuario, fecha__gte=twelve_months_ago)
        ingresos_por_mes = Ingreso.objects.filter(usuario=usuario, fecha__gte=twelve_months_ago)
        return gastos_por_mes, ingresos_por_mes

    def obtener_totales_deudas_prestamos(self, usuario, formato_query=True):
        total_deudas = Deuda.objects.filter(usuario_deudor=usuario).aggregate(total_deudas=models.Sum('monto'))['total_deudas'] or 0
        total_prestamos = Prestamo.objects.filter(usuario_prestamista=usuario).aggregate(total_prestamos=models.Sum('monto_total'))['total_prestamos'] or 0
        return total_deudas, total_prestamos

    def obtener_deudas_proximas(self, usuario):
        return Deuda.objects.filter(usuario_deudor=usuario, fecha_vencimiento__gte=datetime.now()).order_by('fecha_vencimiento')

    def calcular_total_deudas(self, usuario):
        return Deuda.objects.filter(usuario_deudor=usuario).aggregate(total_deuda=models.Sum('monto'))['total_deuda'] or 0

    def calcular_acumulados_por_mes(self, transacciones_por_mes):
        acumulados = {i: 0 for i in range(1, 13)}
        for transaccion in transacciones_por_mes:
            mes = transaccion.fecha.month
            acumulados[mes] += transaccion.cantidad
        return acumulados

    def calcular_ingresos_por_categoria(self, usuario):
        # Agrupar los ingresos por categoría y calcular el total de cada categoría
        ingresos_por_categoria = (
            Ingreso.objects.filter(usuario=usuario)
            .values('fuente')
            .annotate(total=Sum('cantidad'))
            .order_by('fuente')
            # Generar colores aleatorios para las categorías (fuente) dependiendo de la longitud de la fuente
        )
        # Convertir los datos a una lista de diccionarios y añadir un color único a cada categoría
        ingresos_por_categoria_list = []
        for ingreso in ingresos_por_categoria:
            ingreso['color'] = generar_color_unico()
            ingresos_por_categoria_list.append(ingreso)
        
        return ingresos_por_categoria_list
    
    def calcular_egresos_por_categoria(self, usuario):
        # Agrupar los egresos por categoría y calcular el total de cada categoría
        egresos_por_categoria = (
            Egreso.objects.filter(usuario=usuario)
            .values('proposito')
            .annotate(total=Sum('cantidad'))
            .order_by('proposito')
            # Generar colores aleatorios para las categorías (proposito) dependiendo de la longitud del proposito
        )
        # Renombra la clave 'proposito' a 'fuente' para que coincida con la clave de ingresos
        egresos_por_categoria = [{'fuente': egreso.pop('proposito'), 'total': egreso['total']} for egreso in egresos_por_categoria]
        # Convertir los datos a una lista de diccionarios y añadir un color único a cada categoría
        egresos_por_categoria_list = []
        for egreso in egresos_por_categoria:
            egreso['color'] = generar_color_unico()
            egresos_por_categoria_list.append(egreso)
    

        return egresos_por_categoria_list

    def preparar_datos_graficas(self, ingresos_acumulados, gastos_acumulados):
        ingresos_data = [float(ingresos_acumulados[i]) for i in range(1, 13)]
        egresos_data = [float(gastos_acumulados[i]) for i in range(1, 13)]
        return ingresos_data, egresos_data

    def manejar_filtrado_ordenacion(self, request, ingresos, egresos):
        tipo_filter = request.GET.get('tipo', None)
        proposito_filter = request.GET.get('proposito', None)
        fecha_filter = request.GET.get('fecha', None)
        orden = request.GET.get('orden', 'fecha')

        if tipo_filter:
            if tipo_filter == 'ingreso':
                ingresos = ingresos.all()
                egresos = Egreso.objects.none()
            elif tipo_filter == 'egreso':
                egresos = egresos.all()
                ingresos = Ingreso.objects.none()

        if proposito_filter:
            egresos = egresos.filter(proposito=proposito_filter)

        if fecha_filter:
            ingresos = ingresos.filter(fecha__date=fecha_filter)
            egresos = egresos.filter(fecha__date=fecha_filter)

        if orden == 'descripcion':
            ingresos = ingresos.order_by('descripcion')
            egresos = egresos.order_by('descripcion')
        elif orden == 'cantidad':
            ingresos = ingresos.order_by('cantidad')
            egresos = egresos.order_by('cantidad')
        else:
            ingresos = ingresos.order_by('fecha')
            egresos = egresos.order_by('fecha')

        return ingresos, egresos
    
    def filtrar_descripciones_unicas(self, usuario, formato_query=True):
        ingresos = Ingreso.objects.filter(usuario=usuario).values('descripcion').distinct()
        egresos = Egreso.objects.filter(usuario=usuario).values('proposito').distinct()
        if formato_query:
            return ingresos, egresos
        else:
            lista_ingresos = [ingreso['descripcion'] for ingreso in ingresos]
            lista_egresos = [egreso['proposito'] for egreso in egresos]
            return lista_ingresos, lista_egresos
        
    def obtener_cuentas_bancarias(self, usuario, formato_query=True):
        if formato_query:
            return CuentaBancaria.objects.filter(usuario=usuario)[:3]
        else:
            cuentas = CuentaBancaria.objects.filter(usuario=usuario)
            lista_cuentas = []
            for cuenta in cuentas:
                lista_cuentas.append({
                    "id": cuenta.id,
                    'nombre': cuenta.nombre,
                    'numeroCuenta': cuenta.numeroCuenta,
                    'tipoCuenta': cuenta.tipoCuenta,
                    'afiliacion': cuenta.afilacion,
                    'saldoInicial': cuenta.saldoInicial,
                    'saldoActual': cuenta.saldoActual,
                    'banco': cuenta.banco.nombre,
                    'colorIdentificacion': cuenta.colorIdentificacion,
                    'cvc': cuenta.cvc,
                    'fechaVencimiento': cuenta.fechaVencimiento,
                    'usuario': cuenta.usuario.id,
                    'modelo_principal': 'CuentaBancaria',
                })
            return lista_cuentas
        
    def obtener_bancos(self, formato_query=True):
        if formato_query:
            return Banco.objects.all()
        else:
            bancos = Banco.objects.all()
            lista_bancos = []
            for banco in bancos:
                lista_bancos.append({
                    'id': banco.id,
                    'nombre': banco.nombre,
                    'pais': banco.pais
                })
            return lista_bancos
        
    def obtener_tarjetas_credito(self, usuario, formato_query=True):
        if formato_query:
            return TarjetaCredito.objects.filter(usuario=usuario)
        else:
            tarjetas = TarjetaCredito.objects.filter(usuario=usuario)
            lista_tarjetas = []
            for tarjeta in tarjetas:
                lista_tarjetas.append({
                    "id": tarjeta.id,
                    "numeroTarjeta": tarjeta.numero_tarjeta,
                    "nombre_titular": tarjeta.nombre_titular,
                    "fechaVencimiento": tarjeta.fecha_vencimiento,
                    "colorIdentificacion": tarjeta.colorIdentificacion,
                    "limte_maximo": tarjeta.limite_maximo,
                    "limite_actual": tarjeta.limite_actual,
                    "usuario": tarjeta.usuario.id,
                })
            return lista_tarjetas
        
    def obtener_prestamos(self, usuario, formato_query=True):
        if formato_query:
            return Prestamo.objects.filter(usuario_prestamista=usuario)
        else:
            prestamos = Prestamo.objects.filter(usuario_prestamista=usuario)
            lista_prestamos = []
            for prestamo in prestamos:
                lista_prestamos.append({
                    "id": prestamo.id,
                    "descripcion": prestamo.descripcion,
                    "monto_total": prestamo.monto_total,
                    "tasa_interes": prestamo.tasa_interes,
                    "fecha_inicio": prestamo.fecha_inicio,
                    "usuario": prestamo.usuario_prestamista.id,
                })
            return lista_prestamos
        
    def obtener_prestamos_activos(self, usuario, formato_query=True):
        if formato_query:
            return Prestamo.objects.filter(usuario_prestamista=usuario, estado=True)
        else:
            prestamos = Prestamo.objects.filter(usuario_prestamista=usuario, estado=True)
            lista_prestamos = []
            for prestamo in prestamos:
                lista_prestamos.append({
                    "id": prestamo.id,
                    "descripcion": prestamo.descripcion,
                    "monto_total": prestamo.monto_total,
                    "tasa_interes": prestamo.tasa_interes,
                    "fecha_inicio": prestamo.fecha_inicio,
                    "usuario": prestamo.usuario_prestamista.id,
                })
            return lista_prestamos

    def obtener_deudas(self, usuario, formato_query=True):
        if formato_query:
            total_deudas = Deuda.objects.filter(usuario_deudor=usuario).aggregate(total_deudas=models.Sum('monto'))['total_deudas'] or 0
            return Deuda.objects.filter(usuario_deudor=usuario), total_deudas
        else:
            deudas = Deuda.objects.filter(usuario_deudor=usuario)
            # Contar cuantas son de tarjeta de crédito y cuantas son de préstamos
            lista_deudas = []
            total_deudas = 0
            for deuda in deudas:
                total_deudas+= deuda.monto
                lista_deudas.append({
                    "id": deuda.id,
                    "usuario_deudor": deuda.usuario_deudor.username,
                    "monto": deuda.monto,
                    "tipo_deuda": deuda.tipo_deuda,
                    "estado": "Pagada" if deuda.estado else "Pendiente",
                    "descripcion": deuda.descripcion,

                    "tarjeta": deuda.tarjeta.numeroCuenta if deuda.tarjeta else None,
                    "prestamo": deuda.prestamo.descripcion if deuda.prestamo else None,

                    "deuda_meses": deuda.deuda_meses.descripcion if deuda.deuda_meses else None,

                    "fecha_vencimiento": deuda.fecha_vencimiento,
                    "meses": deuda.meses,
                    "interes": deuda.interes,                    
                })

            
            return lista_deudas, total_deudas

class InicioView(LoginRequiredMixin, View):
    def get(self, request):
        helper = InicioHelper()
        # Obtener totales de ingresos y egresos
        total_ingresos, total_egresos = helper.obtener_totales_ingresos_egresos(request.user)
        # Obtener cuentas
        cuentas = helper.obtener_cuentas(request.user)
        # Obtener transacciones recientes
        ingresos_recentes, egresos_recentes = helper.obtener_transacciones_recientes(request.user)
        # Obtener transacciones (ingresos y egresos)
        ingresos, egresos = helper.obtener_transacciones(request.user)
        # Obtener gastos de los últimos 12 meses
        gastos_por_mes = helper.obtener_gastos_por_mes(request.user)
        # Obtener fuentes más comunes de ingresos y propósitos más comunes de egresos
        top_fuentes_ingresos, top_propositos_egresos = helper.obtener_fuentes_propositos_comunes(request.user)
        # Datos para los gráficos del mes actual
        ingresos_mensuales, egresos_mensuales = helper.obtener_datos_graficos_mes_actual(request.user)
        # Obtener gastos e ingresos de los últimos 12 meses
        gastos_por_mes, ingresos_por_mes = helper.obtener_gastos_ingresos_por_mes(request.user)
        # Crear un diccionario para almacenar el total acumulado por mes
        gastos_acumulados = helper.calcular_acumulados_por_mes(gastos_por_mes)
        ingresos_acumulados = helper.calcular_acumulados_por_mes(ingresos_por_mes)
        # Preparar datos para las gráficas
        ingresos_data, egresos_data = helper.preparar_datos_graficas(ingresos_acumulados, gastos_acumulados)
        # Manejar filtrado y ordenación
        ingresos, egresos = helper.manejar_filtrado_ordenacion(request, ingresos, egresos)
        # Obtener deudas próximas a pagar
        deudas_proximas = helper.obtener_deudas_proximas(request.user)
        total_deudas = helper.calcular_total_deudas(request.user)
        # Todas la catergorias unir top_fuentes_ingresos y top_propositos_egresos
        categorias = []
        for fuente_ingresos in top_fuentes_ingresos:
            categorias.append(fuente_ingresos['fuente'])
        for proposito_egresos in top_propositos_egresos:
            categorias.append(proposito_egresos['proposito'])
         # Obtener todas las cuentas
        cuentas = helper.obtener_cuentas(request.user, formato_query=False) 
        context = {
            'total_ingresos': float(total_ingresos),
            'total_egresos': float(total_egresos),
            'total_deudas': float(total_deudas),

            'cuentas': cuentas,
            'ingresos_recentes': ingresos_recentes,
            'egresos_recentes': egresos_recentes,

            'ingresos': ingresos,
            'egresos': egresos,

            'ingresos_data': ingresos_data,
            'egresos_data': egresos_data,

            'top_fuentes_ingresos': top_fuentes_ingresos,
            'top_propositos_egresos': top_propositos_egresos,

            'deudas_proximas': deudas_proximas,
            'categorias': categorias,
            'cuentas': cuentas,
        }
        return render(request, 'index.html', context)


def deudas(request):
    return render(request, 'finanzas/deudas.html')


#def ingresos(request):
    #return render(request, 'finanzas/ingresos.html')


def egresos(request):
    return render(request, 'finanzas/egresos.html')

def bancos(request):
    return render(request, 'finanzas/bancos.html')

def prestamos(request):
    return render(request, 'finanzas/prestamos.html')


def cuentas(request):
    return render(request, 'finanzas/cuenta.html')


def mi_cuenta(request):
    return render(request, 'usuario/mi_cuenta.html')



def login(request):
    return render(request, '')

def logout(request):
    return render(request, '')
