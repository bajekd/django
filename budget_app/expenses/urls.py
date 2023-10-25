from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name="index"),
    path('add-expense/', views.create_expense, name='create-expense'),
    path('edit-expense/<int:id>', views.update_expense, name='update-expense'),
    path('expense-delete/<int:id>', views.delete_expense, name='delete-expense'),
    path('search-expenses/', csrf_exempt(views.search_expenses), name='search-expenses'),
    path('expense_category_summary/', views.expense_category_summary, name='expense-category-summary'),
    path('stats/', views.stats_view, name='stats'),
    path('export_csv/', views.export_csv, name='export-csv'),
    path('export_excel/', views.export_excel, name='export-excel'),
    path('export_pdf/', views.export_pdf, name='export-pdf'),
]