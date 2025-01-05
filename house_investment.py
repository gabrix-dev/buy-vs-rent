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
    monthly_net_income: float
    years_of_study: int
    annual_income_increase: float = 0.03
    initial_monthly_expenses: float = 1200
    annual_expenses_increase: float = 0.02


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

    def calculate_value_evolution(
        self, params: AnalysisParams = None
    ) -> Tuple[List[float], List[float], List[float], List[float], dict]:
        if params is None:
            params = self.params

        down_payment, appraisal_notary = self._calculate_initial_payments(params.house_price)
        initial_payment_total = down_payment + appraisal_notary
        monthly_ownership_costs = self._calculate_monthly_costs(params.house_price)
        monthly_payment = self._calculate_monthly_payment(params.house_price, down_payment, params.mortgage_term)

        # Initialize tracking variables
        monthly_income = params.monthly_net_income
        monthly_expenses = params.initial_monthly_expenses
        house_value = params.house_price
        rent_price = params.initial_rent_price

        # Scenario 1: House purchase
        house_stock_portfolio = 0  # Start at zero, house value is tracked separately
        # Scenario 2: Rent only
        rent_stock_portfolio = 0

        house_values = []
        house_stock_values = []
        rent_stock_values = []

        # Initial investment is reflected in negative net worth
        total_initial_cost = initial_payment_total

        for i in range(params.years_of_study):
            for j in range(12):
                # Calculate monthly savings in both scenarios
                disposable_income = monthly_income - monthly_expenses

                # Scenario 1: House purchase
                if i < params.mortgage_term:
                    house_monthly_costs = monthly_payment + monthly_ownership_costs
                    house_savings = disposable_income - house_monthly_costs
                else:
                    house_monthly_costs = monthly_ownership_costs
                    house_savings = disposable_income - house_monthly_costs

                # Scenario 2: Rent
                rent_savings = disposable_income - rent_price

                # Update stock portfolios
                house_stock_portfolio += house_savings
                rent_stock_portfolio += rent_savings

                # Apply monthly stock market returns
                house_stock_portfolio *= 1 + params.stock_market_return / 12
                rent_stock_portfolio *= 1 + params.stock_market_return / 12

            # Yearly updates
            monthly_income *= 1 + params.annual_income_increase
            monthly_expenses *= 1 + params.annual_expenses_increase
            house_value *= 1 + self.config.annual_house_appreciation
            rent_price *= 1 + self.config.annual_rent_increase

            house_values.append(house_value)
            house_stock_values.append(house_stock_portfolio)
            rent_stock_values.append(rent_stock_portfolio)

            # Calculate combined values (house + stock portfolio)
            combined_values = [h + s for h, s in zip(house_values, house_stock_values)]

        # Calculate final net worth for both scenarios
        house_final_worth = house_values[-1] + house_stock_portfolio - total_initial_cost
        rent_final_worth = rent_stock_values[-1]

        financial_details = {
            "house_scenario_net_worth": house_final_worth,
            "rent_scenario_net_worth": rent_final_worth,
            "final_house_value": house_values[-1],
            "house_stock_portfolio": house_stock_values[-1],
            "rent_stock_portfolio": rent_stock_values[-1],
        }

        return house_values, house_stock_values, combined_values, rent_stock_values, financial_details
