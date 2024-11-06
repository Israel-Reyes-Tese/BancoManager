from django.conf import settings
from django.db import models
#╔═══════════════════════════════════════════════════════════════════════════════╗
#║ _____          _      _              _         ____       __     _ _ _        ║
#║|_   _|_ _ _ __(_) ___| |_ __ _    __| | ___   / ___|_ __ /_/  __| (_) |_ ___  ║
#║  | |/ _` | '__| |/ _ \ __/ _` |  / _` |/ _ \ | |   | '__/ _ \/ _` | | __/ _ \ ║
#║  | | (_| | |  | |  __/ || (_| | | (_| |  __/ | |___| | |  __/ (_| | | || (_) |║
#║  |_|\__,_|_| _/ |\___|\__\__,_|  \__,_|\___|  \____|_|  \___|\__,_|_|\__\___/ ║
#║             |__/                                                              ║
#╚═══════════════════════════════════════════════════════════════════════════════╝
class TarjetaCredito(models.Model):
    numero_tarjeta = models.CharField(max_length=16, unique=True)
    nombre_titular = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField()
    colorIdentificacion = models.CharField(max_length=20)
    limite = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Tarjeta: {self.numero_tarjeta} - Titular: {self.nombre_titular}"

#╔══════════════════════════════════════════════╗
#║ ____        __      _                        ║
#║|  _ \ _ __ /_/  ___| |_ __ _ _ __ ___   ___  ║
#║| |_) | '__/ _ \/ __| __/ _` | '_ ` _ \ / _ \ ║
#║|  __/| | |  __/\__ \ || (_| | | | | | | (_) |║
#║|_|   |_|  \___||___/\__\__,_|_| |_| |_|\___/ ║
#╚══════════════════════════════════════════════╝
class Prestamo(models.Model):
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)  
    fecha_inicio = models.DateField()
    usuario_prestamista = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prestamos')

    def __str__(self):
        return f"Préstamo: {self.monto_total} - Prestamista: {self.usuario_prestamista}"

#╔══════════════════════════════╗
#║ ____                 _       ║
#║|  _ \  ___ _   _  __| | __ _ ║
#║| | | |/ _ \ | | |/ _` |/ _` |║
#║| |_| |  __/ |_| | (_| | (_| |║
#║|____/ \___|\__,_|\__,_|\__,_|║
#╚══════════════════════════════╝
class Deuda(models.Model):
    DEUDA_TIPO_CHOICES = (
        ('usuario', 'Usuario'),
        ('tarjeta', 'Tarjeta de Crédito'),
        ('prestamo', 'Préstamo'),
    )
    
    usuario_deudor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deudas_deudor')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_deuda = models.CharField(max_length=20, choices=DEUDA_TIPO_CHOICES)
    estado = models.BooleanField(default=False)  # Indica si la deuda está saldada o no
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    tarjeta = models.ForeignKey(TarjetaCredito, on_delete=models.SET_NULL, null=True, blank=True)
    prestamo = models.ForeignKey(Prestamo, on_delete=models.SET_NULL, null=True, blank=True)

    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(default='2022-01-01')

    def __str__(self):
        return f"{self.usuario_deudor} debe {self.monto} - Tipo: {self.tipo_deuda}"