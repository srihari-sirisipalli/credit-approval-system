from django.urls import path
from .views import RegisterCustomerView, CheckLoanEligibilityView, CreateLoanView, ViewLoanDetails, ViewLoansByCustomer

urlpatterns = [
    # Endpoint for registering a new customer
    path('register/', RegisterCustomerView.as_view(), name='register-customer'),

    # Endpoint for checking loan eligibility
    path('check-eligibility/', CheckLoanEligibilityView.as_view(), name='check-eligibility'),

    # Endpoint for creating a new loan
    path('create-loan/', CreateLoanView.as_view(), name='create-loan'),

    # Endpoint for viewing details of a specific loan
    path('view-loan/loan-id/<int:loan_id>/', ViewLoanDetails.as_view(), name='view-loan-details'),

    # Endpoint for viewing all loans associated with a specific customer
    path('view-loans/customer-id/<int:customer_id>/', ViewLoansByCustomer.as_view(), name='view-loans-by-customer'),
]