from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class AuditLog(models.Model):
    """
    Modelo para registrar auditorías de cambios en otros modelos,
    incluyendo detalles sobre el modelo afectado, el cambio realizado,
    el usuario que realizó el cambio, y una marca de tiempo.
    """
    ACTION_CHOICES = (
        ('create', 'Creación'),
        ('update', 'Actualización'),
        ('delete', 'Eliminación'),
    )

    model_name = models.CharField(max_length=100)  # Nombre del modelo afectado
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)  # Acción realizada
    record_id = models.PositiveIntegerField()  # ID del registro afectado
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='audit_logs')
    timestamp = models.DateTimeField(auto_now_add=True)  # Marca de tiempo del cambio
    description = models.TextField(blank=True, null=True)  # Descripción opcional del cambio

    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-timestamp']  # Para que se ordenen descendientemente por fecha

    def clean(self):
        """
        Validaciones personalizadas para garantizar que el
        registro de auditoría sea coherente.
        """
        # Verificar que la acción sea válida
        if self.action not in dict(self.ACTION_CHOICES):
            raise ValidationError('La acción debe ser una de las siguientes: create, update, delete.')

        # Verificar que el timestamp no sea en el futuro
        if self.timestamp > timezone.now():
            raise ValidationError('La marca de tiempo no puede ser futura.')

    def __str__(self):
        return f"{self.action.capitalize()} en {self.model_name} - ID: {self.record_id} por {self.user} - Fecha: {self.timestamp}"

