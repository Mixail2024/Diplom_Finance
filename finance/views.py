from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Sum, ProtectedError
from django.db import transaction
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from .models import Wallet, Income, Income_type, Spending, Spending_type, Info, Rates
from .forms import (
    Form_create_wlt, Form_delete_wlt,
    Form_add_income, Form_update_income,
    Form_add_income_type, Form_update_income_type,
    Form_add_spending, Form_update_spending,
    Form_add_spending_type, Form_update_spending_type,
    Form_set_date_init_bal, TransferForm
    )
from django.utils.timezone import now
from datetime import timedelta, datetime
from decimal import Decimal
import json
from .my_exchange import get_currency_rates


main_currency = 'CZK'
current_date = datetime.now()
#=========================================================================================================_H O M E
def home(request):


    try:#__________________________________________________set init date
        choosen_date_obj = Info.objects.get()
    except Info.DoesNotExist:
        choosen_date_obj = None
    if request.method == 'POST':

        form = Form_set_date_init_bal(request.POST, instance=choosen_date_obj)
        if form.is_valid():
            form.save()
    else:
        form = Form_set_date_init_bal(instance=choosen_date_obj)#_____end
    prev_date = choosen_date_obj.init_date - timedelta(days=1)
    choosen_init = choosen_date_obj.init_date
    choosen_final = choosen_date_obj.final_date

    wlts = Wallet.objects.all()#_______________preparing tickers
    tickers = set()
    for wlt in wlts:
        tickers.add(wlt.w_ticker)
    tickers = sorted(tickers)

    n = 0#______________________________________preparing data for tables and data_chart for charts
    data = {}
    data_chart = []
    for ticker in tickers:
        data[ticker] = {}
        for wlt in wlts:
            if ticker == wlt.w_ticker:
                n += 1

                if choosen_date_obj.init_date < wlt.w_date:
                    bal_on_date = 0
                else:
                    before_obj_dt = Income.objects.filter(wallet=wlt, date__range=[wlt.w_date, prev_date])
                    before_dt_sum = before_obj_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
                    before_obj_ct = Spending.objects.filter(wallet=wlt, date__range=[wlt.w_date, prev_date])
                    before_ct_sum = before_obj_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
                    bal_on_date = wlt.w_balance + before_dt_sum - before_ct_sum

                after_obj_dt = Income.objects.filter(wallet=wlt, date__range=[choosen_init, choosen_final])
                after_dt_sum = after_obj_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
                after_obj_ct = Spending.objects.filter(wallet=wlt, date__range=[choosen_init, choosen_final])
                after_ct_sum = after_obj_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')

                if choosen_date_obj.init_date < wlt.w_date:
                    after_obj_dt = Income.objects.filter(wallet=wlt, date__range=[wlt.w_date, choosen_final])
                    after_dt_sum = after_obj_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
                    after_obj_ct = Spending.objects.filter(wallet=wlt, date__range=[wlt.w_date, choosen_final])
                    after_ct_sum = after_obj_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
                    final_bal = wlt.w_balance + after_dt_sum - after_ct_sum
                else:
                    final_bal = bal_on_date + after_dt_sum - after_ct_sum

                data_chart.append([wlt, float(final_bal)])
                data[ticker][wlt] = {
                    'n': n,
                    'wlt_pk': wlt.pk,
                    'bal_on_date': bal_on_date,
                    'after_dt_sum': after_dt_sum,
                    'after_ct_sum': after_ct_sum,
                    'final_bal': final_bal,
                }




    totals = {}#________________________________________________totals row for tables
    for ticker, wallets in data.items():
        totals[ticker] = {
            'total_initial': sum(wallet_data['bal_on_date'] for wallet_data in wallets.values()),
            'total_income': sum(wallet_data['after_dt_sum'] for wallet_data in wallets.values()),
            'total_spending': sum(wallet_data['after_ct_sum'] for wallet_data in wallets.values()),
            'total_final': sum(wallet_data['final_bal'] for wallet_data in wallets.values()),
        }

    info_date_obj = Info.objects.get()
    info_init = info_date_obj.init_date
    info_final = info_date_obj.final_date


    tickers_without_czk = tickers[:]#_______________rates for context
    tickers_without_czk.remove('CZK')
    rates = {}
    for ticker in tickers_without_czk:
        try:
            last_rate = Rates.objects.filter(name=ticker).latest('date')
            rates[ticker] = {'buy': str(last_rate.buy), 'sell': str(last_rate.sell), 'date':last_rate.date}
        except:
            rates[ticker] = {'buy': str(1), 'sell': str(1), 'date': current_date}



    choosen_ticker = request.GET.get("choosen_ticker")#_______________getting ticker from template


    if choosen_ticker == None:#_____________________________________Converting currencies
        choosen_ticker = main_currency

    if choosen_ticker == main_currency:
        for i in data_chart:
            ticker = i[0].w_ticker
            value = i[1]
            if ticker == main_currency:
               pass
            else:
                i[1] = round(value * float(rates[ticker]['buy']),2)
    else:
       for i in data_chart:
            ticker = i[0].w_ticker
            value = i[1]
            if ticker != main_currency:
                if ticker == choosen_ticker:
                    pass
                else:
                    i[1] = round((value * float(rates[ticker]['buy']))/float(rates[choosen_ticker]['sell']),2)
            else:
                i[1] = round(value/float(rates[choosen_ticker]['sell']),2)


    total_amount_lst = [i[1] for i in data_chart]
    total_amount = sum(total_amount_lst)



    pie_chart = []#_________________data for pie chart
    for i in data_chart:
        l=[]
        ticker = i[0].w_ticker
        l.append(i[0].f_name)
        value = i[1]
        if value >0:
            l.append(value)

        else:
            l.append(0)
        pie_chart.append(l)
    data_pie_chart = [['Wallet', 'Sum']]+ pie_chart


    wlts_lst = ['Category']#_________________data for bar chart
    lst = []
    for ticker in tickers:
        raw = []
        raw.append(ticker)
        for j in data_chart:
            if j[0].w_ticker == ticker:
                wlts_lst.append(j[0].f_name)
                wlts_lst.append({'role': 'annotation'})
                raw.append(float(j[1]))
                raw.append(str(j[0].f_name) +' '+str(float(j[1]))+' '+(str(choosen_ticker)).lower())
        lst.append(raw)
    qty_lst = []
    for i in lst:
        qty_lst.append(int((len(i)-1)/2))
    new_lst = []
    for i in lst:
        add_b = [0.00, '']
        add_a = [0.00, '']
        ind = lst.index(i)
        before = sum(qty_lst[:ind])
        if before == 0:
            before = []
            add_b = 0
        after = sum(qty_lst[(ind + 1):])
        if after == 0:
            after = []
            add_a = 0
        ticker = i.pop(0)
        i = (add_b * before) + i + (add_a * after)
        i = [ticker]+i
        new_lst.append(i)
    data_bar_chart = [wlts_lst] + new_lst




    context = {#_________________________________________________CONTEXT
        'data': data,
        'data_pie_chart': data_pie_chart,
        'data_bar_chart': data_bar_chart,
        'info_init': info_init,
        'info_final': info_final,
        'form': form,
        'rates': rates,
        'choosen_ticker': choosen_ticker,
        'tickers': tickers,
        'totals': totals,
        'total_amount': total_amount,
        'wlts': wlts,


        }
    return render(request, 'finance/home.html', context)



