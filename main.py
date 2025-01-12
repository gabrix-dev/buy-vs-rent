from matplotlib import pyplot as plt
from house_investment import HouseInvestment, AnalysisParams
import numpy as np

params = AnalysisParams(
    house_price=300000,
    mortgage_interest=0.02,
    mortgage_term=30,
    stock_market_return=0.06,
    initial_rent_price=1100,
    monthly_net_income=2600,
    years_of_study=40,
)

analysis = HouseInvestment(params)

# Plot: Complete value evolution comparison
plt.figure(figsize=(12, 6))
(
    house_values,
    house_stock_values,
    combined_values,
    rent_stock_values,
    yearly_house_savings,
    yearly_rent_savings,
    yearly_house_expenses,
    yearly_rent_expenses,
    financial_details,
) = analysis.calculate_value_evolution()
years = range(1, params.years_of_study + 1)

# Plot all value series
plt.plot(years, house_values, label=f"House Value (Final: {house_values[-1]:,.0f}€)", color="gray")
plt.plot(
    years, house_stock_values, label=f"Buy Scenario Stocks (Final: {house_stock_values[-1]:,.0f}€)", color="lightblue"
)
plt.plot(years, combined_values, label=f"Buy Total (Final: {combined_values[-1]:,.0f}€)", color="blue")
plt.plot(years, rent_stock_values, label=f"Rent Total (Final: {rent_stock_values[-1]:,.0f}€)", color="orange")

plt.xlabel("Years")
plt.ylabel("Value (€)")
plt.title("Value Evolution Comparison")
plt.legend()
plt.grid(True)

# Add parameters text box
params_text = (
    f"Parameters:\n"
    f"House price: {params.house_price:,.0f}€\n"
    f"Mortgage interest: {params.mortgage_interest*100:.1f}%\n"
    f"Mortgage term: {params.mortgage_term} years\n"
    f"Stock market return: {params.stock_market_return:.1%}\n"
    f"Initial rent: {params.initial_rent_price:,.0f}€\n"
    f"Monthly net income: {params.monthly_net_income:,.0f}€"
)
plt.text(
    0.05,
    0.95,
    params_text,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)

# Add results text box
results_text = (
    f"Relevant numbers:\n"
    f'Buy scenario net worth: {financial_details["house_scenario_net_worth"]:,.0f}€\n'
    f'Rent scenario net worth: {financial_details["rent_scenario_net_worth"]:,.0f}€\n\n'
    f'Final house value: {financial_details["final_house_value"]:,.0f}€\n'
    f'Buy stock portfolio: {financial_details["house_stock_portfolio"]:,.0f}€\n'
    f'Rent stock portfolio: {financial_details["rent_stock_portfolio"]:,.0f}€\n\n'
    f'Initial monthly savings (Buy): {financial_details["initial_house_savings"]:,.0f}€\n'
    f'Initial monthly savings (Rent): {financial_details["initial_rent_savings"]:,.0f}€\n'
    f'Final monthly savings (Buy): {financial_details["final_house_savings"]:,.0f}€\n'
    f'Final monthly savings (Rent): {financial_details["final_rent_savings"]:,.0f}€'
)
plt.text(
    0.5,
    0.95,
    results_text,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)

plt.tight_layout()
plt.show()

# Plot for yearly expenses
plt.figure(figsize=(12, 6))
plt.plot(years, yearly_house_expenses, label="Buy Scenario Monthly Expenses")
plt.plot(years, yearly_rent_expenses, label="Rent Scenario Monthly Expenses")

plt.xlabel("Years")
plt.ylabel("Monthly Amount (€)")
plt.title("Monthly Expenses Comparison Over Time")
plt.legend()
plt.grid(True)

# Add parameters text box for expenses plot
params_text = (
    f"Initial values:\n"
    f"Monthly net income: {params.monthly_net_income:,.0f}€\n"
    f"Monthly life expenses: {params.initial_monthly_expenses:,.0f}€\n"
    f"Rent: {params.initial_rent_price:,.0f}€\n"
    f"House cost: {params.house_price:,.0f}€\n"
    f"Mortgage interest: {params.mortgage_interest*100:.1f}%\n"
    f"Loan duration: {params.mortgage_term} years\n"
    f"\nMonthly expenses:\n"
    f"Buy initial: {yearly_house_expenses[0]:,.0f}€\n"
    f"Buy final: {yearly_house_expenses[-1]:,.0f}€\n"
    f"Rent initial: {yearly_rent_expenses[0]:,.0f}€\n"
    f"Rent final: {yearly_rent_expenses[-1]:,.0f}€"
)
plt.text(
    0.05,
    0.95,
    params_text,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)
