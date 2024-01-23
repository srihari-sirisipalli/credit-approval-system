import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.management import call_command
from credit_app.models import Customer, Loan

class Command(BaseCommand):
    help = 'Initialize data into the system'
    call_command('flush', '--noinput')
    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Clean existing data
                Customer.objects.all().delete()
                Loan.objects.all().delete()

                # Read customer data
                customer_data = pd.read_excel('customer_data.xlsx')
                customers = []

                # Populate Customer objects
                for _, row in customer_data.iterrows():
                    customer = Customer(
                        first_name=row['First Name'],
                        last_name=row['Last Name'],
                        age=row['Age'],
                        phone_number=row['Phone Number'],
                        monthly_salary=row['Monthly Salary'],
                        approved_limit=row['Approved Limit']
                    )
                    customers.append(customer)

                # Bulk create customers
                Customer.objects.bulk_create(customers)

                # Read loan data
                loan_data = pd.read_excel('loan_data.xlsx')
                loans = []

                # Populate Loan objects
                for _, row in loan_data.iterrows():
                    loan = Loan(
                        customer_id=row['Customer ID'],
                        loan_amount=row['Loan Amount'],
                        tenure=row['Tenure'],
                        interest_rate=row['Interest Rate'],
                        monthly_repayment=row['Monthly payment'],
                        emis_paid_on_time=row['EMIs paid on Time'],
                        start_date=row['Date of Approval'],
                        end_date=row['End Date']
                    )
                    loans.append(loan)

                # Bulk create loans
                Loan.objects.bulk_create(loans)

                self.stdout.write(self.style.SUCCESS('Data initialized successfully'))
        except Exception as e:
            # Log and display error if any exception occurs during data initialization
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
