# views.py

from django.shortcuts import render, redirect
from ..forms.modelo_dinero import IngresoForm, EgresoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def guardar_formulario_post(form_model, request, modelo_principal, vista_redireccion, nombre_template):
    if request.method == 'POST':
        form = form_model(request.POST)
        print("Formulario recibido modelo", modelo_principal)
        try:
            if form.is_valid():
                print("Formulario válido")
                # Agregar el usuario al formulario
                form = form.save(commit=False)
                form.usuario = request.user
                form.save()
                # Limpiar el formulario
                form = form_model()
                return redirect(vista_redireccion)
            else:
                # Imprimir errores en consola
                print("Formulario inválido", form.errors)
        except Exception as e:
            messages.error(request, 'Error al guardar el ingreso', e)
    else:
        form = form_model()
    return render(request, f'form/create/{nombre_template}.html', {'form': form
                                                 , 'modelo_principal': modelo_principal})

    

@login_required
def crear_ingreso(request):
    return guardar_formulario_post(IngresoForm, request, 'Ingreso', 'crear_ingreso', 'ingreso')

@login_required
def crear_egreso(request):
    return guardar_formulario_post(EgresoForm, request, 'Egreso', 'crear_egreso', 'egreso')