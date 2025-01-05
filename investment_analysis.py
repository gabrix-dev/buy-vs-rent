from dataclasses import dataclass
import numpy_financial as npf
from typing import Tuple, List


@dataclass
class AnalysisParams:
    house_price: float
    mortgage_interest: float
    mortgage_term: int
    stock_market_return: float
    initial_rent_price: float


@dataclass
class InvestmentConfig:
    # Spanish property-specific parameters
    catastral_value_percentage: float = 0.5  # % of house price that represents the official tax value
    ibi_percentage: float = 0.0066  # Annual property tax rate
    # General parameters
    maintenance_cost_percentage: float = 0.01
    appraisal_notary_percentage: float = 0.1
    monthly_community_fees: float = 60
    annual_home_insurance_percentage: float = 0.001
    annual_garbage_tax: float = 100
    down_payment_percentage: float = 0.2
    annual_house_appreciation: float = 0.02
    annual_rent_increase: float = 0.02


class HouseInvestment:
    def __init__(
        self,
        params: AnalysisParams,
        config: InvestmentConfig = InvestmentConfig(),
    ):
        self.params = params
        self.config = config

    def _calculate_initial_payments(self, house_price: float) -> tuple[float, float]:
        down_payment = house_price * self.config.down_payment_percentage
        appraisal_notary = house_price * self.config.appraisal_notary_percentage
        return down_payment, appraisal_notary

    def _calculate_monthly_costs(self, house_price: float) -> float:
        catastral_value = house_price * self.config.catastral_value_percentage

        monthly_ibi_tax = (self.config.ibi_percentage * catastral_value) / 12
        monthly_maintenance = (self.config.maintenance_cost_percentage * house_price) / 12
        monthly_insurance = (self.config.annual_home_insurance_percentage * house_price) / 12
        monthly_garbage_tax = self.config.annual_garbage_tax / 12

        monthly_ownership_costs = (
            monthly_maintenance
            + monthly_ibi_tax
            + self.config.monthly_community_fees
            + monthly_insurance
            + monthly_garbage_tax
        )
        return monthly_ownership_costs

    def _calculate_monthly_payment(self, house_price: float, down_payment: float, mortgage_term: int) -> float:
        loan_amount = house_price - down_payment
        n_months = mortgage_term * 12
        print(f"Monthly payment: {npf.pmt(self.params.mortgage_interest / 12, n_months, -loan_amount)}")
        return npf.pmt(self.params.mortgage_interest / 12, n_months, -loan_amount)

    def calculate_value_evolution(self, params: AnalysisParams = None) -> Tuple[List[float], List[float], dict]:
        if params is None:
            params = self.params

        down_payment, appraisal_notary = self._calculate_initial_payments(params.house_price)
        initial_payment_total = down_payment + appraisal_notary
        monthly_ownership_costs = self._calculate_monthly_costs(params.house_price)
        monthly_payment = self._calculate_monthly_payment(params.house_price, down_payment, params.mortgage_term)
        monthly_cost_total = monthly_payment + monthly_ownership_costs
        print(f"Monthly cost total: {monthly_cost_total}")
        monthly_investment = monthly_cost_total - params.initial_rent_price

        # Store financial details
        financial_details = {
            "initial_payment_total": initial_payment_total,
            "monthly_cost_total": monthly_cost_total,
            "monthly_investment": monthly_investment,
        }

        # Tracking variables
        total_interest = 0
        total_rent = 0
        total_monthly_costs = 0
        loan_balance = params.house_price - down_payment

        house_value = params.house_price
        stock_portfolio_value = initial_payment_total
        rent_price = params.initial_rent_price
        house_values = []
        stock_values = []

        for i in range(params.mortgage_term):
            for j in range(12):
                # Calculate monthly interest
                monthly_interest = loan_balance * (params.mortgage_interest / 12)
                total_interest += monthly_interest

                # Update remaining capital
                principal_payment = monthly_payment - monthly_interest
                loan_balance -= principal_payment

                # Update total rent
                total_rent += rent_price

                monthly_investment = monthly_cost_total - rent_price
                if monthly_investment > 0:
                    stock_portfolio_value += monthly_investment
                    print(f"Year {i} - Month {j} - Stock portfolio investment: {monthly_investment}")
                else:
                    print(f"Year {i} - Month {j} - No investment, rental is higher than costs: {rent_price}")

                total_monthly_costs += monthly_cost_total

            house_value *= 1 + self.config.annual_house_appreciation
            stock_portfolio_value *= 1 + params.stock_market_return
            rent_price *= 1 + self.config.annual_rent_increase

            house_values.append(house_value)
            stock_values.append(stock_portfolio_value)

        # Update financial details with totals
        total_house_expense = initial_payment_total + total_monthly_costs
        financial_details.update(
            {"total_interest": total_interest, "total_rent": total_rent, "total_house_expense": total_house_expense}
        )

        print(f"House value: {house_values[-1]}")
        print(f"Stock portfolio value: {stock_values[-1]}")
        print(f"Total interest paid: {total_interest:,.2f}")
        print(f"Total rent paid: {total_rent:,.2f}")
        return house_values, stock_values, financial_details

    def analyze_mortgage_terms(self, terms: List[int]) -> dict:
        """Analyzes the impact of different mortgage terms on final values."""
        final_values = {"house": [], "stocks": [], "details": []}

        for term in terms:
            new_params = AnalysisParams(
                house_price=self.params.house_price,
                mortgage_interest=self.params.mortgage_interest,
                mortgage_term=term,
                stock_market_return=self.params.stock_market_return,
                initial_rent_price=self.params.initial_rent_price,
            )
            house_values, stock_values, details = self.calculate_value_evolution(new_params)
            final_values["house"].append(house_values[-1])
            final_values["stocks"].append(stock_values[-1])
            final_values["details"].append(details)

        return final_values

    def analyze_rent_prices(self, rent_prices: List[float]) -> dict:
        """Analyzes the impact of different rent prices on final values."""
        final_values = {"house": [], "stocks": [], "details": []}

        for rent_price in rent_prices:
            new_params = AnalysisParams(
                house_price=self.params.house_price,
                mortgage_interest=self.params.mortgage_interest,
                mortgage_term=self.params.mortgage_term,
                stock_market_return=self.params.stock_market_return,
                initial_rent_price=rent_price,
            )
            house_values, stock_values, details = self.calculate_value_evolution(new_params)
            final_values["house"].append(house_values[-1])
            final_values["stocks"].append(stock_values[-1])
            final_values["details"].append(details)

        return final_values

    def analyze_stock_returns(self, returns: List[float]) -> dict:
        """Analyzes the impact of different stock market returns on final values."""
        final_values = {"house": [], "stocks": [], "details": []}

        for return_rate in returns:
            new_params = AnalysisParams(
                house_price=self.params.house_price,
                mortgage_interest=self.params.mortgage_interest,
                mortgage_term=self.params.mortgage_term,
                stock_market_return=return_rate,
                initial_rent_price=self.params.initial_rent_price,
            )
            house_values, stock_values, details = self.calculate_value_evolution(new_params)
            final_values["house"].append(house_values[-1])
            final_values["stocks"].append(stock_values[-1])
            final_values["details"].append(details)

        return final_values
