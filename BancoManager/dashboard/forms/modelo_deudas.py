from django import forms
from django.conf import settings
from ..modelo_deudas.models_deudas import TarjetaCredito, Prestamo, Deuda

class TarjetaCreditoForm(forms.ModelForm):
    class Meta:
        model = TarjetaCredito
        fields = ['numero_tarjeta', 'nombre_titular', 'fecha_vencimiento', 'colorIdentificacion', 'limite']
        widgets = {
            'numero_tarjeta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Tarjeta'}),
            'nombre_titular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Titular'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'colorIdentificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color de Identificación'}),
            'limite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Límite'}),
        }

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['descripcion', 'monto_total', 'tasa_interes', 'fecha_inicio', 'usuario_prestamista']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto Total'}),
            'tasa_interes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tasa de Interés'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'usuario_prestamista': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PrestamoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['usuario_prestamista'].queryset = settings.AUTH_USER_MODEL.objects.filter(usuario=user)

class DeudaForm(forms.ModelForm):
    class Meta:
        model = Deuda
        fields = ['usuario_deudor', 'tipo_deuda', 'monto', 'estado', 'descripcion', 'tarjeta', 'prestamo', 'fecha_vencimiento']
        widgets = {
            'usuario_deudor': forms.Select(attrs={'class': 'form-control'}),
            'tipo_deuda': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'tarjeta': forms.Select(attrs={'class': 'form-control'}),
            'prestamo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DeudaForm, self).__init__(*args, **kwargs)
        if user:
            # Pasamos el usuario para filtrar los usuarios deudores nombrar solo el nombre y excluir el usuario actual
            self.fields['usuario_deudor'].queryset = settings.AUTH_USER_MODEL.objects.filter(usuario=user).exclude(usuario=user)
        # Mostrar el username en lugar del correo 
        self.fields['usuario_deudor'].label_from_instance = lambda obj: "%s" % obj.username