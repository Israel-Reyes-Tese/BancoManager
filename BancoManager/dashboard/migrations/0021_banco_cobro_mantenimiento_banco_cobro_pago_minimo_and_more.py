# Generated by Django 5.1.3 on 2024-11-19 17:44

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_cuentabancaria_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='banco',
            name='cobro_mantenimiento',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='banco',
            name='cobro_pago_minimo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='banco',
            name='tasa_interes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='banco',
            name='ultima_fecha_actualizacion',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
