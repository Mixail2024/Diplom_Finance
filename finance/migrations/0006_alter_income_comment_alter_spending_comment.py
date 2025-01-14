# Generated by Django 5.1.4 on 2025-01-14 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_spending_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='comment',
            field=models.TextField(blank=True, max_length=60, null=True, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='spending',
            name='comment',
            field=models.TextField(blank=True, max_length=60, null=True, verbose_name='Comment'),
        ),
    ]
