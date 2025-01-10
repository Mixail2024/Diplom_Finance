from django.db import models

class Wallet(models.Model):
    W_TYPES = (
        ('a', 'account'),
        ('b', 'bank account'),
        ('c', 'cash'),
        )
    w_name = models.CharField(max_length=20, verbose_name = 'Wallet name')
    w_ticker = models.CharField(max_length=3, verbose_name = 'Currency ticker')
    w_type = models.CharField(max_length=1, choices=W_TYPES, verbose_name = 'Type')
    w_bank = models.CharField(max_length=20, verbose_name = 'Bank name', blank=True)
    initial_balance = models.DecimalField(max_digits=9, decimal_places=2, verbose_name = 'Initial balance', default=0.00)

    def __str__(self):
        return self.w_name

    class Meta:
        verbose_name = 'wallet'
        verbose_name_plural = 'wallets'
        ordering = ['w_name']


class Income(models.Model):
    date = models.DateField(db_index=True, verbose_name = 'Date')
    debit = models.DecimalField(max_digits=9, decimal_places=2, verbose_name = 'Debit')
    source = models.CharField(max_length=20, null=True, blank=True, verbose_name = 'From')
    comment = models.CharField(max_length=20, null=True, blank=True, verbose_name = 'Comment')
    income_type = models.ForeignKey('Income_type', null=True, blank=True, on_delete=models.PROTECT, verbose_name = 'Income Type')
    wallet = models.ForeignKey(Wallet, null=True, blank=True, on_delete=models.PROTECT, verbose_name = 'Wallet')
    class Meta:
        verbose_name = 'income'
        verbose_name_plural = 'incomes'
        ordering = ['date']

class Spending(models.Model):
    date = models.DateField(db_index=True, verbose_name = 'Date')
    credit = models.DecimalField(max_digits=9, decimal_places=2, verbose_name = 'Credit')
    destination = models.CharField(max_length=20, null=True, blank=True, verbose_name = 'To')
    comment = models.CharField(max_length=20, null=True, blank=True, verbose_name = 'Comment')
    spending_type = models.ForeignKey('Spending_type', null=True, blank=True, on_delete=models.PROTECT, verbose_name = 'Spending Type')
    class Meta:
        verbose_name = 'spending'
        verbose_name_plural = 'spendings'
        ordering = ['date']



class Income_type(models.Model):
    name = models.CharField(max_length=30, db_index=True, unique=True, verbose_name ='income type')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'income type'
        verbose_name_plural = 'income types'
        ordering = ['name']

class Spending_type(models.Model):
    name = models.CharField(max_length=30, db_index=True, unique=True,  verbose_name ='spending type')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'spending type'
        verbose_name_plural = 'spending types'
        ordering = ['name']