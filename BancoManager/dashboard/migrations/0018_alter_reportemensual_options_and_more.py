# Generated by Django 4.2.16 on 2024-11-15 01:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0017_transferencia_registropago_registroingreso_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportemensual',
            options={'ordering': ['-tiempo_anual', '-mes'], 'verbose_name': 'Reporte Mensual', 'verbose_name_plural': 'Reportes Mensuales'},
        ),
        migrations.RenameField(
            model_name='reportemensual',
            old_name='año',
            new_name='tiempo_anual',
        ),
        migrations.AlterUniqueTogether(
            name='reportemensual',
            unique_together={('usuario', 'mes', 'tiempo_anual')},
        ),
    ]
