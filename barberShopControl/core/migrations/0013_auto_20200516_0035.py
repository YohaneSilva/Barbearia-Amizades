# Generated by Django 3.0.5 on 2020-05-16 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_periodo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='per_periodo',
            field=models.CharField(max_length=5, verbose_name='Periodo'),
        ),
    ]