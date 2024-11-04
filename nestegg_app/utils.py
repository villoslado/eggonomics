"""
Import modules and define functions to load data and get user input
"""

import os
import sys
import random
import matplotlib.pyplot as plt


def read_to_list(file_name):
    # Open a file of data in percent, convert to decimal and return a list
    with open(file_name) as in_file:
        lines = [float(line.strip()) for line in in_file]
        decimal = [round(line / 100, 5) for line in lines]
        return decimal


def default_input(prompt, default=None):
    # Allow use of default values in input
    prompt = "{} [{}]: ".format(prompt, default)
    response = input(prompt)
    if not response and default:
        return default
    else:
        return response


"""
Load data files with original data in percent form
"""
print("\nNote: Input data should be in percent format (e.g. 5.0 for 5%)")

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bonds = read_to_list(
        os.path.join(base_dir, "data", "10yr_TBond_returns_1926-2013_pct.txt"),
    )
    stocks = read_to_list(
        os.path.join(base_dir, "data", "SP500_returns_1926-2013_pct.txt"),
    )
    blend_40_50_10 = read_to_list(
        os.path.join(base_dir, "data", "40-50-10_returns_1926-2013_pct.txt"),
    )
    blend_50_50 = read_to_list(
        os.path.join(base_dir, "data", "50-50_returns_1926-2013_pct.txt"),
    )
    infl_rate = read_to_list(
        os.path.join(base_dir, "data", "inflation_rate_1926-2013_pct.txt"),
    )
except IOError as e:
    print("Error reading file: {}".format(e))
    sys.exit(1)

"""
Get user input; use dictionary for investment-type arguments
Print input legend for user
"""
investment_type_args = {
    "bonds": bonds,
    "stocks": stocks,
    "sb_blend": blend_50_50,
    "sbc_blend": blend_40_50_10,
}
print("   stocks = S&P 500")
print("   bonds = 10-year Treasury Bonds")
print("   sb_blend = 50% stocks, 50% bonds")
print("   sbc_blend = 40% stocks, 50% bonds, 10% cash\n")
print("Press ENTER to take the default value in brackets\n")

"""
Get user input for investment type
"""
invest_type = default_input(
    "Enter investment type: (stocks, bonds, sb_blend, sbc_blend: \n", "bonds"
).lower()
while invest_type not in investment_type_args:
    invest_type = input("Invalid input. Enter investment type: ").lower()

"""
Get user input for starting value of investment
"""
start_value = default_input(
    "Enter starting value of investment: \n",
    "10000",
)
while not start_value.isdigit():
    start_value = input("Invalid input. Enter starting value of investment: ")

"""
Get user input for annual pre-tax withdrawal
"""
withdrawal = default_input(
    "Enter annual pre-tax withdrawal (today's $): \n",
    "10000",
)
while not withdrawal.isdigit():
    withdrawal = input("Invalid input. Enter annual pre-tax withdrawal: ")

"""
Get user input for min number of years in retirement
"""
min_years = default_input(
    "Enter minimum years in retirement: \n",
    "10",
)
while not min_years.isdigit():
    min_years = input("Invalid input. Enter minimum years in retirement: ")

"""
Get user input for most likely number of years in retirement
"""
most_likely_years = default_input(
    "Enter most likely years in retirement: \n",
    "25",
)
while not most_likely_years.isdigit():
    most_likely_years = input(
        "Invalid input. Enter most likely years in retirement: ",
    )

"""
Get user input for max number of years in retirement
"""
max_years = default_input(
    "Enter maximum years in retirement: \n",
    "40",
)
while not max_years.isdigit():
    max_years = input("Invalid input. Enter maximum years in retirement: ")

"""
Get user input for number of cases to run
"""
num_cases = default_input(
    "Enter number of cases to run: \n",
    "50000",
)
while not num_cases.isdigit():
    num_cases = input("Invalid input. Enter number of cases to run: ")
