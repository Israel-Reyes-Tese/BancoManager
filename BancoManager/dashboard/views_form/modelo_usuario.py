# views.py
from ..forms.modelo_usuario import UsuarioForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .funciones_forms_views import guardar_formulario_post_sin_user, is_admin

# Solamente el administrador puede crear usuarios

@login_required 
@user_passes_test(is_admin)
def crear_usuario(request):
    return guardar_formulario_post_sin_user(UsuarioForm, request, 'Usuario', 'crear_usuario', 'usuario')