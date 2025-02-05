# Generated by Django 5.1.4 on 2025-02-05 07:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Income_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, verbose_name='income type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('init_date', models.DateField(verbose_name='Init date')),
                ('final_date', models.DateField(verbose_name='Final date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('name', models.CharField(db_index=True, max_length=5, verbose_name='Currency')),
                ('buy', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Buy')),
                ('sell', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Sell')),
                ('source', models.URLField(blank=True, max_length=150, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'rate',
                'verbose_name_plural': 'rates',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Spending_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='spending type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('income_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='finance.income_type', verbose_name='Income Type')),
                ('wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.wallet', verbose_name='Wallet')),
            ],
            options={
                'verbose_name': 'income',
                'verbose_name_plural': 'incomes',
                'ordering': ['date'],
            },
        ),
        migrations.AddConstraint(
            model_name='income_type',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_user_name'),
        ),
    ]
