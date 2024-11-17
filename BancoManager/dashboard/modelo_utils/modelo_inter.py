from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone

#  _____                                                                 _____ 
# ( ___ )                                                               ( ___ )
#  |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
#  |   |  __  __  ___  ____  _____ _     ___  ____                       |   | 
#  |   | |  \/  |/ _ \|  _ \| ____| |   / _ \/ ___|                      |   | 
#  |   | | |\/| | | | | | | |  _| | |  | | | \___ \                      |   | 
#  |   | | |  | | |_| | |_| | |___| |__| |_| |___) |                     |   | 
#  |   | |_|__|_|\___/|____/|_____|_____\___/|____/   _     _____ ____   |   | 
#  |   | |  _ \|  _ \|_ _| \ | |/ ___|_ _|  _ \ / \  | |   | ____/ ___|  |   | 
#  |   | | |_) | |_) || ||  \| | |    | || |_) / _ \ | |   |  _| \___ \  |   | 
#  |   | |  __/|  _ < | || |\  | |___ | ||  __/ ___ \| |___| |___ ___) | |   | 
#  |   | |_|   |_| \_\___|_| \_|\____|___|_| /_/   \_\_____|_____|____/  |   | 
#  |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
# (_____)                                                               (_____)
from ..modelo_deudas.models_deudas import *
from ..modelo_banco.models_banco import *
from ..modelo_auditlog.modelo_auditlog import *
from ..modelo_dinero.models_dinero import *

from ..utils.generales import *

class RegistroIngreso(models.Model):
    """
    Modelo para registrar los detalles de cada ingreso realizado,
    incluyendo información sobre la cuenta, el monto, la fecha,
    y el comprobante del ingreso.
    """
    cuenta = models.ForeignKey('CuentaBancaria', on_delete=models.CASCADE, related_name='registros_ingreso')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    comprobante = models.FileField(upload_to=comprobante_upload_to_ingresos, blank=True, null=True)  # Para imágenes o PDFs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro de Ingreso"
        verbose_name_plural = "Registros de Ingreso"
        ordering = ['-fecha']  # Para que se ordenen descendientemente por fecha

    def clean(self):
        """
        Validaciones personalizadas para garantizar que el
        registro de ingreso sea coherente.
        """
        # Verificar que la fecha no sea en el futuro
        if self.fecha > timezone.now().date():
            raise ValidationError('La fecha del ingreso no puede ser futura.')
        
        # Verificar que el monto sea positivo
        if self.monto <= 0:
            raise ValidationError('El monto del ingreso debe ser mayor que cero.')

    def __str__(self):
        return f"Ingreso de {self.monto} en {self.cuenta.nombre} - Fecha: {self.fecha}"

    def aplicar_ingreso(self):
        """
        Método para aplicar el ingreso a la cuenta asociada,
        actualizando el saldo de la cuenta.
        """
        cuenta = self.cuenta
        cuenta.saldoActual += self.monto
        cuenta.saldoInicial += self.monto
        cuenta.save()

    def obtener_comprobante_url(self):
        """
        Método que devuelve la URL del comprobante si está disponible.
        """
        if self.comprobante:
            return self.comprobante.url
        return None
    

class RegistroEgreso(models.Model):
    """
    Modelo para registrar los detalles de cada egreso realizado,
    incluyendo información sobre la cuenta, el monto, la fecha,
    y el comprobante del egreso.
    """
    tipo_modelo = 'egreso'
    cuenta = models.ForeignKey('CuentaBancaria', on_delete=models.CASCADE, related_name='registros_egreso')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    comprobante = models.FileField(upload_to=comprobante_upload_to_egresos, blank=True, null=True)  # Para imágenes o PDFs
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registros_egreso')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro de Egreso"
        verbose_name_plural = "Registros de Egreso"
        ordering = ['-fecha']  # Para que se ordenen descendientemente por fecha

    def clean(self):
        """
        Validaciones personalizadas para garantizar que el
        registro de egreso sea coherente.
        """
        # Verificar que la fecha no sea en el futuro
        if self.fecha > timezone.now().date():
            raise ValidationError('La fecha del egreso no puede ser futura.')
        
        # Verificar que el monto sea positivo
        if self.monto <= 0:
            raise ValidationError('El monto del egreso debe ser mayor que cero.')

    def __str__(self):
        return f"Egreso de {self.monto} en {self.cuenta.nombre} - Fecha: {self.fecha}"

    def aplicar_egreso(self):
        """
        Método para aplicar el egreso a la cuenta asociada,
        actualizando el saldo de la cuenta.
        """
        cuenta = self.cuenta
        if cuenta.saldoActual < self.monto:
            raise ValidationError('El saldo de la cuenta es insuficiente para realizar este egreso.')
        # Validar si la cuenta es de tipo crédito sumar el monto al saldo
        if cuenta.tipoCuenta == 'Credito':
            cuenta.saldoActual += self.monto
            cuenta.saldoInicial += self.monto
        else:
            cuenta.saldoActual -= self.monto
            cuenta.saldoInicial -= self.monto
        cuenta.save()

    def obtener_comprobante_url(self):
        """
        Método que devuelve la URL del comprobante si está disponible.
        """
        if self.comprobante:
            return self.comprobante.url
        return None
    

