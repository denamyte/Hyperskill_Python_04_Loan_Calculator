import argparse
import sys
from math import ceil, log, pow
from typing import Dict, Any



def main():
    if debug:
        print(args)
    if errors_found():
        print('Incorrect parameters')
    else:
        args[inr] /= 1200  # converting interest rate into monthly decimals
        type_actions[args[typ]]()


def define_arguments() -> Dict[str, Any]:
    dash = '--'
    parser = argparse.ArgumentParser(description='This program calculates different parameters of a loan')
    parser.add_argument(dash + typ, choices=[ann, dif])
    parser.add_argument(dash + pay, type=float)
    parser.add_argument(dash + prc, type=int)
    parser.add_argument(dash + per, type=int)
    parser.add_argument(dash + inr, type=float)
    return vars(parser.parse_args())


def errors_found() -> bool:
    if debug:
        print(list(filter(lambda x: x[1] and (type(x[1]) is str or x[1] > 0), args.items())))
    return not args.get(typ) \
        or not args.get(inr) \
        or args.get(typ) == dif and args.get(pay) is not None \
        or 4 > len(list(filter(lambda x: x[1] and (type(x[1]) is str or x[1] > 0), args.items())))


def diff_branch():
    months = [m for m in range(1, args[per] + 1)]
    payments = list(map(calc_diff_payment, months))
    if debug:
        print(payments)
    for m in months:
        print(f'Month {m}: payment is {payments[m - 1]}')
    print(f'\nOverpayment = {sum(payments) - args.get(prc)}')


def calc_diff_payment(m: int):
    pp = args.get(prc)
    nn = args.get(per)
    ii = args.get(inr)
    return ceil(pp / nn + ii * (pp - pp * (m - 1) / nn))


def annuity_branch():
    if args.get(pay) is None:
        annuity_payment_branch()


def annuity_payment_branch():
    ann_pay = ceil(args.get(prc) * common_calc_2())
    overpayment = ceil(ann_pay * args.get(per) - args.get(prc))
    print(f'Your annuity payment = {ann_pay}!')
    print(f'Overpayment = {overpayment}')


# todo
#  Example 4: calculate differentiated payments given a principal of 500,000 over 8 months at an interest rate of 7.8%

def common_calc_2():
    pow_ = pow(1 + args.get(inr), args.get(per))
    return args.get(inr) * pow_ / (pow_ - 1)


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
typ, pay, prc, per, inr = 'type', 'payment', 'principal', 'periods', 'interest'
ann, dif = 'annuity', 'diff'
debug = True
type_actions = {ann: annuity_branch,
                dif: diff_branch}
args = define_arguments()
main()
