from investment_analysis import HouseInvestment, InvestmentConfig, AnalysisParams
import matplotlib.pyplot as plt
import numpy as np

# Spanish terms used:
# - catastral: Official property value determined by the government for tax purposes
# - ibi: Annual property tax based on the catastral value (Impuesto sobre Bienes Inmuebles)

params = AnalysisParams(
    house_price=300000,
    mortgage_interest=0.025,
    mortgage_term=30,
    stock_market_return=0.07,
    initial_rent_price=1200,
)

analysis = HouseInvestment(params)

# Plot 1: Evolution over time
plt.figure(figsize=(12, 6))
house_values, stock_values, details = analysis.calculate_value_evolution()
years = range(1, params.mortgage_term + 1)

# Updated legend labels with final values
final_house_value = house_values[-1]
final_stock_value = stock_values[-1]
plt.plot(years, house_values, label=f"House Value (Final: {final_house_value:,.0f}€)")
plt.plot(years, stock_values, label=f"Stock Portfolio Value (Final: {final_stock_value:,.0f}€)")

plt.xlabel("Years")
plt.ylabel("Value (€)")
plt.title("Value Evolution Over Time")
plt.legend()
plt.grid(True)

# Update parameters text box for plot 1
params_text = (
    f"Parameters:\n"
    f"House price: {params.house_price:,.0f}€\n"
    f"Mortgage interest: {params.mortgage_interest:.1%}\n"
    f"Mortgage term: {params.mortgage_term} years\n"
    f"Stock market return: {params.stock_market_return:.1%}\n"
    f"Initial rent: {params.initial_rent_price:,.0f}€\n\n"
    f"Financial details:\n"
    f'Initial payment: {details["initial_payment_total"]:,.0f}€\n'
    f'Monthly cost: {details["monthly_cost_total"]:,.0f}€\n'
    f'Initial monthly investment: {details["monthly_investment"]:,.0f}€\n'
    f'Total rent: {details["total_rent"]:,.0f}€\n'
    f'Total house expense: {details["total_house_expense"]:,.0f}€\n'
    f'Total interest: {details["total_interest"]:,.0f}€'
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

# Plot 2: Mortgage terms analysis
plt.figure(figsize=(12, 6))
terms = list(range(20, 31))
results = analysis.analyze_mortgage_terms(terms)

x = np.arange(len(terms))
width = 0.35

plt.bar(x - width / 2, results["house"], width, label="House Value")
plt.bar(x + width / 2, results["stocks"], width, label="Stock Portfolio Value")
plt.xlabel("Mortgage Term (years)")
plt.ylabel("Final Value (€)")
plt.title("Final Value by Mortgage Term")
plt.xticks(
    x,
    [f'{p} years\n{results["details"][i]["monthly_cost_total"]:,.0f}€/month' for i, p in enumerate(terms)],
    rotation=45,
    ha="right",
)
plt.legend()
plt.grid(True)

# Add parameters text box for plot 2
params_text_2 = (
    f"Parameters:\n"
    f"House price: {params.house_price:,.0f}€\n"
    f"Mortgage interest: {params.mortgage_interest:.1%}\n"
    f"Stock market return: {params.stock_market_return:.1%}\n"
    f"Initial rent: {params.initial_rent_price:,.0f}€\n"
    f'Initial payment: {results["details"][0]["initial_payment_total"]:,.0f}€'
)
plt.text(
    0.05,
    0.05,
    params_text_2,
    transform=plt.gca().transAxes,
    verticalalignment="bottom",
    horizontalalignment="left",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)
plt.tight_layout()
plt.show()

# Plot 3: Rental price analysis
plt.figure(figsize=(12, 6))
rent_prices = list(range(500, 1501, 100))
rent_results = analysis.analyze_rent_prices(rent_prices)

x = np.arange(len(rent_prices))
width = 0.35

plt.bar(x - width / 2, rent_results["house"], width, label="House Value")
plt.bar(x + width / 2, rent_results["stocks"], width, label="Stock Portfolio Value")
plt.xlabel("Initial Rent Price (€)")
plt.ylabel("Final Value (€)")
plt.title("Final Value by Rent Price")
plt.xticks(
    x,
    [f'{p}€\n{rent_results["details"][i]["monthly_investment"]:,.0f}€ inv/month' for i, p in enumerate(rent_prices)],
    rotation=45,
    ha="right",
)
plt.legend()
plt.grid(True)

# Add parameters text box for plot 3
params_text_3 = (
    f"Parameters:\n"
    f"House price: {params.house_price:,.0f}€\n"
    f"Mortgage interest: {params.mortgage_interest:.1%}\n"
    f"Mortgage term: {params.mortgage_term} years\n"
    f"Stock market return: {params.stock_market_return:.1%}\n"
    f'Initial payment: {rent_results["details"][0]["initial_payment_total"]:,.0f}€\n'
    f'Monthly cost: {rent_results["details"][0]["monthly_cost_total"]:,.0f}€'
)
plt.text(
    0.95,
    0.95,
    params_text_3,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    horizontalalignment="right",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)
plt.tight_layout()
plt.show()

# Plot 4: Stock market return analysis
plt.figure(figsize=(12, 6))
stock_returns = [r / 100 for r in range(4, 12)]  # 4% to 11%
return_results = analysis.analyze_stock_returns(stock_returns)

x = np.arange(len(stock_returns))
width = 0.35

plt.bar(x - width / 2, return_results["house"], width, label="House Value")
plt.bar(x + width / 2, return_results["stocks"], width, label="Stock Portfolio Value")

# Add value labels on top of each bar
for i in range(len(stock_returns)):
    # House value (left bar)
    plt.text(
        i - width / 2,
        return_results["house"][i],
        f'{return_results["house"][i]:,.0f}€',
        ha="center",
        va="bottom",
        rotation=90,
    )
    # Stock value (right bar)
    plt.text(
        i + width / 2,
        return_results["stocks"][i],
        f'{return_results["stocks"][i]:,.0f}€',
        ha="center",
        va="bottom",
        rotation=90,
    )

plt.xlabel("Stock Market Return")
plt.ylabel("Final Value (€)")
plt.title("Final Value by Stock Market Return")
plt.xticks(
    x,
    [f"{p:.0%}" for p in stock_returns],
    rotation=45,
    ha="right",
)
# Move legend to upper left
plt.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95))
plt.grid(True)

# Updated parameters text box for plot 4
params_text_4 = (
    f"Parameters:\n"
    f"House price: {params.house_price:,.0f}€\n"
    f"Mortgage interest: {params.mortgage_interest:.1%}\n"
    f"Mortgage term: {params.mortgage_term} years\n"
    f"Initial rent: {params.initial_rent_price:,.0f}€\n"
    f'Initial payment: {return_results["details"][0]["initial_payment_total"]:,.0f}€\n'
    f'Monthly cost: {return_results["details"][0]["monthly_cost_total"]:,.0f}€\n'
    f'Initial monthly investment: {return_results["details"][0]["monthly_investment"]:,.0f}€'
)
plt.text(
    0.05,
    0.5,
    params_text_4,
    transform=plt.gca().transAxes,
    verticalalignment="bottom",
    horizontalalignment="left",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)
plt.tight_layout()
plt.show()
