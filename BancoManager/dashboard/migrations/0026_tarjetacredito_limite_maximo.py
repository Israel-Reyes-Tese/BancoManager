# Generated by Django 5.1.3 on 2024-11-20 17:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0025_rename_limite_tarjetacredito_limite_actual'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarjetacredito',
            name='limite_maximo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
