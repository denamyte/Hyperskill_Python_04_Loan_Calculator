from math import ceil


def main_menu():
    principal = int(input('Enter the loan principal:\n'))
    choice = input('''What do you want to calculate?
type "m" - for number of monthly payments,
type "p" - for the monthly payment:
''')
    choice_dict[choice](principal)


def number_of_payments_branch(principal):  # m
    monthly_payment = int(input('Enter the monthly payment:\n'))
    number_of_payments = ceil(principal / monthly_payment)
    print(f'\nIt will take {number_of_payments} month{"s" if number_of_payments > 1 else ""} to repay the loan')


def monthly_payment_branch(principal):  # p
    number_of_payments = int(input('Enter the number of months:\n'))
    raw_payment = principal / number_of_payments
    monthly_payment = ceil(raw_payment)
    message = f'\nYour monthly payment = {monthly_payment}'
    if raw_payment != monthly_payment:
        last_month_payment = principal - (number_of_payments - 1) * monthly_payment
        message += f' and the last payment = {last_month_payment}.'
    print(message)


choice_dict = {'m': number_of_payments_branch,
               'p': monthly_payment_branch}
main_menu()
