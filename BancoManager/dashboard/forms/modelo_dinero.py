
from django import forms
from ..models import Ingreso, Egreso  # Asegúrate de importar los modelos correctamente

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