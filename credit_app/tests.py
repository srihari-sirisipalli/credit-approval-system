from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Customer,Loan
from datetime import datetime,timedelta


class RegisterAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_missing_field(self):
        print("\nTest Case: Registering with a missing required field")
        url = '/register/'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            # Missing 'monthly_salary' and 'phone_number' fields
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_register_invalid_age(self):
        print("\nTest Case: Registering with an invalid age (negative age)")
        url = '/register/'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': -5,
            'monthly_salary': 5000,
            'phone_number': 1234567890,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_register_negative_salary(self):
        print("\nTest Case: Registering with a negative monthly salary")
        url = '/register/'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'monthly_salary': -5000,
            'phone_number': 1234567890,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_register_invalid_phone_number(self):
        print("\nTest Case: Registering with an invalid phone number (non-numeric)")
        url = '/register/'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'monthly_salary': 5000,
            'phone_number': 'invalid_number',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_register_data_type_mismatch(self):
        print("\nTest Case: Registering with data type mismatch (string instead of integer for age)")
        url = '/register/'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 'thirty',  # String instead of integer
            'monthly_salary': 5000,
            'phone_number': 1234567890,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")




class CheckLoanEligibilityTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_loan_eligible(self):
        print("\nTest Case: Eligible for Loan")
        url = '/check-eligibility/'
        customer = Customer.objects.create(first_name='John',
                                           last_name='Doe',
                                           age=30,
                                           phone_number=1234567890,
                                           monthly_salary=50000,
                                           approved_limit=10000)
        data = {
            "customer_id":customer.customer_id ,  
            "loan_amount": 10000,
            "interest_rate": 1,
            "tenure": 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test Case Passed!")
    

    def test_customer_not_found(self):
        print("\nTest Case: Customer not found")
        url = '/check-eligibility/'
        data = {
            "customer_id": -1,  # Invalid customer_id
            "loan_amount": 10000,
            "interest_rate": 10,
            "tenure": 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")
    

    def test_negative_loan_amount(self):
        print("\nTest Case: Negative loan amount")
        url = '/check-eligibility/'
        data = {
            "customer_id": 1,
            "loan_amount": -10000,
            "interest_rate": 10,
            "tenure": 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_negative_interest_rate(self):
        print("\nTest Case: Negative interest rate")
        url = '/check-eligibility/'
        data = {
            "customer_id": 1,
            "loan_amount": 10000,
            "interest_rate": -1,
            "tenure": 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_negative_tenure(self):
        print("\nTest Case: Negative tenure")
        url = '/check-eligibility/'
        data = {
            "customer_id": 1,
            "loan_amount": 10000,
            "interest_rate": 10,
            "tenure": -12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    

class CreateLoanTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_customer_not_found(self):
        print("\nTest Case: Customer not found")
        url = '/create-loan/'
        data = {
            'customer_id': 1000,  # Non-existent customer_id
            'loan_amount': 15000.0,
            'interest_rate': 10.0,
            'tenure': 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_zero_loan_amount(self):
        print("\nTest Case: Zero loan amount")
        url = '/create-loan/'
        data = {
            'customer_id': 128,
            'loan_amount': 0.0,  # Zero loan amount
            'interest_rate': 10.0,
            'tenure': 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_negative_loan_amount(self):
        print("\nTest Case: Negative loan amount")
        url = '/create-loan/'
        data = {
            'customer_id': 128,
            'loan_amount': -5000.0,  # Negative loan amount
            'interest_rate': 10.0,
            'tenure': 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_negative_interest_rate(self):
        print("\nTest Case: Negative interest rate")
        url = '/create-loan/'
        data = {
            'customer_id': 128,
            'loan_amount': 15000.0,
            'interest_rate': -1.0,  # Negative interest rate
            'tenure': 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")

    def test_negative_tenure(self):
        print("\nTest Case: Negative tenure")
        url = '/create-loan/'
        data = {
            'customer_id': 128,
            'loan_amount': 15000.0,
            'interest_rate': 10.0,
            'tenure': -12  # Negative tenure
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")
    
    def test_loan_created(self):
        customer = Customer.objects.create(first_name='John',
                                           last_name='Doe',
                                           age=30,
                                           phone_number=1234567890,
                                           monthly_salary=50000,
                                           approved_limit=10000)
        print("\nTest Case: Loan Created")
        url = '/create-loan/'
        data = {
            'customer_id': customer.customer_id,
            'loan_amount': 100.0,
            'interest_rate': 1.0,
            'tenure': 12  
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test Case Passed!")


class ViewLoanDetailsByLoanIDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_loan_is_not_present(self):
        print("\nTest Case: Loan is not present in the data")
        loan_id=1000
        url = f'/view-loan/loan-id/{loan_id}/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test Case Passed!")
    def test_loan_is_present(self):
        print("\nTest Case: Loan is present in the data")
        customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            phone_number=1234567890,
            monthly_salary=5000,
            approved_limit=10000
        )
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=5000,
            interest_rate=10,
            monthly_repayment=500,
            tenure=12,
            emis_paid_on_time=0,
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=365)
        )
        loan_id=loan.loan_id
        url = f'/view-loan/loan-id/{loan_id}/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test Case Passed!")

class ViewLoanDetailsByCustomerIDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_loan_details_customer_is_not_present(self):
        print("\nTest Case: Loan details,when customer is not present in the data")
        loan_id=100
        url = f'view-loans/customer-id/{loan_id}/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Test Case Passed!")