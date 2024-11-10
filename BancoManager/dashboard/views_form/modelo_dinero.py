# views.py
from ..forms.modelo_dinero import IngresoForm, EgresoForm
from django.contrib.auth.decorators import login_required

from .funciones_forms_views import guardar_formulario_post


@login_required
def crear_ingreso(request):
    return guardar_formulario_post(IngresoForm, request, 'Ingreso', 'crear_ingreso', 'ingreso')

@login_required
def crear_egreso(request):
    return guardar_formulario_post(EgresoForm, request, 'Egreso', 'crear_egreso', 'egreso')