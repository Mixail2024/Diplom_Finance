from .models import Wallet, Income, Income_type, Spending, Spending_type
from django import forms


#========================================================================================================W A L L E T S
class Form_create_wlt(forms.ModelForm):#__________________________________________Form_create_wlt
    class Meta:
        model = Wallet
        fields = ['w_name', 'w_ticker', 'w_type', 'w_bank', 'initial_balance']
    def __init__(self, *args, **kwargs):
        super(Form_create_wlt, self).__init__(*args, **kwargs)
        # Установка стиля для конкретного поля
        self.fields['w_name'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['w_ticker'].widget.attrs.update({'style': 'width: 50px;'})
        self.fields['w_bank'].widget.attrs.update({'style': 'width: 200;'})


class Form_delete_wlt(forms.ModelForm):#__________________________________________Form_delete_wlt
    class Meta:
        model = Wallet
        fields = ['w_name', 'w_ticker', 'w_type', 'w_bank', 'initial_balance']



#=====================================================================================================I N C O M E
class Form_add_income(forms.ModelForm):#___________________________________________Form_add_income
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}), input_formats=['%d-%m-%Y'])
    debit = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Enter sum'}))
    class Meta:
        model = Income
        fields = ['date', 'debit', 'source', 'comment', 'income_type']
    def __init__(self, *args, **kwargs):
        super(Form_add_income, self).__init__(*args, **kwargs)
        self.fields['debit'].widget.attrs.update({'style': 'width: 150px;'})
        self.fields['source'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['comment'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['income_type'].widget.attrs.update({'style': 'width: 150;'})


class Form_update_income(forms.ModelForm):#___________________________________________Form_update_income
    class Meta:
        model = Income
        fields = ['date', 'debit', 'source', 'comment', 'income_type']


class Form_add_income_type(forms.Form):#______________________________________________Form_add_income_type
    choices = forms.ModelChoiceField(
        queryset=Income_type.objects.all(),
        required=False,
        label="Choose income type",
        widget=forms.Select(attrs={'style': 'width: 150px;'}))
    new_value = forms.CharField(
        max_length=255,
        required=False,
        label="Add new income type",
        widget=forms.TextInput(attrs={'style': 'width: 150px;'}))

class Form_update_income_type(forms.ModelForm):#_______________________________________Form_update_income_type
    class Meta:
        model = Income_type
        fields = ['name']


#======================================================================================================S P E N D I N G
class Form_add_spending(forms.ModelForm):  # __________________________________________________Form_add_spending
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}),
                           input_formats=['%d-%m-%Y'])
    credit = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Enter sum'}))
    class Meta:
        model = Spending
        fields = ['date', 'credit', 'destination', 'comment', 'spending_type']
    def __init__(self, *args, **kwargs):
        super(Form_add_spending, self).__init__(*args, **kwargs)
        self.fields['credit'].widget.attrs.update({'style': 'width: 150px;'})
        self.fields['destination'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['comment'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['spending_type'].widget.attrs.update({'style': 'width: 150;'})


class Form_update_spending(forms.ModelForm):#___________________________________________Form_update_spending
    class Meta:
        model = Spending
        fields = ['date', 'credit', 'destination', 'comment', 'spending_type']

class Form_add_spending_type(forms.Form):#______________________________________________Form_add_spending_type
    choices = forms.ModelChoiceField(
        queryset=Spending_type.objects.all(),
        required=False,
        label="Choose spending type",
        widget=forms.Select(attrs={'style': 'width: 150px;'}))
    new_value = forms.CharField(
        max_length=255,
        required=False,
        label="Add new spending type",
        widget=forms.TextInput(attrs={'style': 'width: 150px;'}))



class Form_update_spending_type(forms.ModelForm):#_______________________________________Form_update_spending_type
    class Meta:
        model = Spending_type
        fields = ['name']