def home_wlt(request, w_pk):#____________________________________________HOME WLT
    current_wlt = Wallet.objects.get(pk=w_pk)

    info_date_obj = Info.objects.get()
    info_init = info_date_obj.init_date
    info_final = info_date_obj.final_date

    context = {
        'info_init': info_init,
        'info_final': info_final,
        'current_wlt': current_wlt
        }

    return render(request, 'finance/home_wlt.html', context)

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
            data_chart = get_data_chart(filtered_dt, filtered_ct)

            init_date = datetime.strptime(single_date, "%Y-%m-%d").date()
            prev_date = init_date - timedelta(days=1)
            if init_date < current_wlt.w_date:
                init_bal = 0
            else:
                before_obj_dt = Income.objects.filter(wallet=current_wlt, date__range=[current_wlt.w_date, prev_date])
                before_dt_sum = before_obj_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
                before_obj_ct = Spending.objects.filter(wallet=current_wlt, date__range=[current_wlt.w_date, prev_date])
                before_ct_sum = before_obj_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
                init_bal = current_wlt.w_balance + before_dt_sum - before_ct_sum


        elif choice == "period":#_____________________________________________________________________period
            start_date = request.GET.get("start_date")
            end_date = request.GET.get("end_date")
            context['start_date'] = start_date
            context['end_date'] = end_date
            filtered_dt = Income.objects.filter(wallet=current_wlt, date__range=[start_date, end_date])
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
            filtered_ct = Spending.objects.filter(wallet=current_wlt, date__range=[start_date, end_date])
            filtered_ct_sum = filtered_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
            data_chart = get_data_chart(filtered_dt, filtered_ct)

            init_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            prev_date = init_date - timedelta(days=1)
            if init_date < current_wlt.w_date:
                init_bal = 0
            else:
                before_obj_dt = Income.objects.filter(wallet=current_wlt, date__range=[current_wlt.w_date, prev_date])
                before_dt_sum = before_obj_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
                before_obj_ct = Spending.objects.filter(wallet=current_wlt, date__range=[current_wlt.w_date, prev_date])
                before_ct_sum = before_obj_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
                init_bal = current_wlt.w_balance + before_dt_sum - before_ct_sum


        elif choice == "month_year":#_____________________________________________________________________month_year
            month = request.GET.get("month")
            year = request.GET.get("year")
            context['month'] = month
            context['year'] = year
            filtered_dt = Income.objects.filter(wallet=current_wlt, date__year=year, date__month=month)
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
            filtered_ct = Spending.objects.filter(wallet=current_wlt, date__year=year, date__month=month)
            filtered_ct_sum = filtered_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
            data_chart = get_data_chart(filtered_dt, filtered_ct)

            init_date = datetime.strptime(f'{year}-{month}-01', "%Y-%m-%d").date()
            prev_date = init_date - timedelta(days=1)
            if init_date < current_wlt.w_date:
                init_bal = 0
            else:
                before_obj_dt = Income.objects.filter(wallet=current_wlt, date__range=[current_wlt.w_date, prev_date])
                before_dt_sum = before_obj_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
                before_obj_ct = Spending.objects.filter(wallet=current_wlt, date__range=[current_wlt.w_date, prev_date])
                before_ct_sum = before_obj_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
                init_bal = current_wlt.w_balance + before_dt_sum - before_ct_sum


        elif choice == "year_only":#_____________________________________________________________________year_only
            year_only = request.GET.get("year_only")
            context['year_only'] = year_only
            filtered_dt = Income.objects.filter(wallet=current_wlt, date__year=year_only)
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
            filtered_ct = Spending.objects.filter(wallet=current_wlt, date__year=year_only)
            filtered_ct_sum = filtered_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
            data_chart = get_data_chart(filtered_dt, filtered_ct)

            init_date = datetime.strptime(f'{year_only}-01-01', "%Y-%m-%d").date()
            prev_date = init_date - timedelta(days=1)
            if init_date < current_wlt.w_date:
                init_bal = 0
            else:
                before_obj_dt = Income.objects.filter(wallet=current_wlt, date__range=[current_wlt.w_date, prev_date])
                before_dt_sum = before_obj_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
                before_obj_ct = Spending.objects.filter(wallet=current_wlt, date__range=[current_wlt.w_date, prev_date])
                before_ct_sum = before_obj_ct.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
                init_bal = current_wlt.w_balance + before_dt_sum - before_ct_sum

    # ___________________________________________________________________________________________________ContexT
    final_balance = init_bal + filtered_dt_sum - filtered_ct_sum

    context['wlt_pk'] = pk
    context['current_wlt'] = current_wlt

    context['init_bal'] = init_bal

    context['filtered_dt'] = filtered_dt
    context['filtered_dt_count']= filtered_dt.count()
    context['filtered_dt_sum'] = filtered_dt_sum

    context['filtered_ct'] = filtered_ct
    context['filtered_ct_count'] = filtered_ct.count()
    context['filtered_ct_sum'] = filtered_ct_sum

    context['dtct_sum'] = filtered_dt_sum + filtered_ct_sum
    context['left'] = current_wlt.w_limit + final_balance

    context['final_balance'] = final_balance
    context['data_chart'] = data_chart


    return render(request, 'finance/home_wlt.html', context)


