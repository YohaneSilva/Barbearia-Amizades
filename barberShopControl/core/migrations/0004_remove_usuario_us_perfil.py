# Generated by Django 3.0.5 on 2020-05-06 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200506_0905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='us_perfil',
        ),
    ]
