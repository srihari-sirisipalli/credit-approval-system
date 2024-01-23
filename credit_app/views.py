from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,Loan
from .serializers import CustomerSerializer,LoanSerializer
from .utils import check_loan_eligibility, calculate_monthly_installment
from datetime import datetime,timedelta

class RegisterCustomerView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate incoming data using CustomerSerializer
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            # Extract validated data and create a new Customer instance
            data = serializer.validated_data
            customer = Customer.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                age=data['age'],
                monthly_salary=data['monthly_salary'],
                phone_number=data['phone_number']
            )

            # Prepare and send the response data
            response_data = {
                'customer_id': customer.customer_id,
                'name': f"{customer.first_name} {customer.last_name}",
                'age': customer.age,
                'monthly_salary': customer.monthly_salary,
                'approved_limit': customer.approved_limit,
                'phone_number': customer.phone_number
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # Return validation errors if the incoming data is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckLoanEligibilityView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract data from the request
            customer_id = request.data.get('customer_id')
            loan_amount = request.data.get('loan_amount')
            interest_rate = request.data.get('interest_rate')
            tenure = request.data.get('tenure')

            # Check if values are greater than zero
            if not all(value > 0 for value in [loan_amount, interest_rate, tenure]):
                return Response({'error': 'Loan amount, interest rate, and tenure must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve customer based on customer_id
            customer = Customer.objects.get(customer_id=customer_id)

            # Check loan eligibility using utility function
            eligibility_result = check_loan_eligibility(customer, loan_amount, interest_rate, tenure)

            # Adjust interest_rate if needed
            if interest_rate != eligibility_result['corrected_interest_rate']:
                eligibility_result['interest_rate'] = eligibility_result['corrected_interest_rate']

            return Response(eligibility_result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreateLoanView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract data from the request
            customer_id = request.data.get('customer_id')
            loan_amount = request.data.get('loan_amount')
            interest_rate = request.data.get('interest_rate')
            tenure = request.data.get('tenure')

            # Check if values are greater than zero
            if not all(value > 0 for value in [loan_amount, interest_rate, tenure]):
                return Response({'error': 'Loan amount, interest rate, and tenure must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve customer based on customer_id
            customer = Customer.objects.get(customer_id=customer_id)

            # Check loan eligibility using utility function
            eligibility_result = check_loan_eligibility(customer, loan_amount, interest_rate, tenure)

            # Process loan creation based on eligibility
            if eligibility_result['approval']:
                # Calculate start_date (current date)
                start_date = datetime.now().date()

                # Calculate end_date based on tenure
                end_date = start_date + timedelta(days=30 * tenure)

                # Calculate monthly_repayment
                monthly_repayment = calculate_monthly_installment(loan_amount, tenure, interest_rate)

                # Create a new Loan instance
                new_loan = Loan.objects.create(
                    customer=customer,
                    loan_amount=loan_amount,
                    interest_rate=interest_rate,
                    tenure=tenure,
                    start_date=start_date,
                    emis_paid_on_time=0,
                    end_date=end_date,
                    monthly_repayment=monthly_repayment
                )

                # Prepare and send the response data
                response_data = {
                    'loan_id': new_loan.loan_id,
                    'customer_id': customer_id,
                    'loan_approved': True,
                    'message': 'Loan approved',
                    'monthly_installment': monthly_repayment
                }
            else:
                # Prepare and send the response data for non-approved loans
                response_data = {
                    'loan_id': None,
                    'customer_id': customer_id,
                    'loan_approved': False,
                    'message': 'Loan not approved',
                    'monthly_installment': None
                }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ViewLoanDetails(APIView):
    def get(self, request, loan_id):
        try:
            # Retrieve loan based on loan_id
            loan = Loan.objects.get(loan_id=loan_id)

            # Serialize loan and customer data
            loan_serializer = LoanSerializer(loan)
            customer_serializer = CustomerSerializer(loan.customer)
            customer_data = {
                'customer_id': customer_serializer.data['customer_id'],
                'first_name': customer_serializer.data['first_name'],
                'last_name': customer_serializer.data['last_name'],
                'phone_number': customer_serializer.data['phone_number'],
                'age': customer_serializer.data['age'],
            }

            # Prepare and send the response data
            response_data = {
                'loan_id': loan_serializer.data['loan_id'],
                'customer': customer_data,
                'loan_amount': loan_serializer.data['loan_amount'],
                'interest_rate': loan_serializer.data['interest_rate'],
                'monthly_repayment': loan_serializer.data['monthly_repayment'],
                'tenure': loan_serializer.data['tenure']
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ViewLoansByCustomer(APIView):
    def get(self, request, customer_id, *args, **kwargs):
        try:
            # Retrieve all loans for the given customer_id
            loans = Loan.objects.filter(customer__customer_id=customer_id)

            # Serialize loan data
            loan_serializer = LoanSerializer(loans, many=True)

            # Create a response with the serialized data
            response_data = []
            for loan_data in loan_serializer.data:
                # Calculate repayments_left based on tenure and emis_paid_on_time
                repayments_left = loan_data['tenure'] - loan_data['emis_paid_on_time']

                # Add additional information to the response
                loan_response = {
                    'loan_id': loan_data['loan_id'],
                    'loan_amount': loan_data['loan_amount'],
                    'interest_rate': loan_data['interest_rate'],
                    'monthly_installment': loan_data['monthly_repayment'],
                    'repayments_left': repayments_left,
                }

                response_data.append(loan_response)

            # Return a custom error if there are no loans for the customer
            if len(response_data) == 0:
                return Response({'Error': 'Customer is not present'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
