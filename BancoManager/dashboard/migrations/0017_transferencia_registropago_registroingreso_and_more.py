# Generated by Django 4.2.16 on 2024-11-15 01:03

import dashboard.utils.generales
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0016_alter_banco_options_alter_cuentabancaria_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha_transferencia', models.DateField(default=django.utils.timezone.now)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cuenta_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_destino', to='dashboard.cuentabancaria')),
                ('cuenta_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_origen', to='dashboard.cuentabancaria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transferencia',
                'verbose_name_plural': 'Transferencias',
                'ordering': ['-fecha_transferencia'],
            },
        ),
        migrations.CreateModel(
            name='RegistroPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_pago', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha_pago', models.DateField()),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deuda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_pago', to='dashboard.deuda')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_pago', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Registro de Pago',
                'verbose_name_plural': 'Registros de Pago',
                'ordering': ['-fecha_pago'],
            },
        ),
        migrations.CreateModel(
            name='RegistroIngreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateField()),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('comprobante', models.FileField(blank=True, null=True, upload_to=dashboard.utils.generales.comprobante_upload_to_ingresos)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_ingreso', to='dashboard.cuentabancaria')),
            ],
            options={
                'verbose_name': 'Registro de Ingreso',
                'verbose_name_plural': 'Registros de Ingreso',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='RegistroEgreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateField()),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('comprobante', models.FileField(blank=True, null=True, upload_to=dashboard.utils.generales.comprobante_upload_to_egresos)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_egreso', to='dashboard.cuentabancaria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_egreso', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Registro de Egreso',
                'verbose_name_plural': 'Registros de Egreso',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='ReporteMensual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.PositiveIntegerField()),
                ('año', models.PositiveIntegerField()),
                ('ingresos_total', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('egresos_total', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('saldo_final', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportes_mensuales', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reporte Mensual',
                'verbose_name_plural': 'Reportes Mensuales',
                'ordering': ['-año', '-mes'],
                'unique_together': {('usuario', 'mes', 'año')},
            },
        ),
    ]
