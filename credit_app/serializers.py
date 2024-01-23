# credit_app/serializers.py
from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.

    Serializes Customer objects for API interactions.
    """
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'age', 'phone_number', 'monthly_salary', 'approved_limit']


class LoanSerializer(serializers.ModelSerializer):
    """
    Serializer for the Loan model.

    Serializes Loan objects for API interactions.
    """
    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'tenure', 'interest_rate', 'monthly_repayment', 'emis_paid_on_time', 'start_date', 'end_date']
