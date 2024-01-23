# credit_app/admin.py
from django.contrib import admin
from .models import Customer, Loan

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'first_name', 'last_name', 'age', 'phone_number', 'monthly_salary', 'approved_limit']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_filter = ['age', 'monthly_salary','approved_limit']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['loan_id', 'customer','customer_id', 'loan_amount', 'tenure', 'interest_rate', 'monthly_repayment', 'emis_paid_on_time', 'start_date', 'end_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'loan_id']
    list_filter = ['customer','emis_paid_on_time', 'start_date', 'end_date',]
