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


print("\nNote: Input data should be in percent format (e.g. 5.0 for 5%)")

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bonds = read_to_list(os.path.join(base_dir, "data", "10-yr_TBond_returns_1926-2013_pct.txt"),)
    stocks = read_to_list(os.path.join(base_dir, "data", "SP500_returns_1926-2013_pct.txt"),)
    blend_40_50_10 = read_to_list(os.path.join(base_dir, "data", "40-50-10_returns_1926-2013_pct.txt"),)
    blend_50_50 = read_to_list(os.path.join(base_dir, "data", "50-50_returns_1926-2013_pct.txt"),)
    infl_rate = read_to_list(os.path.join(base_dir, "data", "inflation_rate_1926-2013_pct.txt"),)
except IOError as e:
    print("Error reading file: {}".format(e))
    sys.exit(1)
