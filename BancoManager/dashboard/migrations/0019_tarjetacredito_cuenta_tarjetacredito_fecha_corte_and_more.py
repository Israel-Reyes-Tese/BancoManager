# Generated by Django 4.2.16 on 2024-11-15 02:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_alter_reportemensual_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarjetacredito',
            name='cuenta',
            field=models.ForeignKey(default=20, on_delete=django.db.models.deletion.CASCADE, related_name='tarjetas_credito', to='dashboard.cuentabancaria'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarjetacredito',
            name='fecha_corte',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarjetacredito',
            name='fecha_inicio',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarjetacredito',
            name='fecha_limite_pago',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
