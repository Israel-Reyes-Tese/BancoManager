from django.conf import settings
from django.db import models

from ..modelo_banco.models_banco import CuentaBancaria
# +===========================================================================================================+
from ..modelo_abstract.model_abstract import TimestampedModel
# +===========================================================================================================+
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
# +===========================================================================================================+
from datetime import datetime

#╔═══════════════════════════════════════════════════════════════════════════════╗
#║ _____          _      _              _         ____       __     _ _ _        ║
#║|_   _|_ _ _ __(_) ___| |_ __ _    __| | ___   / ___|_ __ /_/  __| (_) |_ ___  ║
#║  | |/ _` | '__| |/ _ \ __/ _` |  / _` |/ _ \ | |   | '__/ _ \/ _` | | __/ _ \ ║
#║  | | (_| | |  | |  __/ || (_| | | (_| |  __/ | |___| | |  __/ (_| | | || (_) |║
#║  |_|\__,_|_| _/ |\___|\__\__,_|  \__,_|\___|  \____|_|  \___|\__,_|_|\__\___/ ║
#║             |__/                                                              ║
#╚═══════════════════════════════════════════════════════════════════════════════╝
class TarjetaCredito(TimestampedModel):
    """
    Modelo para representar una tarjeta de crédito con detalles relevantes
    como el número, titular y límite de la tarjeta.
    """
    numero_tarjeta = models.CharField(
        max_length=16,
        unique=True,
        validators=[RegexValidator(r'^\d{16}$', 'El número de tarjeta debe contener 16 dígitos.')]
    )
    nombre_titular = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField()

    colorIdentificacion = models.CharField(max_length=20)
    limite = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tarjetas_credito')

    class Meta:
        ordering = ['nombre_titular']
        verbose_name = "Tarjeta de Crédito"
        verbose_name_plural = "Tarjetas de Crédito"

    def clean(self):
        # Validar que la fecha de vencimiento sea en el futuro
        if self.fecha_vencimiento <= datetime.now().date():
            raise ValidationError('La fecha de vencimiento debe ser una fecha futura.')

    def __str__(self):
        return f"Tarjeta: {self.numero_tarjeta} - Titular: {self.nombre_titular} - Límite: {self.limite} - Vencimiento: {self.fecha_vencimiento}"

#╔══════════════════════════════════════════════╗
#║ ____        __      _                        ║
#║|  _ \ _ __ /_/  ___| |_ __ _ _ __ ___   ___  ║
#║| |_) | '__/ _ \/ __| __/ _` | '_ ` _ \ / _ \ ║
#║|  __/| | |  __/\__ \ || (_| | | | | | | (_) |║
#║|_|   |_|  \___||___/\__\__,_|_| |_| |_|\___/ ║
#╚══════════════════════════════════════════════╝
class Prestamo(TimestampedModel):
    """
    Modelo para representar un préstamo con todos sus detalles relevantes,
    como el monto, tasa de interés y el prestamista.
    """
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    fecha_inicio = models.DateField()

    usuario_prestamista = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prestamos')
    estado = models.BooleanField(default=False)  # Indica si la deuda está saldada o no

    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"

    def clean(self):
        # Validar que la fecha de inicio no sea en el futuro
        if self.fecha_inicio > datetime.now().date():
            raise ValidationError('La fecha de inicio no puede ser futura.')

    def __str__(self):
        estado_texto = "Saldado" if self.estado else "Pendiente"
        return f"Préstamo: {self.monto_total} - Prestamista: {self.usuario_prestamista} - Estado: {estado_texto}"

#╔══════════════════════════════╗
#║ ____                 _       ║
#║|  _ \  ___ _   _  __| | __ _ ║
#║| | | |/ _ \ | | |/ _` |/ _` |║
#║| |_| |  __/ |_| | (_| | (_| |║
#║|____/ \___|\__,_|\__,_|\__,_|║
#╚══════════════════════════════╝
class Deuda(TimestampedModel):
    DEUDA_TIPO_CHOICES = (
        ('usuario', 'Usuario'),
        ('tarjeta', 'Tarjeta de Crédito'),
        ('prestamo', 'Préstamo'),
    )
    
    usuario_deudor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deudas_deudor')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tipo_deuda = models.CharField(max_length=20, choices=DEUDA_TIPO_CHOICES)
    estado = models.BooleanField(default=False)  # Indica si la deuda está saldada o no
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    tarjeta = models.ForeignKey(CuentaBancaria, on_delete=models.SET_NULL, null=True, blank=True)
    prestamo = models.ForeignKey(Prestamo, on_delete=models.SET_NULL, null=True, blank=True)

    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()

    class Meta:
        ordering = ['fecha_vencimiento']
        verbose_name = "Deuda"
        verbose_name_plural = "Deudas"

    def clean(self):
        # Asegúrate de que la fecha de vencimiento sea posterior a la fecha de creación
        if self.fecha_vencimiento <= self.fecha_creacion:
            raise ValidationError('La fecha de vencimiento debe ser posterior a la fecha de creación.')

    def __str__(self):
        estado_texto = "Saldada" if self.estado else "Pendiente"
        return f"{self.usuario_deudor} debe {self.monto} - Tipo: {self.tipo_deuda} - Estado: {estado_texto}"