def get_data_chart(dt , ct):#______________________________________get_data_chart
    dt_types = []
    for i in dt:
        if not i.income_type in dt_types:
            dt_types.append(i.income_type)
    dt_types_qty = len(dt_types)
    dt_type_names = []
    for j in dt_types:
        dt_type_names.append(j.name)
        dt_type_names.append({"role": "annotation"})

    ct_types = []
    for i in ct:
        if not i.spending_type in ct_types:
            ct_types.append(i.spending_type)
    ct_types_qty = len(ct_types)
    ct_type_names = []
    for j in ct_types:
        ct_type_names.append(j.name)
        ct_type_names.append({"role": "annotation"})

    types_row = ['Category'] + dt_type_names + ct_type_names

    dt_row = ['Incomes']
    for typ in dt_types:
        try:
            group = dt.filter(income_type=typ)
            group_sum = group.aggregate(Sum('debit'))['debit__sum'] or 0.00
        except:
            group_sum = 0.00

        dt_row.append(float(group_sum))
        dt_row.append(str(typ) + ' ' + str(float(group_sum)))
    dt_row = dt_row + [0.00, '']*ct_types_qty

    ct_row = ['Spendings']
    ct_row = ct_row + [0.00, '']*dt_types_qty
    for typ in ct_types:
        try:
            group = ct.filter(spending_type=typ)
            group_sum = group.aggregate(Sum('credit'))['credit__sum'] or 0.00
        except:
            group_sum = 0.00

        ct_row.append(float(group_sum))
        ct_row.append(str(typ) + ' ' + str(float(group_sum)))

    data_chart = [types_row, dt_row, ct_row]
    data_chart = json.dumps(data_chart)
    # print(data_chart)
    return data_chart




