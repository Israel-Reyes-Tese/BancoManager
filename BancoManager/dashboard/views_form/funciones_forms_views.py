from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from django.http import JsonResponse

def validar_inconsistencias(form, modelo_principal):
    if modelo_principal == 'Deuda':
        pass

def is_admin(user):
    if user.is_superuser:
        return True
    

def guardar_formulario_data_preterminada(form_model, request, modelo_principal, data_adicional={}):
    if request.method == 'POST':
        # Crear un nuevo formulario con los datos adicionales y data preterminada
        try:
            form_model.objects.create(**data_adicional)
            return JsonResponse({'success': True,
                                    'message': f'{modelo_principal} creado correctamente.'
                                    })
        except Exception as e:
            messages.error(request, 'Error al guardar el ingreso', e)
            return JsonResponse({'success': False,
                                    'message': f'Error al guardar el {modelo_principal}.'
                                    })


def guardar_formulario_post(form_model, request, modelo_principal, vista_redireccion, nombre_template):
    if request.method == 'POST':
        form = form_model(request.POST)
        print("Formulario recibido modelo METOD POST", modelo_principal)
        try:
            if form.is_valid():
                print("Formulario válido")
                # Agregar el usuario al formulario
                form = form.save(commit=False)
                form.usuario = request.user
                try:
                    form.save()
                except Exception as e:
                    messages.error(request, 'Error al guardar el ingreso', e)
                # Limpiar el formulario
                form = form_model()
                return redirect(vista_redireccion)
            else:
                # Imprimir errores en consola
                print("Formulario inválido", form.errors)
        except Exception as e:
            messages.error(request, 'Error al guardar el ingreso', e)

    else:
        print("Formulario no recibido", form_model)
        form = form_model()
    return render(request, f'form/create/{nombre_template}.html', {'form': form
                                                 , 'modelo_principal': modelo_principal})


def guardar_formulario_post_sin_user(form_model, request, modelo_principal, vista_redireccion, nombre_template):
    if request.method == 'POST':
        form = form_model(request.POST)
        print("Formulario recibido modelo", modelo_principal)
        try:
            if form.is_valid():
                print("Formulario válido")
                # Agregar el usuario al formulario
                form = form.save(commit=False)
                try:
                    form.save()
                except Exception as e:
                    messages.error(request, 'Error al guardar el ingreso', e)
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
    

# Editar formulario
def editar_formulario_get_or_post(form_model, request, app_label, template_name, modelo_principal, pk, vista_redireccion):
    applicacion = get_object_or_404(app_label, pk=pk)
    if request.method == 'POST':
        form = form_model(request.POST, instance=applicacion)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                messages.error(request, 'Error al guardar el ingreso', e)
            # Cerrar la vista y redirigir a la vista principal a la url 'api/editar_ingreso/pk/
            return redirect(vista_redireccion, pk=pk)
    else:
        form = form_model(instance=applicacion)
    return render(request, f'form/create/{template_name}.html', {
                                                                'form': form,
                                                                'id_formulario': pk,
                                                                'applicacion': applicacion,
                                                                'modelo_principal': modelo_principal
                                                                })

# Eliminar registro

def eliminar_registro_Get_or_post(request, app_label, pk, vista_redireccion, modelo_principal):
    registro = get_object_or_404(app_label, pk=pk)
    try:
        registro.delete()
    except Exception as e:
        messages.error(request, 'Error al eliminar el registro', e)
    return JsonResponse({'success': True,
                         'message': f'{registro} eliminado correctamente.'
                         })
