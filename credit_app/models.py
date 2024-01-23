from django.db import models
from django.core.validators import MinValueValidator

class Customer(models.Model):
    # Customer model representing information about a customer
    customer_id = models.AutoField(primary_key=True)  # Auto-incremented primary key for the customer
    first_name = models.CharField(max_length=255)  # First name of the customer
    last_name = models.CharField(max_length=255)  # Last name of the customer
    age = models.PositiveIntegerField()  # Age of the customer
    phone_number = models.BigIntegerField()  # Phone number of the customer
    monthly_salary = models.IntegerField(validators=[MinValueValidator(0)])  # Monthly salary of the customer, disallowing negative values
    approved_limit = models.IntegerField(null=True, blank=True)  # Approved credit limit for the customer

    def save(self, *args, **kwargs):
        # Override the save method to set the default value for approved_limit based on the condition
        if self.approved_limit is None:
            self.approved_limit = round(36 * self.monthly_salary, -5)  # Round to nearest lakh

        super().save(*args, **kwargs)

    def __str__(self):
        # String representation of the Customer object, used for display purposes
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model):
    # Loan model representing information about a loan
    loan_id = models.AutoField(primary_key=True)  # Auto-incremented primary key for the loan
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey linking loan to a customer
    loan_amount = models.FloatField(validators=[MinValueValidator(0)])  # Amount of the loan, disallowing negative values
    tenure = models.IntegerField(validators=[MinValueValidator(0)])  # Tenure or duration of the loan
    interest_rate = models.FloatField(validators=[MinValueValidator(0)])  # Interest rate for the loan
    monthly_repayment = models.FloatField(validators=[MinValueValidator(0)])  # Monthly repayment amount for the loan
    emis_paid_on_time = models.IntegerField(validators=[MinValueValidator(0)])  # Number of EMIs paid on time
    start_date = models.DateField()  # Start date of the loan
    end_date = models.DateField()  # End date of the loan

    def __str__(self):
        # String representation of the Loan object, used for display purposes
        return f"Loan ID: {self.loan_id} - Customer: {self.customer.first_name} {self.customer.last_name}"
