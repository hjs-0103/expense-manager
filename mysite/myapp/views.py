from django.shortcuts import render,redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime

# Create your views here.
def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    all_expenses = Expense.objects.all()

    total_expenses = all_expenses.aggregate(Sum("amount"))['amount__sum']


    past_year= datetime.date.today() - datetime.timedelta(days=365)
    data_py = Expense.objects.filter(date__gt=past_year)
    past_year_filtered = data_py.aggregate(Sum('amount'))["amount__sum"]

    past_month= datetime.date.today() - datetime.timedelta(days=30)
    data_pm = Expense.objects.filter(date__gt=past_month)
    past_month_filtered = data_pm.aggregate(Sum('amount'))["amount__sum"]
  
    past_week= datetime.date.today() - datetime.timedelta(days=7)
    data_pw = Expense.objects.filter(date__gt=past_week)
    past_week_filtered = data_pw.aggregate(Sum('amount'))["amount__sum"]

    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))


    sums_per_category = Expense.objects.filter().values('category').annotate(sum=Sum('amount'))


    expenseform = ExpenseForm();
    return render(request,'myapp/dark-modern-index.html', {'expense_form': expenseform,'all_expenses' : all_expenses,'sum': total_expenses,'yearly':past_year_filtered,'monthly':past_month_filtered,'weekly':past_week_filtered,'daily':daily_sums,'categorysums':sums_per_category})


def edit(request,id):
    item = Expense.objects.get(id=id)
    expense_form = ExpenseForm(request.POST or None,instance=item)

    if expense_form.is_valid():
        expense_form.save()
        return redirect('index')
    

    return render(request,'myapp/modern-edit.html', {"expense_form" : expense_form})

def delete(request,id):
    item = Expense.objects.get(id=id)
    expense_form = ExpenseForm(request.POST or None,instance=item)
    if request.method == "POST":
        item.delete()
        return redirect('index')
    
    return render(request,'myapp/delete_item.html', {"expense_form" : expense_form})