# Generated by Django 3.0.5 on 2020-05-19 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20200519_1843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='res_email',
            new_name='us_email',
        ),
    ]
