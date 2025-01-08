from django.contrib import admin
from .models import Wallet, Income_type, Spending_type, Income, Spending

class WalletAdmin(admin.ModelAdmin):
    list_display = ('w_name', 'w_ticker', 'w_type', 'w_bank', 'initial_balance')
    list_display_links = ('w_name', 'w_ticker')
    search_fields = ('w_name', 'w_ticker')

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('date', 'debit', 'source', 'comment', 'income_type', 'wallet')
    list_display_links = ('debit', 'income_type', 'wallet')
    search_fields = ('date', 'debit', 'source', 'comment', 'income_type', 'wallet')

class SpendingAdmin(admin.ModelAdmin):
    list_display = ('date', 'credit', 'destination', 'comment', 'spending_type')
    list_display_links = ('credit', 'spending_type')
    search_fields = ('date', 'credit', 'destination', 'comment', 'spending_type')


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Income_type)
admin.site.register(Spending_type)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Spending, SpendingAdmin)
