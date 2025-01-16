# Generated by Django 5.1.4 on 2025-01-16 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='debit',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Sum dt'),
        ),
        migrations.AlterField(
            model_name='spending',
            name='credit',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Sum ct'),
        ),
    ]
