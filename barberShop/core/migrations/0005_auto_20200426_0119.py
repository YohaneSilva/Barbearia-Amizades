# Generated by Django 2.2.12 on 2020-04-26 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200426_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='us_situacao_conta',
            field=models.BooleanField(default=1, null=True, verbose_name='Status da conta'),
        ),
    ]
