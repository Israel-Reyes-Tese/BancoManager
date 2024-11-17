from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..modelo_banco.models_banco import *
from django.db.models import Q
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone

from ..modelo_banco.models_banco import Banco, CuentaBancaria
from ..modelo_deudas.models_deudas import Deuda, TarjetaCredito, Prestamo
from ..modelo_auditlog.modelo_auditlog import AuditLog


from datetime import timedelta
from django.core.mail import send_mail



def BuscarInformacion(request, modelo, values=(), retorno_json=True, campos_busqueda=()):
    query = request.GET.get('query', '')
    modelo_principal = modelo.objects.filter(usuario=request.user)
    if query:
        for campo in campos_busqueda:
            modelo_principal = modelo_principal.filter(
                Q(**{campo: query})
            )
    modelo_list = list(modelo_principal.values(*values))
    # Transformar el nombre del modelo a algo más amigable
    modelo = modelo.__name__.lower()
    if retorno_json:
        return JsonResponse({f'{modelo}': modelo_list})
    else:
        return modelo_list
# Funciones Utilitarias
def comprobante_upload_to_ingresos(instance, filename):
    # Extrae la extensión del archivo
    extension = filename.split('.')[-1]
    
    # Genera el nuevo nombre del archivo con cuenta, usuario y monto
    nuevo_nombre = f"{instance.fecha}_{instance.cuenta.banco.nombre}_{instance.monto}.{extension}"
    nuevo_nombre_usuario = str(instance.usuario.username).replace(".", "_")
    # Ultimos 4 digitos de la cuenta
    nuevo_nombre_cuenta = str(instance.cuenta.numeroCuenta)[-4:]
    # Genera la ruta de subida con usuario, cuenta y tipo de modelo
    ruta = f"comprobantes_ingreso/{instance.tipo_modelo}/{nuevo_nombre_usuario}/{nuevo_nombre_cuenta}/{nuevo_nombre}"
    return ruta

def comprobante_upload_to_egresos(instance, filename):
    # Extrae la extensión del archivo
    extension = filename.split('.')[-1]
    
    # Genera el nuevo nombre del archivo con cuenta, usuario y monto
    nuevo_nombre = f"{instance.fecha}_{instance.cuenta.banco.nombre}_{instance.monto}.{extension}"
    nuevo_nombre_usuario = str(instance.usuario.username).replace(".", "_")
    nuevo_nombre_cuenta = str(instance.cuenta.numeroCuenta)[-4:]
    # Genera la ruta de subida con usuario, cuenta y tipo de modelo
    ruta = f"comprobantes_ingreso/{instance.tipo_modelo}/{nuevo_nombre_usuario}/{nuevo_nombre_cuenta}/{nuevo_nombre}"
    return ruta


def validate_fecha_no_futura(fecha):
    """Valida que una fecha no sea futura."""
    if fecha > timezone.now().date():
        raise ValidationError('La fecha no puede ser futura.')

def validate_monto_positivo(monto):
    """Valida que un monto sea mayor que cero."""
    if monto <= 0:
        raise ValidationError('El monto debe ser mayor que cero.')

def verifica_monto_pago(deuda_monto, pago_monto):
    """Verifica que el monto del pago no exceda la deuda restante."""
    if pago_monto > deuda_monto:
        raise ValidationError('El monto del pago excede el saldo de la deuda.')
    
def validate_fecha_no_futura(fecha):
    """Valida que una fecha no sea futura."""
    if fecha > timezone.now().date():
        raise ValidationError('La fecha no puede ser futura.')

def validate_monto_positivo(monto):
    """Valida que un monto sea mayor que cero."""
    if monto <= 0:
        raise ValidationError('El monto debe ser mayor que cero.')

def actualizar_saldo(cuenta, monto, operacion='sumar'):
    """
    Actualiza el saldo de una cuenta bancaria.
    :param cuenta: La cuenta a actualizar.
    :param monto: El monto a agregar o restar.
    :param operacion: Tipo de operación (sumar o restar).
    """
    if operacion == 'sumar':
        cuenta.saldoActual += monto
    elif operacion == 'restar':
        cuenta.saldoActual -= monto
    
    cuenta.save()

def registrar_actividad(usuario, accion, detalle):
    """
    Registra una actividad en el sistema (puedes expandir con un modelo específico).
    :param usuario: El usuario que realiza la acción.
    :param accion: La acción realizada.
    :param detalle: Detalles sobre la acción.
    """
    # Esta función puede implementar el registro en un modelo AuditLog o similar
    pass


def log_audit_action(model_name, action, record_id, user, description=''):
    """Función para crear un registro de auditoría."""
    log_entry = AuditLog(
        model_name=model_name,
        action=action,
        record_id=record_id,
        user=user,
        description=description
    )
    log_entry.clean()  # Ejecutamos las validaciones
    log_entry.save()  # Guardamos el registro en la base de datos


def validate_mes(mes):
    """Valida que un mes sea válido (1 a 12)."""
    if mes < 1 or mes > 12:
        raise ValidationError('El mes debe estar entre 1 y 12.')

def validate_año(año):
    """Valida que el año sea razonable (como mínimo 2000)."""
    if año < 2000:
        raise ValidationError('El año debe ser 2000 o posterior.')
# - 
def actualizar_saldo(cuenta, saldo_anterior, nuevo_saldo):
    """
    Función auxiliar para actualizar el saldo de una cuenta bancaria.
    """
    # Calcular la diferencia de saldo
    diferencia = nuevo_saldo - saldo_anterior

    # Actualizar el saldo de la cuenta bancaria
    cuenta.saldoInicial += diferencia
    cuenta.save()

def calcular_fecha_vencimiento(fecha_inicio, dias=30):
    """
    Función auxiliar para calcular una fecha de vencimiento
    predeterminada a 30 días después de la fecha de inicio.
    """
    return fecha_inicio + timedelta(days=dias)


def enviar_alerta_deuda_alta(usuario, monto):
    """
    Función auxiliar para enviar un correo de alerta si 
    el monto de la deuda supera el límite establecido.
    """
    subject = 'Alerta: Deuda alta'
    message = f'Se ha registrado una deuda alta de {monto}.\nPor favor, revise su estado financiero.'
    from_email = 'noreply@tuapp.com'
    
    # Envío del correo
    send_mail(
        subject,
        message,
        from_email,
        [usuario.email],
        fail_silently=False,
    )


def actualizar_limite_deuda(usuario, nuevo_limite):
    """
    Función auxiliar para actualizar el límite de las deudas asociadas
    al usuario cuando el límite de la tarjeta de crédito cambia.
    """
    # Actualiza el límite en todas las deudas relacionadas
    Deuda.objects.filter(usuario_deudor=usuario).update(monto=nuevo_limite)


def actualizar_estado_deuda(prestamo):
    """
    Función auxiliar para actualizar el estado de la deuda
    asociada cuando un préstamo es marcado como saldado.
    """
    try:
        # Obtener la deuda relacionada con el préstamo
        deuda = Deuda.objects.get(prestamo=prestamo)
        # Actualizar el estado de la deuda
        deuda.estado = prestamo.estado  # Actualiza el estado basado en el préstamo
        deuda.save()
    except ObjectDoesNotExist:
        print(f"No se encontró la deuda asociada al préstamo {prestamo.id}.")
    except Exception as e:
        print(f"Ocurrió un error al actualizar el estado de la deuda: {e}")