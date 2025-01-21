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
    w_bank = models.CharField(max_length=25, verbose_name = 'Bank name', blank=True)
    w_date = models.DateField(db_index=True, verbose_name = 'Open date')
    w_balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name = 'Open balance', default=0.00)
    f_name = models.CharField(max_length=24, blank=True, verbose_name='Full wallet name')
    w_limit = models.DecimalField(max_digits=12, decimal_places=2, verbose_name = 'Limit', default=0.00)
    def save(self, *args, **kwargs):
        self.f_name = f"{self.w_name} {self.w_ticker}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.f_name

    class Meta:
        verbose_name = 'wallet'
        verbose_name_plural = 'wallets'
        ordering = ['w_name']


class Income(models.Model):
    date = models.DateField(db_index=True, verbose_name = 'Date')
    debit = models.DecimalField(max_digits=12, decimal_places=2, verbose_name = 'Sum dt')
    source = models.CharField(max_length=20, null=True, blank=True, verbose_name = 'From')
    comment = models.TextField(max_length=60, null=True, blank=True, verbose_name = 'Comment')
    income_type = models.ForeignKey('Income_type', null=True, blank=True, on_delete=models.PROTECT, verbose_name = 'Income Type')
    wallet = models.ForeignKey(Wallet, null=True, blank=True, on_delete=models.CASCADE, verbose_name = 'Wallet')
    class Meta:
        verbose_name = 'income'
        verbose_name_plural = 'incomes'
        ordering = ['date']
    def save(self, *args, **kwargs):
        if not self.income_type:
            # Устанавливаем значение по умолчанию, если оно не задано
            self.income_type, created = Income_type.objects.get_or_create(name='no type')
        super().save(*args, **kwargs)

class Spending(models.Model):
    date = models.DateField(db_index=True, verbose_name = 'Date')
    credit = models.DecimalField(max_digits=12, decimal_places=2, verbose_name = 'Sum ct')
    destination = models.CharField(max_length=20, null=True, blank=True, verbose_name = 'To')
    comment = models.TextField(max_length=60, null=True, blank=True, verbose_name = 'Comment')
    spending_type = models.ForeignKey('Spending_type', null=True, blank=True, on_delete=models.PROTECT, verbose_name = 'Spending Type')
    wallet = models.ForeignKey(Wallet, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Wallet')
    class Meta:
        verbose_name = 'spending'
        verbose_name_plural = 'spendings'
        ordering = ['date']
    def save(self, *args, **kwargs):
        if not self.spending_type:
            # Устанавливаем значение по умолчанию, если оно не задано
            self.spending_type, created = Spending_type.objects.get_or_create(name='no type')
        super().save(*args, **kwargs)



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


class Info(models.Model):
    init_date = models.DateField(verbose_name='Init date')
    final_date = models.DateField(verbose_name='Final date', default='2025-01-01')


    def save(self, *args, **kwargs):
        if not self.pk:  # Если запись новая (нет pk)
            Info.objects.all().delete()  # Удаляем все существующие записи
        super().save(*args, **kwargs)  # Сохраняем текущую запись