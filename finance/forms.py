from .models import Wallet, Income, Income_type, Spending, Spending_type
from django import forms

class Form_create_wlt(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['w_name', 'w_ticker', 'w_type', 'w_bank', 'initial_balance']
    def __init__(self, *args, **kwargs):
        super(Form_create_wlt, self).__init__(*args, **kwargs)
        # Установка стиля для конкретного поля
        self.fields['w_name'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['w_ticker'].widget.attrs.update({'style': 'width: 50px;'})
        self.fields['w_bank'].widget.attrs.update({'style': 'width: 200;'})

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
    def __init__(self, *args, **kwargs):
        super(Form_add_income, self).__init__(*args, **kwargs)
        self.fields['debit'].widget.attrs.update({'style': 'width: 150px;'})
        self.fields['source'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['comment'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['income_type'].widget.attrs.update({'style': 'width: 150;'})

class Form_add_income_type(forms.Form):
    choices = forms.ModelChoiceField(
        queryset=Income_type.objects.all(),
        required=False,
        label="Choose income type",
        widget=forms.Select(attrs={'style': 'width: 150px;'})  # Исправлено: используем forms.Select
    )
    new_value = forms.CharField(
        max_length=255,
        required=False,
        label="Add new income type",
        widget=forms.TextInput(attrs={'style': 'width: 150px;'})  # Добавляем стиль для текстового поля
    )
class Form_update_income_type(forms.ModelForm):
    class Meta:
        model = Income_type
        fields = ['name']

class Form_add_spending(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}), input_formats=['%d-%m-%Y'])
    class Meta:
        model = Spending
        fields = ['date', 'credit', 'destination', 'comment', 'spending_type']

class Form_update_income(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'debit', 'source', 'comment', 'income_type']