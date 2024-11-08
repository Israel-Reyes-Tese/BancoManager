
from django import forms
from ..models import Ingreso, Egreso  # Asegúrate de importar los modelos correctamente
from ..modelo_banco.models_banco import CuentaBancaria, Banco# Asegúrate de importar los modelos correctamente

from django.conf import settings

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['nombre', 'direccion', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Banco'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }

class CuentaBancariaForm(forms.ModelForm):
    class Meta:
        model = CuentaBancaria
        fields = ['nombre', 'numeroCuenta', 'tipoCuenta', 'afilacion', 'colorIdentificacion', 'saldoInicial', 'saldoActual', 'banco','cvc', 'fechaVencimiento', 'usuario', 'cvc', 'fechaVencimiento']
        widgets = {
                'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Cuenta'}),
                'numeroCuenta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Cuenta'}),
                'tipoCuenta': forms.Select(attrs={'class': 'form-control'}),
                'afilacion': forms.Select(attrs={'class': 'form-control'}),
                'colorIdentificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color de Identificación'}),
                'saldoInicial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Saldo Inicial'}),
                'saldoActual': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Saldo Actual'}),
                'banco': forms.Select(attrs={'class': 'form-control'}),
                'cvc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVC'}),
                'fechaVencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                'usuario': forms.Select(attrs={'class': 'form-control'}),
                'cvc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVC'}),
                'fechaVencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CuentaBancariaForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['usuario'].queryset = settings.AUTH_USER_MODEL.objects.filter(usuario=user)