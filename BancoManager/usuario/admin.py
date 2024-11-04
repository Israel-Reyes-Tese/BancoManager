from django.contrib import admin
from .models import usuario
# Register your models here.

@admin.register(usuario)
class usuario_admin(admin.ModelAdmin):
    list_display = ('id','username','email','is_staff','is_active','is_superuser','last_login','date_joined')
    search_fields = ('username','email','is_staff','is_active','is_superuser','last_login','date_joined')
    list_filter = ('username','email','is_staff','is_active','is_superuser','last_login','date_joined')
    ordering = ('username','email','is_staff','is_active','is_superuser','last_login','date_joined')
    date_hierarchy = 'date_joined'
    verbose_name = "Usuario"
    verbose_name_plural = "Usuarios"
    search_fields = ('username','email')
