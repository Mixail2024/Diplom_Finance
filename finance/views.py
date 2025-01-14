from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Sum
from decimal import Decimal
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Wallet, Income, Income_type, Spending, Spending_type
from .forms import (
    Form_create_wlt,
    Form_add_income, Form_update_income,
    Form_add_income_type, Form_update_income_type,
    Form_add_spending, Form_update_spending,
    Form_add_spending_type, Form_update_spending_type
    )
from django.utils.timezone import datetime



#=========================================================================================================_H O M E
def home(request):
    wlts = Wallet.objects.order_by('w_name')
    return render(request, 'finance/home.html', {'wlts':wlts})

def home_wlt(request, w_pk):
    current_wlt = Wallet.objects.get(pk=w_pk)
    return render(request, 'finance/home_wlt.html', {'current_wlt':current_wlt})


#========================================================================================================W A L L E T
class Create_wlt(CreateView):#____________________________________________Create_wlt
    model = Wallet
    form_class = Form_create_wlt
    template_name = 'finance/tmplt_create_wlt.html'
    success_url = reverse_lazy('home')


class Update_wlt(UpdateView):#____________________________________________Update_wlt
    model = Wallet
    form_class = Form_create_wlt
    template_name = 'finance/tmplt_update_wlt.html'
    def get_success_url(self):
        w_pk = self.kwargs['pk']  # Получаем pk текущей записи из URL
        return reverse_lazy('home_wlt', kwargs={'w_pk': w_pk})


class Delete_wlt(DeleteView):#_______________________________________________Delete_wlt
    model = Wallet
    template_name = 'finance/tmplt_delete_wlt.html'
    success_url = reverse_lazy('home')
    # Переопределим метод GET для отображения подтверждения на той же странице
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(object=self.object))
    # Переопределим метод POST для удаления
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(self.get_context_data(deleted=True))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        return context

#================================================================================================C A L E N D A R
def calendar_view(request, pk):
    current_wlt = Wallet.objects.get(pk=pk)
    initial_balance = current_wlt.initial_balance
    context = {}
    if request.method == 'GET':
        choice = request.GET.get("choice")

        if choice == "date":#_____________________________________________________________________date
            single_date = request.GET.get("single_date")
            context['single_date'] = single_date

            filtered_dt = Income.objects.filter(wallet=current_wlt, date=single_date)
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')

            filtered_ct = Spending.objects.filter(wallet=current_wlt, date=single_date)
            filtered_ct_sum = filtered_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')


        elif choice == "period":#_____________________________________________________________________period
            start_date = request.GET.get("start_date")
            end_date = request.GET.get("end_date")
            context['start_date'] = start_date
            context['end_date'] = end_date

            filtered_dt = Income.objects.filter(wallet=current_wlt, date__range=[start_date, end_date])
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')

            filtered_ct = Spending.objects.filter(wallet=current_wlt, date__range=[start_date, end_date])
            filtered_ct_sum = filtered_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')


        elif choice == "month_year":#_____________________________________________________________________month_year
            month = request.GET.get("month")
            year = request.GET.get("year")
            context['month'] = month
            context['year'] = year

            filtered_dt = Income.objects.filter(wallet=current_wlt, date__year=year, date__month=month)
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')


            filtered_ct = Spending.objects.filter(wallet=current_wlt, date__year=year, date__month=month)
            filtered_ct_sum = filtered_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')


        elif choice == "year_only":#_____________________________________________________________________year_only
            year_only = request.GET.get("year_only")
            context['year_only'] = year_only

            filtered_dt = Income.objects.filter(wallet=current_wlt, date__year=year_only)
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')

            filtered_ct = Spending.objects.filter(wallet=current_wlt, date__year=year_only)
            filtered_ct_sum = filtered_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')

    # ___________________________________________________________________________________________________ContexT
    context['wlt_pk'] = pk
    context['current_wlt'] = current_wlt
    context['initial_balance'] = initial_balance

    context['filtered_dt'] = filtered_dt
    context['filtered_dt_sum'] = "{:.2f}".format(filtered_dt_sum)

    context['filtered_ct'] = filtered_ct
    context['filtered_ct_sum'] = "{:.2f}".format(filtered_ct_sum)

    context['dtct_sum'] = filtered_dt_sum + filtered_ct_sum

    context['final_balance'] = initial_balance + filtered_dt_sum - filtered_ct_sum

    # print('request', request.GET)
    # print('context', context)
    return render(request, 'finance/home_wlt.html', context)



#=======================================================================================================I N C O M E
def add_income(request, w_pk):#_______________________________________________add_income
    message = ''
    current_wlt = Wallet.objects.get(pk=w_pk)
    form = Form_add_income(request.POST or None, prefix="form_income")
    if form.is_valid():
        income = form.save(commit=False)
        income.wallet = current_wlt
        income.save()
        # Получаем все параметры из request.GET и добавляем их к URL
        get_params = request.GET.urlencode()
        return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{get_params}')

    return render(request, 'finance/tmplt_add_income.html', {'form': form, 'w_pk': w_pk, 'current_wlt':current_wlt, 'message':message})


def update_income(request, w_pk, income_pk):#_____________________________________________Update_income
    record = get_object_or_404(Income, pk=income_pk)
    if request.method == 'POST':
        form = Form_update_income(request.POST, instance=record)
        if form.is_valid():
            form.save()
            # Получаем все параметры из request.GET и добавляем их к URL
            get_params = request.GET.urlencode()
            return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{get_params}')
    else:
        form = Form_update_income(instance=record)

    return render(request, 'finance/tmplt_update_income.html', {
        'form': form,
        'w_pk': w_pk,
        'record': record,
    })


