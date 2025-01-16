from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Sum
from decimal import Decimal
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Wallet, Income, Income_type, Spending, Spending_type
from .forms import (
    Form_create_wlt, Form_delete_wlt,
    Form_add_income, Form_update_income,
    Form_add_income_type, Form_update_income_type,
    Form_add_spending, Form_update_spending,
    Form_add_spending_type, Form_update_spending_type
    )
from django.utils.timezone import datetime, now



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




def delete_wlt(request, pk):  # ____________________________________________________________Delete_wlt
    current_wlt = get_object_or_404(Wallet, pk=pk)
    form = Form_delete_wlt(request.POST or None, instance=current_wlt)
    recs_income_qty = Income.objects.filter(wallet=current_wlt).count()
    recs_spending_qty = Spending.objects.filter(wallet=current_wlt).count()
    total_qty = recs_income_qty + recs_spending_qty
    message = None
    if request.method == 'POST':
        if 'confirm' in request.POST:
            current_wlt.delete()
            message = f"Wallet '{current_wlt}' deleted successfully"
        if 'cancel' in request.POST:
            get_params = request.GET.urlencode()
            url = reverse_lazy('calendar', kwargs={'pk': pk})
            if get_params:
                url = f"{url}?{get_params}"
                return redirect(url)
            else:
                return redirect(reverse_lazy('home_wlt', kwargs={'w_pk': pk}))
    return render(request, 'finance/tmplt_delete_wlt.html', {
        'form': form,
        'pk': pk,
        'message': message,
        'current_wlt': current_wlt,
        'recs_income_qty': recs_income_qty,
        'recs_spending_qty': recs_spending_qty,
        'total_qty': total_qty
    })



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

    lst = [pk, current_wlt, initial_balance, filtered_dt, filtered_ct]
    for i in lst:
        if not i:
            i = []

    context['wlt_pk'] = pk
    context['current_wlt'] = current_wlt
    context['initial_balance'] = initial_balance

    context['filtered_dt'] = filtered_dt
    context['filtered_dt_count']= filtered_dt.count()
    context['filtered_dt_sum'] = filtered_dt_sum

    context['filtered_ct'] = filtered_ct
    context['filtered_ct_count'] = filtered_ct.count()
    context['filtered_ct_sum'] = filtered_ct_sum

    context['dtct_sum'] = filtered_dt_sum + filtered_ct_sum

    context['final_balance'] = initial_balance + filtered_dt_sum - filtered_ct_sum

    # print('request', request.GET)
    # print('context', context)
    return render(request, 'finance/home_wlt.html', context)


def delete_filtered_dt(request, w_pk):#_________________________________________delete_filtered_dt
    params = request.GET.get('params')
    params = params.replace("*", "&")
    print('params DDt', params)
    lst = request.GET.get('ids')
    lst = lst.split('/')
    lst = [i for i in lst if i.isdigit() and int(i) > 0]
    Income.objects.filter(pk__in=lst).delete()
    return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{params}')

def delete_filtered_ct(request, w_pk):#_________________________________________delete_filtered_ct
    params = request.GET.get('params')
    params= params.replace("*", "&")
    print('params kt', params)
    lst = request.GET.get('ids')
    lst = lst.split('/')
    lst = [i for i in lst if i.isdigit() and int(i) > 0]
    Spending.objects.filter(pk__in=lst).delete()
    return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{params}')



#=======================================================================================================I N C O M E

def add_income(request, w_pk):#_______________________________________________add_income
    message = ''
    current_wlt = Wallet.objects.get(pk=w_pk)
    single_date = request.GET.get('single_date', now().strftime('%Y-%m-%d'))
    form = Form_add_income(request.POST or None, prefix="form", initial={'date': single_date})
    if request.method == 'POST' and form.is_valid():
        income = form.save(commit=False)
        income.wallet = current_wlt
        income.save()
        get_params = request.GET.urlencode()
        if get_params:
           return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{get_params}')
        else:
            return redirect(f'/finance/home_wlt/{w_pk}')

    return render(request, 'finance/tmplt_add_income.html', {'form': form, 'w_pk': w_pk, 'current_wlt':current_wlt, 'message':message, 'single_date':single_date})