def delete_filtered_dt(request, w_pk):#_________________________________________delete_filtered_dt
    params = request.GET.get('params')
    params = params.replace("*", "&")
    lst = request.GET.get('ids')
    lst = lst.split('/')
    lst = [i for i in lst if i.isdigit() and int(i) > 0]
    Income.objects.filter(pk__in=lst).delete()
    return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{params}')

def delete_filtered_ct(request, w_pk):#_________________________________________delete_filtered_ct
    params = request.GET.get('params')
    params= params.replace("*", "&")
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
                try:
                    selected_item.delete()
                    message = f"'{selected_item}' deleted successfully"
                except ProtectedError:
                    message = f"Cannot delete '{selected_item}' because it is referenced by other records!"


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
    get_params = request.GET.urlencode()
    if request.method == 'POST':
        form = Form_update_spending(request.POST, instance=record)
        if form.is_valid():
            if "delete" in request.POST:
               if record:
                   record.delete()
                   message = f"the record deleted successfully"

                   return redirect(f'/finance/home_wlt/{w_pk}/calendar/?{get_params}')
            if "save" in request.POST:
                form.save()
                # Получаем все параметры из request.GET и добавляем их к URL

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

def transfer_funds(request):
    today_date = now().date()  # Получаем текущую дату с учётом часового пояса
    form = TransferForm(request.POST or None, initial={"date": today_date})  # Инициализация формы с текущей датой

    if request.method == "POST":
        if form.is_valid():
            from_wallet = form.cleaned_data["from_wallet"]
            to_wallet = form.cleaned_data["to_wallet"]
            amount = form.cleaned_data["amount"]
            comment = form.cleaned_data["comment"]
            date = form.cleaned_data["date"]
            amount_to = form.cleaned_data["amount_to"]
            print('amount_to', amount_to)
            # Проверяем, чтобы кошельки не совпадали
            if from_wallet == to_wallet:
                form.add_error(None, "The source and destination wallets must be different.")
            else:
                try:
                    with transaction.atomic():  # Работа с транзакцией
                        # Получаем или создаём типы операций
                        transfer_type_spending, _ = Spending_type.objects.get_or_create(name="Transfer")
                        transfer_type_income, _ = Income_type.objects.get_or_create(name="Transfer")

                        # Создаем запись в Spending
                        Spending.objects.create(
                            date=date,
                            wallet=from_wallet,
                            credit=amount,
                            comment=comment,
                            spending_type=transfer_type_spending,
                            destination=to_wallet
                        )

                        # Создаем запись в Income
                        income_amount = amount_to if amount_to !=0 else amount
                        print(income_amount)
                        Income.objects.create(
                            date=date,
                            wallet=to_wallet,
                            debit=income_amount,
                            comment=comment,
                            income_type=transfer_type_income,
                            source=from_wallet
                        )

                    # Сообщение об успешной операции
                    messages.success(request, "Funds transferred successfully!")
                    return redirect(reverse_lazy("home"))

                except Exception as e:
                    # Сообщение об ошибке транзакции
                    form.add_error(None, f"Transaction failed: {str(e)}")
    return render(request, "finance/tmplt_transfer.html", {"form": form})

def update_rates(request):
    total_rates = Rates.objects.count()
    if total_rates > 100:
        old_records = Rates.objects.order_by('date')[:30]  # Получаем 30 самых старых
        old_records.delete()
    try:
        rates = get_currency_rates()
        with transaction.atomic():  # Используем транзакцию для атомарности
            for obj in rates:
                # Добавляем проверку, чтобы избежать дублирования записей
                if not Rates.objects.filter(date=obj.datetime, name=obj.name).exists():
                    Rates.objects.create(
                        date=obj.datetime,
                        name=obj.name,
                        buy=obj.buy,
                        sell=obj.sell,
                        source=obj.website
                    )
                else:
                    # Если запись уже существует, обновляем её
                    Rates.objects.filter(date=obj.datetime, name=obj.name).update(
                        buy=obj.buy, sell=obj.sell, source=obj.website
                    )

        # Сообщение об успешном обновлении
        messages.success(request, "Currency rates updated successfully.")

        return redirect('home')
    except Exception as e:
        # Обрабатываем ошибки
        messages.error(request, f"Error updating currency rates: {str(e)}")
        return redirect('home')