# Generated by Django 5.1.4 on 2025-01-06 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='dt',
            new_name='debit',
        ),
        migrations.RenameField(
            model_name='spending',
            old_name='ct',
            new_name='credit',
        ),
        migrations.AddField(
            model_name='wallet',
            name='initial_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Debit'),
        ),
    ]
