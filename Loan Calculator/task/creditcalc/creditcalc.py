import argparse
from math import ceil, floor, log, pow
from typing import Dict, Any


def main():
    if errors_found():
        print('Incorrect parameters.')
    else:
        args[inr] /= 1200  # converting interest rate into monthly decimals
        if args[typ] == dif:
            diff_branch()
        else:
            annuity_branch()


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
    return not args.get(typ)\
        or not args.get(inr)\
        or args[typ] == dif and args.get(pay) is not None\
        or 4 > existent_args_number()


def existent_args_number():
    return len(list(filter(lambda x: x[1] and (type(x[1]) is str or x[1] > 0), args.items())))


def diff_branch():
    months = [m for m in range(1, args[per] + 1)]
    payments = list(map(calc_diff_payment, months))
    for m in months:
        print(f'Month {m}: payment is {payments[m - 1]}')
    print(f'\nOverpayment = {sum(payments) - args[prc]}')


def calc_diff_payment(m: int):
    p, n, i = args[prc], args[per], args[inr]
    return ceil(p / n + i * (p - p * (m - 1) / n))


def annuity_branch():
    if not args.get(pay):
        annuity_payment_branch()
    elif not args.get(prc):
        annuity_principal_branch()
    elif not args.get(per):
        annuity_periods_branch()


def annuity_payment_branch():
    args[pay] = ceil(args[prc] * formula_part())
    print(f'Your annuity payment = {args[pay]}!')
    show_annuity_overpayment()


def annuity_principal_branch():
    args[prc] = floor(args[pay] / formula_part())
    print(f'Your loan principal = {args[prc]}!')
    show_annuity_overpayment()


def annuity_periods_branch():
    args[per] = ceil(log(args[pay] / (args[pay] - args[inr] * args[prc]), 1 + args[inr]))
    print(number_or_payments_msg(args[per]))
    show_annuity_overpayment()


def number_or_payments_msg(months):
    years, months_in_year = divmod(months, 12)
    return 'It will take'\
        f' {years} years' if years else ''\
        ' and' if years and months_in_year else ''\
        f' {months_in_year} months' if months_in_year else ''\
        ' to repay this loan!'


def show_annuity_overpayment():
    overpayment = ceil(args[pay] * args[per] - args[prc])
    print(f'Overpayment = {overpayment}')


def formula_part():
    pow_ = pow(1 + args[inr], args[per])
    return args[inr] * pow_ / (pow_ - 1)


typ, pay, prc, per, inr = 'type', 'payment', 'principal', 'periods', 'interest'
ann, dif = 'annuity', 'diff'
args = define_arguments()
main()
