from django.db import models
from django.conf import settings
# Importar el date time
from datetime import datetime


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
class Banco(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    fechaIngreso = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nombre
    
#╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#║  ____ _   _ _____ _   _ _____  _      ____    _    _   _  ____    _    ____  ___ ___    __  __  ___  ____  _____ _     ___  ║
#║ / ___| | | | ____| \ | |_   _|/ \    | __ )  / \  | \ | |/ ___|  / \  |  _ \|_ _/ _ \  |  \/  |/ _ \|  _ \| ____| |   / _ \ ║
#║| |   | | | |  _| |  \| | | | / _ \   |  _ \ / _ \ |  \| | |     / _ \ | |_) || | | | | | |\/| | | | | | | |  _| | |  | | | |║
#║| |___| |_| | |___| |\  | | |/ ___ \  | |_) / ___ \| |\  | |___ / ___ \|  _ < | | |_| | | |  | | |_| | |_| | |___| |__| |_| |║
#║ \____|\___/|_____|_| \_| |_/_/   \_\ |____/_/   \_\_| \_|\____/_/   \_\_| \_\___\___/  |_|  |_|\___/|____/|_____|_____\___/ ║
#╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

class CuentaBancaria(models.Model):
    nombre = models.CharField(max_length=100)
    numeroCuenta = models.CharField(max_length=20, unique=True)
    tipoCuenta = models.CharField(choices=tipo_cuenta)  # Ejemplo: 'Crédito' o 'Débito'
    afilacion = models.CharField(choices=tipo_cuentas, default="Otra")  # Ejemplo: 'Visa', 'MasterCard', 'American Express', 'Discover', 'Otra'
    
    colorIdentificacion = models.CharField(max_length=20)
    
    saldoInicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldoActual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, related_name='cuentas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cuentas_bancarias')

    cvc = models.CharField(max_length=3, blank=True, null=True, default='000')
    fechaVencimiento = models.DateField(blank=True, null=True, default='2022-01-01')

    fechaIngreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.numeroCuenta}"