# views.py

from django.shortcuts import render, redirect
from ..forms.modelo_dinero import IngresoForm, EgresoForm
from django.contrib import messages

def crear_ingreso(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        print("Formulario recibido")
        try:
            if form.is_valid():
                print("Formulario válido")
                # Agregar el usuario al formulario
                form = form.save(commit=False)
                form.usuario = request.user
                form.save()
                # Limpiar el formulario
                form = IngresoForm()
                return redirect('crear_ingreso')  # Redirige a la lista de ingresos después de guardar
            else:
                # Imprimir errores en consola
                print("Formulario inválido", form.errors)
        
        except Exception as e:
            messages.error(request, 'Error al guardar el ingreso', e)
    else:
        form = IngresoForm()
    return render(request, 'form/ingreso.html', {'form': form})

def crear_egreso(request):
    if request.method == 'POST':
        form = EgresoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Egreso agregado correctamente')
            return redirect('nombre_de_la_vista_donde_rediriges')
    else:
        form = EgresoForm()
    return render(request, 'form/egreso.html', {'form': form})