from matplotlib import pyplot as plt
from house_investment import HouseInvestment, AnalysisParams

params = AnalysisParams(
    house_price=300000,
    mortgage_interest=0.025,
    mortgage_term=30,
    stock_market_return=0.07,
    initial_rent_price=1200,
    monthly_net_income=3000,
    years_of_study=30,
)

analysis = HouseInvestment(params)

# Plot: Complete value evolution comparison
plt.figure(figsize=(12, 6))
house_values, house_stock_values, combined_values, rent_stock_values, financial_details = (
    analysis.calculate_value_evolution()
)
years = range(1, params.years_of_study + 1)

# Plot all value series
plt.plot(years, house_values, label=f"House Value (Final: {house_values[-1]:,.0f}€)")
plt.plot(years, house_stock_values, label=f"House Scenario Stocks (Final: {house_stock_values[-1]:,.0f}€)")
plt.plot(years, combined_values, label=f"Combined Value (Final: {combined_values[-1]:,.0f}€)")
plt.plot(years, rent_stock_values, label=f"Rent Scenario Stocks (Final: {rent_stock_values[-1]:,.0f}€)")

plt.xlabel("Years")
plt.ylabel("Value (€)")
plt.title("Value Evolution Comparison")
plt.legend()
plt.grid(True)

# Add parameters text box
params_text = (
    f"Parameters:\n"
    f"House price: {params.house_price:,.0f}€\n"
    f"Mortgage interest: {params.mortgage_interest:.1%}\n"
    f"Mortgage term: {params.mortgage_term} years\n"
    f"Stock market return: {params.stock_market_return:.1%}\n"
    f"Initial rent: {params.initial_rent_price:,.0f}€\n\n"
    f"Financial details:\n"
    f'House scenario net worth: {financial_details["house_scenario_net_worth"]:,.0f}€\n'
    f'Rent scenario net worth: {financial_details["rent_scenario_net_worth"]:,.0f}€'
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
