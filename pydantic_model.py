from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated


class UserInput(BaseModel):

    age: Annotated[int, Field(..., ge=10, le=110, title="Age of the borrower", description="age of the borrower")]
    total_unsecured_balance: Annotated[float, Field(..., ge=0, title="Total Unsecured Credit Limit", description="The total amount of money borrower currently owe on all your credit cards and personal lines of credit (in dollers)")]
    total_unsecured_credit_limit: Annotated[float, Field(..., ge=0, title="Total Unsecured Credit Limit", description="The total credit limit available across all of the borrower's credit cards and personal lines of credit (in dollers)")]
    total_monthly_debt_payment: Annotated[float, Field(..., ge=0, title="Total Monthly debt payment", description="Total amout of debt that borrower pays every month (in dollers)")]
    MonthlyIncome: Annotated[float, Field(..., ge=0, title="Total Monthly Income", description="Total Monthly income of the borrower (in dollers)")]
    NumberOfOpenCreditLinesAndLoans: Annotated[int, Field(..., ge=0, le=60, title="Number of Open Credit Line", description="Number of open credit accounts (credit cards, car loans, etc.) Example: If the borrower have 2 credit cards + 1 car loan + 1 personal loan = 4 total.")]
    NumberOfTime30_59DaysPastDueNotWorse: Annotated[int, Field(..., ge=0, le=15, title="Number of times late by 30 - 59 days", description="How many times the borrower has been late (by 30–59 days) on a payment in the past. Example: If you missed your credit card bill and paid it 40 days late, it counts here.")]
    NumberOfTimes90DaysLate: Annotated[int, Field(..., ge=0, le=20, title="Number of time late by 90 days", description="Number of times borrower has been 90 days or more late in payment. Example: If the borrower missed payments and paid after 3 months, it counts here.")]
    NumberRealEstateLoansOrLines: Annotated[int, Field(..., ge=0, le=60, title="Number of Mortgage or Real Estate lones", description="Number of mortgage or real estate loans (like home loans). Example: Someone may have 1 house loan and 1 plot loan = 2.")]
    NumberOfTime60_89DaysPastDueNotWorse: Annotated[int, Field(..., ge=0, le=12, title="Number of times late by 60 - 89 days", description="Number of times borrower was late by 60 to 89 days in payments. Example: If the borrower missed paying your bill for 2 months.")]
    NumberOfDependents: Annotated[int, Field(..., ge=0, le=10, title="Number of Dependents", description="Number of people financially dependent on the borrower (children, elderly parents, etc.). Example: If the borrower have 2 kids and 1 elderly parent = 3 dependents.")]

    @computed_field
    @property
    def RevolvingUtilizationOfUnsecuredLines(self) -> float:
        if self.total_unsecured_credit_limit == 0:
            return 0.0
        return self.total_unsecured_balance / self.total_unsecured_credit_limit
    
    @computed_field
    @property
    def DebtRatio(self) -> float:
        if self.MonthlyIncome == 0:
            return self.total_monthly_debt_payment
        else:
            return self.total_monthly_debt_payment / self.MonthlyIncome