def add_income_type(request, w_pk):#_________________________________________add_income_type
    current_wlt = get_object_or_404(Wallet, pk=w_pk)
    message = None
    form = Form_add_income_type(request.POST or None, prefix="form")
    if form.is_valid():
        if "delete" in request.POST:
            selected_item = form.cleaned_data.get("choices")
            if selected_item:
                selected_item.delete()
                message = f"'{selected_item}' deleted successfully"
        elif "edit" in request.POST:
            selected_item = form.cleaned_data.get("choices")
            if selected_item:
               return redirect('update_income_type', w_pk=w_pk, pk=selected_item.pk)
        elif "add" in request.POST:
            new_value = form.cleaned_data.get("new_value")
            if new_value:
                if not Income_type.objects.filter(name=new_value).exists():
                    Income_type.objects.create(name=new_value)
                    message = f"'{new_value}' added successfully"
                    form = Form_add_income_type(prefix="form")  # Очищаем форму после добавления
                else:
                    message = f"'{new_value}' already exists"
        elif "add_exit" in request.POST:
            new_value = form.cleaned_data.get("new_value")
            if new_value:
                if not Income_type.objects.filter(name=new_value).exists():
                    Income_type.objects.create(name=new_value)
                    message = f"'{new_value}' added successfully"
                else:
                    message = f"'{new_value}' already exists"
            return redirect('add_income', w_pk=w_pk)
    # Возвращаем страницу с формой и возможным сообщением
    return render(request, 'finance/tmplt_add_income_type.html', {
        'form': form,
        'w_pk': w_pk,
        'current_wlt': current_wlt,
        'message': message
    })

class Update_income_type(UpdateView):#_________________________________________Update_income_type
    model = Income_type
    form_class = Form_update_income_type
    template_name = 'finance/tmplt_update_income_type.html'
    def get_success_url(self):
        w_pk = self.kwargs['w_pk']
        current_wlt = Wallet.objects.get(pk=w_pk)
        return reverse_lazy('home_wlt', kwargs={'w_pk': w_pk})



#====================================================================================================S P E N D I N G
def add_spending(request, w_pk):#_______________________________________________add_spending
    message = ''
    current_wlt = Wallet.objects.get(pk=w_pk)
    form_spending = Form_add_spending(request.POST or None, prefix="form_spending")
    if form_spending.is_valid():
        spending = form_spending.save(commit=False)
        spending.wallet = current_wlt
        spending.save()
        # Получаем все параметры из request.GET и добавляем их к URL
        get_params = request.GET.urlencode()
        return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{get_params}')
    return render(request, 'finance/tmplt_add_spending.html', {'form_spending': form_spending, 'w_pk': w_pk, 'current_wlt':current_wlt, 'message':message})


def update_spending(request, w_pk, spending_pk):  # _____________________________________________Update_spending
    record = get_object_or_404(Spending, pk=spending_pk)

    if request.method == 'POST':
        form = Form_update_spending(request.POST, instance=record)
        if form.is_valid():
            form.save()
            # Получаем все параметры из request.GET и добавляем их к URL
            get_params = request.GET.urlencode()
            return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{get_params}')
    else:
        form = Form_update_spending(instance=record)

    return render(request, 'finance/tmplt_update_spending.html', {
        'form': form,
        'w_pk': w_pk,
        'record': record,
    })


def add_spending_type(request, w_pk):#_________________________________________add_spending_type
    current_wlt = get_object_or_404(Wallet, pk=w_pk)
    message = None
    form = Form_add_spending_type(request.POST or None, prefix="form")
    if form.is_valid():
        if "delete" in request.POST:
            selected_item = form.cleaned_data.get("choices")
            if selected_item:
                selected_item.delete()
                message = f"'{selected_item}' deleted successfully"
        elif "edit" in request.POST:
            selected_item = form.cleaned_data.get("choices")
            if selected_item:
               return redirect('update_spending_type', w_pk=w_pk, pk=selected_item.pk)
        elif "add" in request.POST:
            new_value = form.cleaned_data.get("new_value")
            if new_value:
                if not Spending_type.objects.filter(name=new_value).exists():
                    Spending_type.objects.create(name=new_value)
                    message = f"'{new_value}' added successfully"
                    form = Form_add_spending_type(prefix="form")  # Очищаем форму после добавления
                else:
                    message = f"'{new_value}' already exists"
        elif "add_exit" in request.POST:
            new_value = form.cleaned_data.get("new_value")
            if new_value:
                if not Spending_type.objects.filter(name=new_value).exists():
                    Spending_type.objects.create(name=new_value)
                    message = f"'{new_value}' added successfully"
                else:
                    message = f"'{new_value}' already exists"
            return redirect('add_spending', w_pk=w_pk)
    # Возвращаем страницу с формой и возможным сообщением
    return render(request, 'finance/tmplt_add_spending_type.html', {
        'form': form,
        'w_pk': w_pk,
        'current_wlt': current_wlt,
        'message': message
    })

class Update_spending_type(UpdateView):#_________________________________________Update_spending_type
    model = Spending_type
    form_class = Form_update_spending_type
    template_name = 'finance/tmplt_update_spending_type.html'
    def get_success_url(self):
        w_pk = self.kwargs['w_pk']
        current_wlt = Wallet.objects.get(pk=w_pk)
        return reverse_lazy('home_wlt', kwargs={'w_pk': w_pk})










