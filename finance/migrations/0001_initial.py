# Generated by Django 5.1.4 on 2025-01-17 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Income_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='income type')),
            ],
            options={
                'verbose_name': 'income type',
                'verbose_name_plural': 'income types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('init_date', models.DateField(db_index=True, verbose_name='Init Date')),
            ],
        ),
        migrations.CreateModel(
            name='Spending_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='spending type')),
            ],
            options={
                'verbose_name': 'spending type',
                'verbose_name_plural': 'spending types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('w_name', models.CharField(max_length=20, verbose_name='Wallet name')),
                ('w_ticker', models.CharField(max_length=3, verbose_name='Currency ticker')),
                ('w_type', models.CharField(choices=[('a', 'account'), ('b', 'bank account'), ('c', 'cash')], max_length=1, verbose_name='Type')),
                ('w_bank', models.CharField(blank=True, max_length=25, verbose_name='Bank name')),
                ('w_date', models.DateField(db_index=True, verbose_name='Open date')),
                ('w_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Open balance')),
                ('f_name', models.CharField(blank=True, max_length=24, verbose_name='Full wallet name')),
                ('w_limit', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Limit')),
            ],
            options={
                'verbose_name': 'wallet',
                'verbose_name_plural': 'wallets',
                'ordering': ['w_name'],
            },
        ),
        migrations.CreateModel(
            name='Spending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, verbose_name='Date')),
                ('credit', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Sum ct')),
                ('destination', models.CharField(blank=True, max_length=20, null=True, verbose_name='To')),
                ('comment', models.TextField(blank=True, max_length=60, null=True, verbose_name='Comment')),
                ('spending_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='finance.spending_type', verbose_name='Spending Type')),
                ('wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.wallet', verbose_name='Wallet')),
            ],
            options={
                'verbose_name': 'spending',
                'verbose_name_plural': 'spendings',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, verbose_name='Date')),
                ('debit', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Sum dt')),
                ('source', models.CharField(blank=True, max_length=20, null=True, verbose_name='From')),
                ('comment', models.TextField(blank=True, max_length=60, null=True, verbose_name='Comment')),
                ('income_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='finance.income_type', verbose_name='Income Type')),
                ('wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.wallet', verbose_name='Wallet')),
            ],
            options={
                'verbose_name': 'income',
                'verbose_name_plural': 'incomes',
                'ordering': ['date'],
            },
        ),
    ]
