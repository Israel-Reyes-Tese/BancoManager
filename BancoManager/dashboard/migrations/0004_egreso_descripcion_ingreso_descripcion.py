# Generated by Django 4.2.16 on 2024-11-06 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_cuentabancaria_afilacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='egreso',
            name='descripcion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ingreso',
            name='descripcion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