plt.tight_layout()
plt.show()

# Plot for yearly savings/investments
plt.figure(figsize=(12, 6))
plt.plot(years, yearly_house_savings, label="Buy Scenario Monthly Investment")
plt.plot(years, yearly_rent_savings, label="Rent Scenario Monthly Investment")

plt.xlabel("Years")
plt.ylabel("Monthly Amount (€)")
plt.title("Monthly Investment Comparison Over Time")
plt.legend()
plt.grid(True)

# Add parameters text box for savings plot
params_text = (
    f"Initial values:\n"
    f"Monthly net income: {params.monthly_net_income:,.0f}€\n"
    f"Monthly life expenses: {params.initial_monthly_expenses:,.0f}€\n"
    f"Rent: {params.initial_rent_price:,.0f}€\n"
    f"House cost: {params.house_price:,.0f}€\n"
    f"Mortgage interest: {params.mortgage_interest*100:.1f}%\n"
    f"Loan duration: {params.mortgage_term} years\n"
    f"\nMonthly investments:\n"
    f"Buy initial: {yearly_house_savings[0]:,.0f}€\n"
    f"Buy final: {yearly_house_savings[-1]:,.0f}€\n"
    f"Rent initial: {yearly_rent_savings[0]:,.0f}€\n"
    f"Rent final: {yearly_rent_savings[-1]:,.0f}€"
)
plt.text(
    0.05,
    0.95,
    params_text,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)
plt.tight_layout()
plt.show()

# Plot for stock market return analysis
plt.figure(figsize=(12, 6))
stock_returns = [r / 100 for r in range(5, 12)]  # 5% to 11%
final_values = []

for return_rate in stock_returns:
    test_params = AnalysisParams(
        house_price=params.house_price,
        mortgage_interest=params.mortgage_interest,
        mortgage_term=params.mortgage_term,
        stock_market_return=return_rate,
        initial_rent_price=params.initial_rent_price,
        monthly_net_income=params.monthly_net_income,
        years_of_study=params.years_of_study,
    )
    test_analysis = HouseInvestment(test_params)
    results = test_analysis.calculate_value_evolution()
    final_values.append({"buy": results[2][-1], "rent": results[3][-1]})  # combined_values  # rent_stock_values

x = np.arange(len(stock_returns))
width = 0.35

plt.bar(x - width / 2, [v["buy"] for v in final_values], width, label="Buy Scenario Total")
plt.bar(x + width / 2, [v["rent"] for v in final_values], width, label="Rent Scenario Total")

# Add value labels on top of each bar
for i in range(len(stock_returns)):
    plt.text(
        i - width / 2,
        final_values[i]["buy"],
        f'{final_values[i]["buy"]:,.0f}€',
        ha="center",
        va="bottom",
        rotation=90,
    )
    plt.text(
        i + width / 2,
        final_values[i]["rent"],
        f'{final_values[i]["rent"]:,.0f}€',
        ha="center",
        va="bottom",
        rotation=90,
    )

plt.xlabel("Stock Market Return")
plt.ylabel("Final Value (€)")
plt.title("Final Value by Stock Market Return")
plt.xticks(x, [f"{p:.0%}" for p in stock_returns], rotation=45, ha="right")
plt.legend()
plt.grid(True)

# Add parameters text box
params_text = (
    f"Parameters:\n"
    f"House price: {params.house_price:,.0f}€\n"
    f"Mortgage interest: {params.mortgage_interest*100:.1f}%\n"
    f"Mortgage term: {params.mortgage_term} years\n"
    f"Initial rent: {params.initial_rent_price:,.0f}€\n"
    f"Monthly net income: {params.monthly_net_income:,.0f}€\n"
    f"Years of study: {params.years_of_study} years"
)
plt.text(
    0.05,
    0.95,
    params_text,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)

plt.tight_layout()
plt.show()

# Plot for mortgage interest rate analysis
plt.figure(figsize=(12, 6))
interest_rates = [r / 1000 for r in range(5, 35, 5)]  # 0.5% to 3% in 0.5% steps
final_values = []

