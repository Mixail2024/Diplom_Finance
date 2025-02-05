from django.contrib import admin
from .models import Wallet, Income, Spending, Income_type, Spending_type, Info, Rates


class WalletAdmin(admin.ModelAdmin):
    list_display = ('f_name', 'w_ticker', 'w_type', 'w_bank', 'w_date', 'w_balance', 'w_limit', 'user')
    list_display_links = ('f_name', 'w_ticker')
    search_fields = ('f_name', 'w_ticker')

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('date', 'debit', 'source', 'comment', 'income_type', 'wallet', 'user')
    list_display_links = ('debit', 'income_type', 'wallet')
    search_fields = ('date', 'debit', 'source', 'comment', 'income_type', 'wallet')

class IncomeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_display_links = ('name', 'user')

class SpendingAdmin(admin.ModelAdmin):
    list_display = ('date', 'credit', 'destination', 'comment', 'spending_type', 'wallet', 'user')
    list_display_links = ('credit', 'spending_type', 'wallet')
    search_fields = ('date', 'credit', 'destination', 'comment', 'spending_type', 'wallet')

class SpendingTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_display_links = ('name', 'user')

class InfoAdmin(admin.ModelAdmin):
    list_display = ('init_date', 'final_date', 'user')

class RatesAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'buy', 'sell', 'source', 'user')



admin.site.register(Wallet, WalletAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Spending, SpendingAdmin)
admin.site.register(Income_type, IncomeTypeAdmin)
admin.site.register(Spending_type, SpendingTypeAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(Rates, RatesAdmin)