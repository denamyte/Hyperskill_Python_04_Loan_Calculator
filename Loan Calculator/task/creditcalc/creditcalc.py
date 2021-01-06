import argparse
import sys
from math import ceil, log, pow
from typing import Dict, Any

typ, pay, pri, per, inr = 'type', 'payment', 'principal', 'periods', 'interest'


def main():
    args = define_arguments()
    print(args)
    if errors_found(args):
        print('Incorrect parameters')
    else:
        # todo the main branch
        pass


def define_arguments() -> Dict[str, Any]:
    dash = '--'
    parser = argparse.ArgumentParser(description='This program calculates different parameters of a loan')
    parser.add_argument(dash + typ, choices=['annuity', 'diff'])
    parser.add_argument(dash + pay, type=float)
    parser.add_argument(dash + pri, type=int)
    parser.add_argument(dash + per, type=int)
    parser.add_argument(dash + inr, type=float)
    return vars(parser.parse_args())


def errors_found(args: Dict[str, Any]) -> bool:
    diff_payment_collision = args.get(typ) and args.get(typ) == 'diff' and args.get(pay)
    interest_not_found = args.get(inr) is None
    lack_of_params = 4 > len(list(filter(lambda x: x[1] is not None, args.items())))
    return diff_payment_collision or interest_not_found or lack_of_params


# todo: add Calculation of differentiated payments
#  replace old params with new ones

[p, a, n, i] = [r for r in range(4)]  # indices:  0, 1, 2, 3
enter = 'Enter the '
prompts = ['loan principal:\n',  # the indexed prompts
           'the monthly payment:\n',
           'the number of periods:\n',
           'loan interest:\n']
data = []  # the indexed data; will be filled up after prompts


def main_menu():
    choice = input('''What do you want to calculate?
type "n" for number of monthly payments,
type "a" for annuity monthly payment amount,
type "p" for loan principal:
''')
    # choice_dict[choice]()


def number_of_payments_branch():  # n
    ask_for_data_without(n)
    months = ceil(log(data[a] / (data[a] - data[i] * data[p]), 1 + data[i]))
    print(number_or_payments_msg(months))


def number_or_payments_msg(months):
    years, months_in_year = divmod(months, 12)
    msg = 'It will take'
    msg += f' {years} years' if years else ''
    msg += ' and' if years and months_in_year else ''
    msg += f' {months_in_year} months' if months_in_year else ''
    msg += ' to repay this loan!'
    return msg


def monthly_payment_branch():  # a
    ask_for_data_without(a)
    print(f'Your monthly payment = {ceil(data[p] * common_calc())}!')


def loan_principal_branch():  # p
    ask_for_data_without(p)
    print(f'Your loan principal = {round(data[a] / common_calc())}!')


def common_calc():
    pow_ = pow(1 + data[i], data[n])
    return data[i] * pow_ / (pow_ - 1)


def ask_for_data_without(skip: int):
    for ind in range(4):
        data.append(float(input(enter + prompts[ind])) if ind != skip else 0.0)
    data[i] /= 1200  # converting annually percents into a monthly floating number


# choice_dict = {'n': number_of_payments_branch,
#                'a': monthly_payment_branch,
#                'p': loan_principal_branch}
# main_menu()

main()
