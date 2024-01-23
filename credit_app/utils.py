# credit_app/utils.py
from datetime import datetime
from django.db import models
from django.db.models import F
from .models import Loan, Customer

def calculate_credit_score(customer):
    """
    Calculate the credit score for a customer based on various rules.

    Rules:
    i. Deduct points for EMIs not paid on time
    ii. Deduct points for the number of loans taken in the past
    iii. Deduct points for loan activity in the current year
    iv. Deduct points if the sum of current loans > approved limit

    Args:
    - customer: Customer object

    Returns:
    - int: Calculated credit score
    """
    credit_score = 100  # Start with a base score of 100

    # Rule i: Deduct points for EMIs not paid on time
    emis_not_paid_on_time = Loan.objects.filter(customer=customer, emis_paid_on_time__lt=F('tenure')).count()
    credit_score -= emis_not_paid_on_time * 2  # Deduct 2 points for each EMI not paid on time

    # Rule ii: Deduct points for the number of loans taken in the past
    total_loans_taken = Loan.objects.filter(customer=customer).count()
    credit_score -= total_loans_taken * 3  # Deduct 3 points for each loan taken in the past

    # Rule iii: Deduct points for loan activity in the current year
    current_year = datetime.now().year
    loans_in_current_year = Loan.objects.filter(customer=customer, start_date__year=current_year).count()
    credit_score -= loans_in_current_year * 5  # Deduct 5 points for loan activity in the current year

    # Rule iv: Deduct points if the sum of current loans > approved limit
    total_current_loan_amount = Loan.objects.filter(customer=customer).aggregate(models.Sum('loan_amount'))['loan_amount__sum'] or 0
    if total_current_loan_amount > customer.approved_limit:
        credit_score = 0

    return max(credit_score, 0)  # Ensure credit score is not negative


def calculate_corrected_interest_rate(credit_score, interest_rate):
    """
    Calculate the corrected interest rate based on the customer's credit score.

    Args:
    - credit_score: int, Customer's credit score
    - interest_rate: float, Initial interest rate

    Returns:
    - float or None: Corrected interest rate or None if not applicable
    """
    if credit_score > 50:
        return interest_rate
    elif 50 >= credit_score > 30:
        return max(interest_rate, 12)
    elif 30 >= credit_score > 10:
        return max(interest_rate, 16)
    else:
        return None


def calculate_monthly_installment(loan_amount, tenure, interest_rate):
    """
    Calculate the monthly installment for a loan.

    Args:
    - loan_amount: float, Loan amount
    - tenure: int, Loan tenure in months
    - interest_rate: float, Interest rate per annum

    Returns:
    - float: Calculated monthly installment rounded to 2 decimal places
    """
    interest_rate /= 100  # Convert percentage to decimal
    monthly_interest_rate = interest_rate / 12
    numerator = loan_amount * monthly_interest_rate
    denominator = 1 - (1 + monthly_interest_rate) ** -tenure

    monthly_installment = numerator / denominator

    return round(monthly_installment, 2)  # Round to 2 decimal places


def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    """
    Check the eligibility of a loan based on the customer's credit score and provided loan details.

    Args:
    - customer: Customer object
    - loan_amount: float, Requested loan amount
    - interest_rate: float, Requested interest rate
    - tenure: int, Requested loan tenure in months

    Returns:
    - dict: Loan approval details including interest rate, corrected interest rate, tenure, and monthly installment
    """
    credit_score = calculate_credit_score(customer)
    corrected_interest_rate = calculate_corrected_interest_rate(credit_score, interest_rate)
    monthly_installment = calculate_monthly_installment(loan_amount, tenure, corrected_interest_rate)

    total_current_emis = Loan.objects.filter(customer=customer).aggregate(models.Sum('monthly_repayment'))['monthly_repayment__sum'] or 0
    monthly_salary = customer.monthly_salary

    # Check loan eligibility based on the provided conditions
    approval = credit_score > 0 and (
        (credit_score > 50) or
        (50 >= credit_score > 30 and corrected_interest_rate > 12) or
        (30 >= credit_score > 10 and corrected_interest_rate > 16)
    )

    approval = approval and (total_current_emis + monthly_installment <= 0.5 * monthly_salary)
    
    if approval:
        return {
            'approval': approval,
            'interest_rate': interest_rate,
            'corrected_interest_rate': corrected_interest_rate,
            'tenure': tenure,
            'monthly_installment': monthly_installment
        }
    else:
        return {
            'approval': approval,
            'interest_rate': None,
            'corrected_interest_rate': None,
            'tenure': None,
            'monthly_installment': None
        }
