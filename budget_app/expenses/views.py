import json
import csv, xlwt
from weasyprint import HTML
import tempfile
import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Sum
from django.template.loader import render_to_string

from .models import Category, Expense
from userpreferences.models import UserPreference


# Create your views here.


@login_required(login_url="/authentication/login/")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {"expenses": expenses, "page_obj": page_obj, "currency": currency}

    return render(request, "expenses/index.html", context)


@login_required(login_url="/authentication/login/")
def create_expense(request):
    categories = Category.objects.all()
    date = timezone.now()
    context = {"categories": categories, "values": request.POST, "date": date}

    if request.method == "GET":
        return render(request, "expenses/create_expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]

        if not amount:
            messages.error(request, "Amount is required, please fill appropriate form")
            return render(request, "expenses/create_expense.html", context)

        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]

        Expense.objects.create(
            amount=amount,
            date=date,
            description=description,
            owner=request.user,
            category=category,
        )
        messages.success(request, "Expense saved successfully")

        return redirect("expenses:index")

    return render(request, "expenses/create_expense.html")


@login_required(login_url="/authentication/login/")
def update_expense(request, id):
    expense = Expense.objects.get(id=id)
    categories = Category.objects.all()
    context = {"expense": expense, "categories": categories, "values": expense}

    if request.method == "GET":
        return render(request, "expenses/update_expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]

        if not amount:
            messages.error(request, "Amount is required, please fill appropriate form")
            return render(request, "expenses/update_expense.html", context)

        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]

        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.category = category

        expense.save()
        messages.success(request, "Expense updated  successfully")

        return redirect("expenses:index")


@login_required(login_url="/authentication/login/")
def delete_expense(request, id):
    expense = Expense.objects.get(id=id)

    expense.delete()
    messages.success(request, "Expense removed")

    return redirect("expenses:index")


def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        expenses = (
            Expense.objects.filter(amount__istartswith=search_str, owner=request.user)
            | Expense.objects.filter(date__istartswith=search_str, owner=request.user)
            | Expense.objects.filter(
                description__icontains=search_str, owner=request.user
            )
            | Expense.objects.filter(category__icontains=search_str, owner=request.user)
        )
        data = expenses.values()

        return JsonResponse(list(data), safe=False)


def expense_category_summary(request):
    today_date = datetime.date.today()
    six_months_ago = today_date - datetime.timedelta(days=30 * 6)
    categories_list = [category.name for category in Category.objects.all()]
    finalrep = {}
    
    for category in categories_list:
        finalrep[category] = Expense.objects.filter(
            owner=request.user, date__gte=six_months_ago,
            date__lte=today_date, category=category,
        ).aggregate(Sum("amount"))["amount__sum"]  # .aggregate(Sum('column_name') returns {'column_name__sum': sum})
    
    return JsonResponse({'expenses_categories_data': finalrep})


@login_required(login_url="/authentication/login/")
def stats_view(request):
    return render(request, 'expenses/stats.html')


@login_required(login_url="/authentication/login/")
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename=Expenses_{str(datetime.date.today())}_csv"

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response


@login_required(login_url="/authentication/login/")
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f"attachment; filename=Expenses_{str(datetime.date.today())}_xls"
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
        

    wb.save(response)

    return response


@login_required(login_url="/authentication/login/")
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"attachment; filename=Expenses_{str(datetime.date.today())}_pdf"
    response['COntent-Transfer-Encoding'] = "binary"

    expenses = Expense.objects.filter(owner=request.user)
    sum = expenses.aggregate(Sum('amount'))["amount__sum"] # .aggregate(Sum('column_name') returns {'column_name__sum': sum})

    html_string = render_to_string('expenses/pdf_output.html', {'expenses': expenses, 'total': sum})
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    
    return response


    





    

