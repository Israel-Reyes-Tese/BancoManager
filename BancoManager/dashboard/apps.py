from django.apps import AppConfig
class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    def ready(self):
        import  dashboard.signals.signals_modelos # Importa las señales para registrarlas automáticamen
