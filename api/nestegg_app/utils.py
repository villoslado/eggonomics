"""
Import modules and define functions to load data and get user input
"""

import os
import sys
import random
import matplotlib.pyplot as plt


def read_to_list(file_name):
    with open(file_name) as in_file:
        lines = [float(line.strip()) for line in in_file]
        decimal = [round(line / 100, 5) for line in lines]
        return decimal


def default_input(prompt, default=None):
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
        os.path.join(base_dir, "data", "S-B-C_blend_1926-2013_pct.txt"),
    )
    blend_50_50 = read_to_list(
        os.path.join(base_dir, "data", "S-B_blend_1926-2013_pct.txt"),
    )
    infl_rate = read_to_list(
        os.path.join(base_dir, "data", "annual_infl_rate_1926-2013_pct.txt"),
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
    "Enter investment type: (stocks, bonds, sb_blend, sbc_blend: \n",
    "sbc_blend",
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

"""
Check for erroneous input
"""
if (
    not int(min_years) <= int(most_likely_years) <= int(max_years)
    or int(max_years) > 99
):
    print("\nProblem with input years.", file=sys.stderr)
    print("Requires Min < ML < Max and Max < 100", file=sys.stderr)
    sys.exit(1)


def montecarlo(returns):
    case_count = 0
    bankrupt_count = 0
    outcome = []

    while case_count < int(num_cases):
        investments = int(start_value)
        start_year = random.randrange(0, len(returns))
        duration = int(
            random.triangular(
                int(min_years),
                int(max_years),
                int(most_likely_years),
            )
        )
        end_year = start_year + duration
        lifespan = [i for i in range(start_year, end_year)]
        bankrupt = "no"

        lifespan_returns = []
        lifespan_infl = []
        for i in lifespan:
            lifespan_returns.append(returns[i % len(returns)])
            lifespan_infl.append(infl_rate[i % len(infl_rate)])

        for index, i in enumerate(lifespan_returns):
            infl = lifespan_infl[index]

            if index == 0:
                withdraw_infl_adj = int(withdrawal)
            else:
                withdraw_infl_adj = int(withdraw_infl_adj * (1 + infl))

            investments -= withdraw_infl_adj
            investments = int(investments * (1 + i))

            if investments <= 0:
                bankrupt = "yes"
                break

        if bankrupt == "yes":
            outcome.append(0)
            bankrupt_count += 1
        else:
            outcome.append(investments)

        case_count += 1

    return outcome, bankrupt_count


def bankrupt_prob(outcome, bankrupt_count):
    total = len(outcome)
    if total == 0:
        print("Error: No outcomes generated.")
        return None

    odds = round(100 * bankrupt_count / total, 1)

    print("\nInvestment type: {}".format(invest_type))
    print("Starting value: ${:,}".format(int(start_value)))
    print("Annual Withdrawal: ${:,}".format(int(withdrawal)))
    print(
        "Years in Retirement: Min {}, ML {}, Max {}".format(
            min_years,
            most_likely_years,
            max_years,
        )
    )
    print("Number of runs: {:,}\n".format(len(outcome)))
    print("Odds of going bankrupt: {}%\n".format(odds))
    print("Average outcome: ${:,}".format(int(sum(outcome) / total)))
    print("Median outcome: ${:,}".format(int(sorted(outcome)[int(total / 2)])))
    print("Best case: ${:,}".format(max(i for i in outcome)))
    print("Worst case: ${:,}".format(min(i for i in outcome)))

    return odds


def main():
    outcome, bankrupt_count = montecarlo(investment_type_args[invest_type])
    odds = bankrupt_prob(outcome, bankrupt_count)
    plotdata = outcome[:3000]
    plt.figure(
        "Outcome by Case (showing first {} runs)".format(len(plotdata)),
        figsize=(16, 5),
    )
    index = [i + 1 for i in range(len(plotdata))]
    plt.bar(index, plotdata, color="black")
    plt.xlabel("Simulated Lives", fontsize=18)
    plt.ylabel("$ Remaining", fontsize=18)
    plt.ticklabel_format(style="plain", axis="y")
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))
    )
    plt.title(
        "Probability of running out of money = {}%".format(odds),
        fontsize=20,
        color="red",
    )
    plt.show()


if __name__ == "__main__":
    main()
