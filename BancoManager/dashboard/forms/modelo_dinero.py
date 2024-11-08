
from django import forms
from ..models import Ingreso, Egreso  # Asegúrate de importar los modelos correctamente
from ..modelo_banco.models_banco import CuentaBancaria, Banco# Asegúrate de importar los modelos correctamente

from django.conf import settings


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['cantidad', 'descripcion', 'fecha', 'fuente', 'cuenta']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fuente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fuente'}),
            'cuenta': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(IngresoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['cuenta'].queryset = CuentaBancaria.objects.filter(usuario=user)

class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = ['cantidad', 'descripcion', 'fecha', 'proposito', 'cuenta']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proposito': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Propósito'}),
            'cuenta': forms.Select(attrs={'class': 'form-control'}),
        }