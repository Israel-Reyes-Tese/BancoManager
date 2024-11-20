from django.db import models
from django.conf import settings
# Importar el date time
from datetime import datetime
# +===========================================================================================================+
from ..modelo_abstract.model_abstract import TimestampedModel
# +===========================================================================================================+
from django.core.validators import RegexValidator, MinValueValidator
# +===========================================================================================================+
tipo_cuenta = (
    ('Credito', 'Crédito'),
    ('Debito', 'Débito'),
    ('Cheques', 'Cheques'),
)

tipo_cuentas = (
    ('Visa', 'Visa'),
    ('MasterCard', 'MasterCard'),
    ('American Express', 'American Express'),
    ('Discover', 'Discover'),
    ('Otra', 'Otra'),
)
#╔═════════════════════════════════════════════════════════════════════╗
#║ ____    _    _   _  ____ ___    __  __  ___  ____  _____ _     ___  ║
#║| __ )  / \  | \ | |/ ___/ _ \  |  \/  |/ _ \|  _ \| ____| |   / _ \ ║
#║|  _ \ / _ \ |  \| | |  | | | | | |\/| | | | | | | |  _| | |  | | | |║
#║| |_) / ___ \| |\  | |__| |_| | | |  | | |_| | |_| | |___| |__| |_| |║
#║|____/_/   \_\_| \_|\____\___/  |_|  |_|\___/|____/|_____|_____\___/ ║
#╚═════════════════════════════════════════════════════════════════════╝
class Banco(TimestampedModel):
    """
    Modelo para representar un banco con su nombre, dirección y teléfono.
    """
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, validators=[
        RegexValidator(r'^\+?1?\d{9,15}$', 'El número de teléfono debe ser de 9 a 15 dígitos.')])
    fechaIngreso = models.DateTimeField(auto_now_add=True)

    cobro_pago_minimo = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    cobro_mantenimiento = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    ultima_fecha_actualizacion = models.DateTimeField(default=datetime.now)
    class Meta:
        ordering = ['nombre']
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self):
        return f"{self.nombre} - Tel: {self.telefono}"
    


class TasaInteres(models.Model):
    """
    Modelo para representar las tasas de interés aplicadas por el banco por diferentes períodos.
    """
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, related_name='tasas_interes')
    meses = models.PositiveIntegerField()  # Número de meses
    porcentaje_interes = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])  # Porcentaje de interés

    fechaCorte = models.DateField(default=datetime.now)
    fechaLimite = models.DateField(default=datetime.now)
    class Meta:
        unique_together = ('banco', 'meses')  # Asegura que no se repitan tasas por el mismo número de meses para un banco
        ordering = ['banco', 'meses']
        verbose_name = "Tasa de Interés"
        verbose_name_plural = "Tasas de Interés"

    def __str__(self):
        return f"Tasa de {self.porcentaje_interes}% por {self.meses} meses para {self.banco.nombre}"
    
#╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#║  ____ _   _ _____ _   _ _____  _      ____    _    _   _  ____    _    ____  ___ ___    __  __  ___  ____  _____ _     ___  ║
#║ / ___| | | | ____| \ | |_   _|/ \    | __ )  / \  | \ | |/ ___|  / \  |  _ \|_ _/ _ \  |  \/  |/ _ \|  _ \| ____| |   / _ \ ║
#║| |   | | | |  _| |  \| | | | / _ \   |  _ \ / _ \ |  \| | |     / _ \ | |_) || | | | | | |\/| | | | | | | |  _| | |  | | | |║
#║| |___| |_| | |___| |\  | | |/ ___ \  | |_) / ___ \| |\  | |___ / ___ \|  _ < | | |_| | | |  | | |_| | |_| | |___| |__| |_| |║
#║ \____|\___/|_____|_| \_| |_/_/   \_\ |____/_/   \_\_| \_|\____/_/   \_\_| \_\___\___/  |_|  |_|\___/|____/|_____|_____\___/ ║
#╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

class CuentaBancaria(TimestampedModel):
    """
    Modelo para representar una cuenta bancaria, incluyendo
    detalles sobre el tipo de cuenta, saldo y afiliación.
    """
    nombre = models.CharField(max_length=100)
    numeroCuenta = models.CharField(max_length=20, unique=True)
    tipoCuenta = models.CharField(max_length=10, choices=tipo_cuenta)
    afilacion  = models.CharField(max_length=20, choices=tipo_cuentas, default='Otra')

    colorIdentificacion = models.CharField(max_length=20)

    saldoInicial = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    saldoActual = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, related_name='cuentas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cuentas_bancarias')

    cvc = models.CharField(max_length=3, validators=[RegexValidator(r'^\d{3}$', 'El CVC debe ser un número de 3 dígitos.')], blank=True, null=True, default='000')
    fechaVencimiento = models.DateField(blank=True, null=True)

    fechaIngreso = models.DateTimeField(auto_now_add=True)

    logo = models.ImageField(upload_to='cuentas/', blank=True, null=True)
    class Meta:
        ordering = ['nombre']
        verbose_name = "Cuenta Bancaria"
        verbose_name_plural = "Cuentas Bancarias"

    def __str__(self):
        return f"{self.nombre} - {self.numeroCuenta} - Banco: {self.banco.nombre}"