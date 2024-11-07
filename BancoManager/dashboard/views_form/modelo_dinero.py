# views.py

from django.shortcuts import render, redirect
from ..forms.modelo_dinero import IngresoForm, EgresoForm
from django.contrib import messages

def crear_ingreso(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingreso agregado correctamente')
            return redirect('nombre_de_la_vista_donde_rediriges')  # Redirigir a la vista correspondiente
    else:
        form = IngresoForm()
    print(form)
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