from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.db.models import Sum
from .models import Wallet, Income, Income_type, Spending, Spending_type
from .forms import Form_create_wlt, Form_delete_wlt, Form_add_income, Form_add_income_type, Form_add_spending
from decimal import Decimal
from django.utils.timezone import datetime

def home(request):
    wlts = Wallet.objects.order_by('w_name')
    return render(request, 'finance/home.html', {'wlts':wlts})

def home_wlt(request, pk):
    current_wlt = Wallet.objects.get(pk=pk)
    return render(request, 'finance/home_wlt.html', {'current_wlt':current_wlt})

class Create_wlt(CreateView):
    model = Wallet
    form_class = Form_create_wlt
    template_name = 'finance/tmplt_create_wlt.html'
    success_url = reverse_lazy('home')

class Update_wlt(UpdateView):
    model = Wallet
    form_class = Form_create_wlt
    template_name = 'finance/tmplt_update_wlt.html'
    def get_success_url(self):
        pk = self.kwargs['pk']  # Получаем pk текущей записи из URL
        return reverse_lazy('home_wlt', kwargs={'pk': pk})

class Delete_wlt(DeleteView):
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
        context['pk'] = self.kwargs.get('pk')  # Извлекаем параметр pk
        return context

from decimal import Decimal
from django.db.models import Sum

def calendar_view(request, pk):
    current_wlt = Wallet.objects.get(pk=pk)
    initial_balance = current_wlt.initial_balance
    filtered = None
    filtered_sum = Decimal('0.00')  # Инициализируем как строку для точности
    period = ""

    context = {}

    if request.method == 'POST':
        choice = request.POST.get("choice")
        if choice == "date":
            single_date = request.POST.get("single_date")
            context['single_date'] = single_date
            filtered_dt = Income.objects.filter(wallet=current_wlt, date=single_date)
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')


        elif choice == "period":
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            context['start_date'] = start_date
            context['end_date'] = end_date
            filtered_dt = Income.objects.filter(wallet=current_wlt, date__range=[start_date, end_date])
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')


        elif choice == "month_year":
            month = request.POST.get("month")
            year = request.POST.get("year")
            context['month'] = month
            context['year'] = year
            filtered_dt = Income.objects.filter(wallet=current_wlt, date__year=year, date__month=month)
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')


        elif choice == "year_only":
            year_only = request.POST.get("year_only")
            context['year_only'] = year_only
            filtered_dt = Income.objects.filter(wallet=current_wlt, date__year=year_only)
            filtered_dt_sum = filtered_dt.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')

    context['pk'] = pk
    context['current_wlt'] = current_wlt
    context['initial_balance'] = initial_balance
    context['filtered_dt'] = filtered_dt
    context['filtered_dt_sum'] = Decimal(filtered_dt_sum)
    context['final_balance'] = initial_balance + Decimal(filtered_dt_sum)

    print('request', request.POST)
    print('context', context)
    return render(request, 'finance/home_wlt.html', context)


def add_income(request, pk):
    message = ''
    wallet = get_object_or_404(Wallet, pk=pk)
    current_wlt = Wallet.objects.get(pk=pk)
    form_income = Form_add_income(request.POST or None, prefix="form_income")
    if form_income.is_valid():
        income = form_income.save(commit=False)
        income.wallet = wallet  # Привязываем доход к конкретному кошельку
        income.save()
        return redirect('home_wlt', pk=wallet.pk)
    return render(request, 'finance/tmplt_new_income.html', {'form_income': form_income, 'pk': pk, 'current_wlt':current_wlt, 'message':message})


def add_income_type(request, pk):
    wallet = get_object_or_404(Wallet, pk=pk)
    current_wlt = Wallet.objects.get(pk=pk)
    message = ''
    form = Form_add_income_type(request.POST or None, prefix="form")
    if form.is_valid():
        if "delete" in request.POST:
            selected_item = form.cleaned_data.get("choices")
            if selected_item:
                selected_item.delete()
                message = "Запись успешно удалена."
        elif "add" in request.POST:
            new_value = form.cleaned_data.get("new_value")
            if new_value:
                if not Income_type.objects.filter(name=new_value).exists():
                    Income_type.objects.create(name=new_value)
                    message = "Запись успешно добавлена."
                    form = Form_add_income_type(prefix="form")  # Очищаем форму
                else:
                    message = "Такое значение уже существует."
        elif "add_exit" in request.POST:
            new_value = form.cleaned_data.get("new_value")
            if new_value:
                if not Income_type.objects.filter(name=new_value).exists():
                    Income_type.objects.create(name=new_value)
                    message = "Запись успешно добавлена."
                else:
                    message = "Такое значение уже существует."
            return redirect('add_income', pk=wallet.pk)
    return render(request, 'finance/tmplt_new_income_type.html', {'form': form, 'pk': pk, 'current_wlt':current_wlt, 'message':message})



class Delete_income_type(FormView):
    pass


class Add_spending(CreateView):
    pass










