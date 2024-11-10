from django import forms
from django.conf import settings
from usuario.models import usuario 
# 
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
        }
        help_texts = {
            'username': None,
        }
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'password': 'Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }
        error_messages = {
            'username': {
                'unique': 'El nombre de usuario ya existe.',
            },
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'password': 'La contraseña debe tener al menos 8 caracteres.',
        }
        labels = {
            'password': 'Contraseña',
        }
