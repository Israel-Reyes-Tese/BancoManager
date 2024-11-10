from django.db import models
from django.conf import settings

from ..modelo_banco.models_banco import CuentaBancaria

#╔═══════════════════════════════════════════════════════════════════════════════╗
#║ ___ _   _  ____ ____  _____ ____   ___    __  __  ___  ____  _____ _     ___  ║
#║|_ _| \ | |/ ___|  _ \| ____/ ___| / _ \  |  \/  |/ _ \|  _ \| ____| |   / _ \ ║
#║ | ||  \| | |  _| |_) |  _| \___ \| | | | | |\/| | | | | | | |  _| | |  | | | |║
#║ | || |\  | |_| |  _ <| |___ ___) | |_| | | |  | | |_| | |_| | |___| |__| |_| |║
#║|___|_| \_|\____|_| \_\_____|____/ \___/  |_|  |_|\___/|____/|_____|_____\___/ ║
#╚═══════════════════════════════════════════════════════════════════════════════╝

class Ingreso(models.Model):
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateField()
    fuente = models.CharField(max_length=100)
    cuenta = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='ingresos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ingresos')
    tipo = models.CharField(max_length=20, default='Ingreso')
    fechaIngreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ingreso: {self.cantidad} - {self.fecha}"
    
#╔══════════════════════════════════════════════════════════════════════════╗
#║ _____ ____ ____  _____ ____   ___    __  __  ___  ____  _____ _     ___  ║
#║| ____/ ___|  _ \| ____/ ___| / _ \  |  \/  |/ _ \|  _ \| ____| |   / _ \ ║
#║|  _|| |  _| |_) |  _| \___ \| | | | | |\/| | | | | | | |  _| | |  | | | |║
#║| |__| |_| |  _ <| |___ ___) | |_| | | |  | | |_| | |_| | |___| |__| |_| |║
#║|_____\____|_| \_\_____|____/ \___/  |_|  |_|\___/|____/|_____|_____\___/ ║
#╚══════════════════════════════════════════════════════════════════════════╝

class Egreso(models.Model):
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateField()
    proposito = models.CharField(max_length=100)
    cuenta = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='egresos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='egresos')
    tipo = models.CharField(max_length=20, default='Egreso')
    fechaIngreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Egreso: {self.cantidad} - {self.fecha}"    