class RegistroPago(models.Model):
    """
    Modelo para registrar los detalles de cada pago realizado
    hacia una deuda.
    """
    deuda = models.ForeignKey('Deuda', on_delete=models.CASCADE, related_name='registros_pago')
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha_pago = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registros_pago')

    class Meta:
        verbose_name = "Registro de Pago"
        verbose_name_plural = "Registros de Pago"
        ordering = ['-fecha_pago']  # Para que se ordenen descendientemente por fecha

    def clean(self):
        """
        Validaciones personalizadas para garantizar que el
        registro de pago sea coherente.
        """
        # Verificar que la fecha no sea en el futuro
        if self.fecha_pago > timezone.now().date():
            raise ValidationError('La fecha del pago no puede ser futura.')

        # Verificar que el monto de pago sea positivo
        if self.monto_pago <= 0:
            raise ValidationError('El monto del pago debe ser mayor que cero.')

        # Asegurarse de que el pago no exceda la deuda restante
        if self.monto_pago > self.deuda.monto:
            raise ValidationError('El monto del pago excede el saldo de la deuda.')

    def __str__(self):
        return f"Pago de {self.monto_pago} hacia {self.deuda} - Fecha: {self.fecha_pago}"

    def aplicar_pago(self):
        """
        Método para aplicar el pago hacia la deuda, ajustando
        el monto de la deuda restante.
        """
        self.deuda.monto -= self.monto_pago
        if self.deuda.monto < 0:  # Si el saldo se vuelve negativo
            self.deuda.monto = 0
        
        # Actualizar el estado de la deuda si se saldó
        if self.deuda.monto == 0:
            self.deuda.estado = True
        
        self.deuda.save()
        self.save()  # Guardar el registro de pago


class Transferencia(models.Model):
    """
    Modelo para registrar las transferencias entre cuentas bancarias,
    incluyendo detalles sobre las cuentas involucradas, el monto, la fecha
    y una descripción opcional.
    """
    cuenta_origen = models.ForeignKey('CuentaBancaria', on_delete=models.CASCADE, related_name='transferencias_origen')
    cuenta_destino = models.ForeignKey('CuentaBancaria', on_delete=models.CASCADE, related_name='transferencias_destino')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha_transferencia = models.DateField(default=timezone.now)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transferencias')

    class Meta:
        verbose_name = "Transferencia"
        verbose_name_plural = "Transferencias"
        ordering = ['-fecha_transferencia']  # Para que se ordenen descendientemente por fecha

    def clean(self):
        """
        Validaciones personalizadas para garantizar que la
        transferencia sea coherente.
        """
        # Verificar que la fecha no sea en el futuro
        if self.fecha_transferencia > timezone.now().date():
            raise ValidationError('La fecha de transferencia no puede ser futura.')

        # Verificar que el monto de transferencia sea positivo
        if self.monto <= 0:
            raise ValidationError('El monto de la transferencia debe ser mayor que cero.')

        # Asegurarse de que la cuenta de origen tiene suficiente saldo
        if self.cuenta_origen.saldoActual < self.monto:
            raise ValidationError('La cuenta de origen no tiene saldo suficiente para realizar la transferencia.')

    def __str__(self):
        return f"Transferencia de {self.monto} de {self.cuenta_origen.nombre} a {self.cuenta_destino.nombre} - Fecha: {self.fecha_transferencia}"

    def procesar_transferencia(self):
        """
        Método para procesar la transferencia, actualizando el saldo
        de las cuentas involucradas.
        """
        # Aplicar el monto a las cuentas
        self.cuenta_origen.saldoActual -= self.monto
        self.cuenta_destino.saldoActual += self.monto
        
        # Guardar los cambios en las cuentas
        self.cuenta_origen.save()
        self.cuenta_destino.save()


class ReporteMensual(models.Model):
    """
    Modelo para almacenar los reportes mensuales de finanzas
    de un usuario, incluyendo ingresos, egresos y saldo final.
    """
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reportes_mensuales')
    mes = models.PositiveIntegerField()  # Mes del año: 1 a 12
    tiempo_anual = models.PositiveIntegerField()  # Año del reporte
    ingresos_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    egresos_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_final = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'mes', 'tiempo_anual')  # Un usuario no puede tener dos reportes para el mismo mes y año
        verbose_name = "Reporte Mensual"
        verbose_name_plural = "Reportes Mensuales"
        ordering = ['-tiempo_anual', '-mes']  # Ordenar por año y mes descendientes

    def clean(self):
        """
        Validaciones personalizadas para garantizar que el
        reporte mensual sea coherente.
        """
        if self.mes < 1 or self.mes > 12:
            raise ValidationError('El mes debe estar entre 1 y 12.')
        if self.tiempo_anual < 2000:  # Suponiendo que los reportes no deberían ser anteriores al año 2000
            raise ValidationError('El año debe ser 2000 o posterior.')

    def __str__(self):
        return f"Reporte de {self.usuario} - {self.mes}/{self.tiempo_anual}"

    def calcular_saldo(self):
        """
        Método para calcular el saldo final a partir de ingresos y egresos.
        """
        self.saldo_final = self.ingresos_total - self.egresos_total

