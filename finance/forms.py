from .models import Wallet, Income, Income_type, Spending, Spending_type, Info
from django import forms


#========================================================================================================W A L L E T S
class Form_create_wlt(forms.ModelForm):#__________________________________________Form_create_wlt
    w_date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}), input_formats=['%Y-%m-%d'])
    class Meta:
        model = Wallet
        fields = ['w_name', 'w_ticker', 'w_type', 'w_bank', 'w_date', 'w_balance', 'w_limit']
    def __init__(self, *args, **kwargs):
        super(Form_create_wlt, self).__init__(*args, **kwargs)
        # Установка стиля для конкретного поля
        self.fields['w_name'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['w_ticker'].widget.attrs.update({'style': 'width: 50px;'})
        self.fields['w_bank'].widget.attrs.update({'style': 'width: 200;'})




class Form_delete_wlt(forms.ModelForm):#__________________________________________Form_delete_wlt
    class Meta:
        model = Wallet
        fields = ['w_name', 'w_ticker', 'w_type', 'w_bank', 'w_date', 'w_balance', 'w_limit']




class Form_set_date_init_bal(forms.ModelForm):
    init_date = forms.DateField(
        widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}),
        input_formats=['%Y-%m-%d']
    )
    final_date = forms.DateField(
        widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}),
        input_formats=['%Y-%m-%d']
    )
    class Meta:
        model = Info
        fields = ['init_date', 'final_date']


#=====================================================================================================I N C O M E


class Form_add_income(forms.ModelForm):#___________________________________________Form_add_income
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}), input_formats=['%Y-%m-%d'])
    debit = forms.DecimalField(label='Sum', widget=forms.TextInput(attrs={'placeholder': 'Enter sum'}))
    class Meta:
        model = Income
        fields = ['date', 'debit', 'source', 'comment', 'income_type']
    def __init__(self, *args, user=None, **kwargs):
        super(Form_add_income, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['debit'].widget.attrs.update({'style': 'width: 150px;'})
        self.fields['source'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['comment'].widget.attrs.update({'style': 'width: 200px; height:50px; padding:5px'})
        self.fields['income_type'].widget.attrs.update({'style': 'width: 150;'})
        self.fields['income_type'].queryset = Income_type.objects.filter(user=user)
    def save(self, commit=True):
        income = super().save(commit=False)
        if self.user:
            income.user = self.user
        if commit:
            income.save()
        return income




class Form_update_income(forms.ModelForm):#___________________________________________Form_update_income
    class Meta:
        model = Income
        fields = ['date', 'debit', 'source', 'comment', 'income_type']
    def __init__(self, *args, **kwargs):
        super(Form_update_income, self).__init__(*args, **kwargs)
        # Установка стиля для конкретного поля
        self.fields['source'].widget.attrs.update({'style': 'width: 150px;'})
        self.fields['comment'].widget.attrs.update({'style': 'width: 200px; height: 50px'})



class Form_add_income_type(forms.Form):#______________________________________________Form_add_income_type
    choices = forms.ModelChoiceField(
        queryset=Income_type.objects.none(),
        required=False,
        label="Choose to edit or to delete",
        widget=forms.Select(attrs={'style': 'width: 150px;'}))
    new_value = forms.CharField(
        max_length=255,
        required=False,
        label="Add new",
        widget=forms.TextInput(attrs={'style': 'width: 150px;'}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['choices'].queryset = Income_type.objects.filter(user=user)




class Form_update_income_type(forms.ModelForm):#_______________________________________Form_update_income_type
    class Meta:
        model = Income_type
        fields = ['name']


#======================================================================================================S P E N D I N G
class Form_add_spending(forms.ModelForm):  # __________________________________________________Form_add_spending
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}),
                           input_formats=['%Y-%m-%d'])
    credit = forms.DecimalField(label='Sum', widget=forms.TextInput(attrs={'placeholder': 'Enter sum'}))
    class Meta:
        model = Spending
        fields = ['date', 'credit', 'destination', 'comment', 'spending_type']
    def __init__(self, *args, user=None, **kwargs):
        super(Form_add_spending, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['credit'].widget.attrs.update({'style': 'width: 150px;'})
        self.fields['destination'].widget.attrs.update({'style': 'width: 200px;'})
        self.fields['comment'].widget.attrs.update({'style': 'width: 200px; height:50px; padding:5px'})
        self.fields['spending_type'].widget.attrs.update({'style': 'width: 150;'})
        self.fields['spending_type'].queryset = Spending_type.objects.filter(user=user)
    def save(self, commit=True):
        spending = super().save(commit=False)
        if self.user:
            spending.user = self.user
        if commit:
            spending.save()
        return spending

class Form_update_spending(forms.ModelForm):#___________________________________________Form_update_spending
    class Meta:
        model = Spending
        fields = ['date', 'credit', 'destination', 'comment', 'spending_type']
    def __init__(self, *args, **kwargs):
        super(Form_update_spending, self).__init__(*args, **kwargs)
        self.fields['destination'].widget.attrs.update({'style': 'width: 150px;'})
        self.fields['comment'].widget.attrs.update({'style': 'width: 200px; height: 50px'})

class Form_add_spending_type(forms.Form):#______________________________________________Form_add_spending_type
    choices = forms.ModelChoiceField(
        queryset=Spending_type.objects.none(),
        required=False,
        label="Choose spending type",
        widget=forms.Select(attrs={'style': 'width: 150px;'}))
    new_value = forms.CharField(
        max_length=255,
        required=False,
        label="Add new",
        widget=forms.TextInput(attrs={'style': 'width: 150px;'}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['choices'].queryset = Spending_type.objects.filter(user=user)



class Form_update_spending_type(forms.ModelForm):#_______________________________________Form_update_spending_type
    class Meta:
        model = Spending_type
        fields = ['name']


class TransferForm(forms.Form):#______________________________________________________________Transfer Form
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Choose date'}),
                           input_formats=['%Y-%m-%d'])
    from_wallet = forms.ModelChoiceField(
        empty_label="Select wallet",
        queryset=Wallet.objects.none(),
        required=True,
        label="From wallet",
        widget=forms.Select(attrs={'style': 'width: 150px;'}))
    to_wallet = forms.ModelChoiceField(
        empty_label="Select wallet",
        queryset=Wallet.objects.none(),
        required=True,
        label="To wallet",
        widget=forms.Select(attrs={'style': 'width: 150px;'}))
    amount = forms.DecimalField(label="Amount", max_digits=10, decimal_places=2)
    amount_to = forms.DecimalField(label="Amount to", max_digits=10, decimal_places=2, required=False, show_hidden_initial=False)

    comment = forms.CharField(
        max_length=255,
        required=False,
        label="Comment",
        widget=forms.TextInput(attrs={'style': 'width: 150px;'}))


    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['from_wallet'].queryset = Wallet.objects.filter(user=user)
            self.fields['to_wallet'].queryset = Wallet.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        if amount and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")

        return cleaned_data