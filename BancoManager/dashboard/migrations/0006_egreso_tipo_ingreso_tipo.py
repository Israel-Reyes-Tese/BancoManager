# Generated by Django 4.2.16 on 2024-11-06 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_deuda_fecha_vencimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='egreso',
            name='tipo',
            field=models.CharField(default='Egreso', max_length=20),
        ),
        migrations.AddField(
            model_name='ingreso',
            name='tipo',
            field=models.CharField(default='Ingreso', max_length=20),
        ),
    ]
