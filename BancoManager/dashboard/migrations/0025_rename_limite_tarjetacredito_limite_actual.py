# Generated by Django 5.1.3 on 2024-11-20 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_tasainteres_fechalimite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarjetacredito',
            old_name='limite',
            new_name='limite_actual',
        ),
    ]