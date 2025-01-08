from .models import Wallet, Income, Income_type, Spending, Spending_type
from django import forms

class Form_create_wlt(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['w_name', 'w_ticker', 'w_type', 'w_bank', 'initial_balance']

class Form_delete_wlt(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['w_name', 'w_ticker', 'w_type', 'w_bank', 'initial_balance']


class Form_add_income(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}), input_formats=['%d-%m-%Y'])
    debit = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Enter sum'}))
    # income_type = forms.ModelChoiceField(queryset=Income_type.objects.all(), widget=forms.Select(attrs={'style':'height:22px'}))
    class Meta:
        model = Income
        fields = ['date', 'debit', 'source', 'comment', 'income_type']

class Form_add_income_type(forms.Form):
    choices = forms.ModelChoiceField(
        queryset=Income_type.objects.all(),
        required=False,
        label="choose income type")
    new_value = forms.CharField(max_length=255, required=False, label="add new income type")


class Form_add_spending(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}), input_formats=['%d-%m-%Y'])
    class Meta:
        model = Spending
        fields = ['date', 'credit', 'destination', 'comment', 'spending_type']