for interest_rate in interest_rates:
    test_params = AnalysisParams(
        house_price=params.house_price,
        mortgage_interest=interest_rate,
        mortgage_term=params.mortgage_term,
        stock_market_return=params.stock_market_return,
        initial_rent_price=params.initial_rent_price,
        monthly_net_income=params.monthly_net_income,
        years_of_study=params.years_of_study,
    )
    test_analysis = HouseInvestment(test_params)
    results = test_analysis.calculate_value_evolution()
    final_values.append({"buy": results[2][-1], "rent": results[3][-1]})  # combined_values  # rent_stock_values

x = np.arange(len(interest_rates))
width = 0.35

plt.bar(x - width / 2, [v["buy"] for v in final_values], width, label="Buy Scenario Total")
plt.bar(x + width / 2, [v["rent"] for v in final_values], width, label="Rent Scenario Total")

# Add value labels on top of each bar
for i in range(len(interest_rates)):
    plt.text(
        i - width / 2,
        final_values[i]["buy"],
        f'{final_values[i]["buy"]:,.0f}€',
        ha="center",
        va="bottom",
        rotation=90,
    )
    plt.text(
        i + width / 2,
        final_values[i]["rent"],
        f'{final_values[i]["rent"]:,.0f}€',
        ha="center",
        va="bottom",
        rotation=90,
    )

plt.xlabel("Mortgage Interest Rate")
plt.ylabel("Final Value (€)")
plt.title("Final Value by Mortgage Interest Rate")
plt.xticks(x, [f"{p:.1%}" for p in interest_rates], rotation=45, ha="right")
plt.legend()
plt.grid(True)

# Add parameters text box
params_text = (
    f"Parameters:\n"
    f"House price: {params.house_price:,.0f}€\n"
    f"Stock market return: {params.stock_market_return:.1%}\n"
    f"Mortgage term: {params.mortgage_term} years\n"
    f"Initial rent: {params.initial_rent_price:,.0f}€\n"
    f"Monthly net income: {params.monthly_net_income:,.0f}€\n"
    f"Years of study: {params.years_of_study} years"
)
plt.text(
    0.05,
    0.95,
    params_text,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)

plt.tight_layout()
plt.ylim(0, 10e6)  # Set y-axis from 0 to 10 million euros
plt.show()

# Plot for rent price analysis
plt.figure(figsize=(12, 6))
rent_prices = [500, 700, 900, 1100, 1300, 1500]
final_values = []

for rent_price in rent_prices:
    test_params = AnalysisParams(
        house_price=params.house_price,
        mortgage_interest=params.mortgage_interest,
        mortgage_term=params.mortgage_term,
        stock_market_return=params.stock_market_return,
        initial_rent_price=rent_price,
        monthly_net_income=params.monthly_net_income,
        years_of_study=params.years_of_study,
    )
    test_analysis = HouseInvestment(test_params)
    results = test_analysis.calculate_value_evolution()
    final_values.append({"buy": results[2][-1], "rent": results[3][-1]})

x = np.arange(len(rent_prices))
width = 0.35

plt.bar(x - width / 2, [v["buy"] for v in final_values], width, label="Buy Scenario Total")
plt.bar(x + width / 2, [v["rent"] for v in final_values], width, label="Rent Scenario Total")

# Add value labels on top of each bar
for i in range(len(rent_prices)):
    plt.text(
        i - width / 2,
        final_values[i]["buy"],
        f'{final_values[i]["buy"]:,.0f}€',
        ha="center",
        va="bottom",
        rotation=90,
    )
    plt.text(
        i + width / 2,
        final_values[i]["rent"],
        f'{final_values[i]["rent"]:,.0f}€',
        ha="center",
        va="bottom",
        rotation=90,
    )

plt.xlabel("Initial Monthly Rent")
plt.ylabel("Final Value (€)")
plt.title("Final Value by Initial Rent Price")
plt.xticks(x, [f"{p:,}€" for p in rent_prices], rotation=45, ha="right")
plt.legend()
plt.grid(True)

# Add parameters text box
params_text = (
    f"Parameters:\n"
    f"House price: {params.house_price:,.0f}€\n"
    f"Stock market return: {params.stock_market_return:.1%}\n"
    f"Mortgage interest: {params.mortgage_interest*100:.1f}%\n"
    f"Mortgage term: {params.mortgage_term} years\n"
    f"Monthly net income: {params.monthly_net_income:,.0f}€\n"
    f"Years of study: {params.years_of_study} years"
)
plt.text(
    0.6,
    0.95,
    params_text,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    horizontalalignment="left",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)

plt.tight_layout()
plt.ylim(0, 10e6)  # Set y-axis from 0 to 10 million euros
plt.show()