def update_income(request, w_pk, income_pk):#_____________________________________________Update_income
    record = get_object_or_404(Income, pk=income_pk)
    if request.method == 'POST':
        form = Form_update_income(request.POST, instance=record)
        if form.is_valid():
            if "delete" in request.POST:
               if record:
                   record.delete()
                   message = f"the record deleted successfully"
                   get_params = request.GET.urlencode()
                   return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{get_params}')
            if "save" in request.POST:
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
               get_params = request.GET.urlencode()
               base_url = reverse('update_income_type', kwargs={'w_pk': w_pk, 'pk': selected_item.pk})
               new_url = f"{base_url}?{get_params}"
               return redirect(new_url)
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


def update_income_type(request, w_pk, pk):#___________________________________________update_income_type
    try:
        income_type = Income_type.objects.get(pk=pk)
    except Income_type.DoesNotExist:
        raise Http404("Income type not found")

    form = Form_update_income_type(request.POST or None, instance=income_type)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            get_params = request.GET.urlencode()
            if get_params:
                return redirect(f'/finance/home_wlt/{w_pk}/add_income_type/?{get_params}')
            else:
               return redirect(f'/finance/home_wlt/{w_pk}/add_income_type/')
        return redirect(f'/finance/home_wlt/{w_pk}')

    # Отображаем форму
    return render(request, 'finance/tmplt_update_income_type.html', {
        'form': form,
        'w_pk': w_pk,
        'income_type': income_type,
    })


#====================================================================================================S P E N D I N G
def add_spending(request, w_pk):#_______________________________________________add_spending
    message = ''
    current_wlt = Wallet.objects.get(pk=w_pk)
    single_date = request.GET.get('single_date', now().strftime('%Y-%m-%d'))
    form = Form_add_spending(request.POST or None, prefix="form", initial={'date': single_date})
    if request.method == 'POST' and form.is_valid():
        spending = form.save(commit=False)
        spending.wallet = current_wlt
        spending.save()
        get_params = request.GET.urlencode()
        if get_params:
           return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{get_params}')
        else:
            return redirect(f'/finance/home_wlt/{w_pk}')

    return render(request, 'finance/tmplt_add_spending.html', {'form': form, 'w_pk': w_pk, 'current_wlt':current_wlt, 'message':message, 'single_date':single_date})


def update_spending(request, w_pk, spending_pk):#_____________________________________________Update_spending
    record = get_object_or_404(Spending, pk=spending_pk)
    if request.method == 'POST':
        form = Form_update_spending(request.POST, instance=record)
        if form.is_valid():
            if "delete" in request.POST:
               if record:
                   record.delete()
                   message = f"the record deleted successfully"
                   get_params = request.GET.urlencode()
                   return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{get_params}')
            if "save" in request.POST:
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
               get_params = request.GET.urlencode()
               base_url = reverse('update_spending_type', kwargs={'w_pk': w_pk, 'pk': selected_item.pk})
               new_url = f"{base_url}?{get_params}"
               return redirect(new_url)
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
    return render(request, 'finance/tmplt_add_spending_type.html', {
        'form': form,
        'w_pk': w_pk,
        'current_wlt': current_wlt,
        'message': message
    })

def update_spending_type(request, w_pk, pk):#___________________________________________update_spending_type
    try:
        spending_type = Spending_type.objects.get(pk=pk)
    except Income_type.DoesNotExist:
        raise Http404("Income type not found")

    form = Form_update_spending_type(request.POST or None, instance=spending_type)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            get_params = request.GET.urlencode()
            if get_params:
                return redirect(f'/finance/home_wlt/{w_pk}/add_spending_type/?{get_params}')
            else:
               return redirect(f'/finance/home_wlt/{w_pk}/add_spending_type/')
        return redirect(f'/finance/home_wlt/{w_pk}')

    # Отображаем форму
    return render(request, 'finance/tmplt_update_spending_type.html', {
        'form': form,
        'w_pk': w_pk,
        'spending_type': spending_type,
    })

