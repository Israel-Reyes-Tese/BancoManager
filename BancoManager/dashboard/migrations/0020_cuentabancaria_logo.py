# Generated by Django 4.2.16 on 2024-11-17 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_tarjetacredito_cuenta_tarjetacredito_fecha_corte_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentabancaria',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='cuentas/'),
        ),
    ]
