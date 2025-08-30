import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

def wrangle(training_dataframe, testing_dataframe):
    """
    Applies the full data preprocessing pipeline to both training and testing DataFrames.
    """
    try:
        is_df = isinstance(training_dataframe, pd.DataFrame) and isinstance(testing_dataframe, pd.DataFrame)
        if not is_df:
            raise TypeError("Both inputs should be pandas DataFrame objects")
        else:
            print("Inputs are pandas DataFrames")
    except NameError:
        print("Pandas is not imported.")
        return training_dataframe, testing_dataframe

    RevolvingUtilizationOfUnsecuredLines_uppercap = training_dataframe['RevolvingUtilizationOfUnsecuredLines'].quantile(0.99)
    training_dataframe['RevolvingUtilizationOfUnsecuredLines'] = training_dataframe['RevolvingUtilizationOfUnsecuredLines'].clip(upper=RevolvingUtilizationOfUnsecuredLines_uppercap)
    testing_dataframe['RevolvingUtilizationOfUnsecuredLines'] = testing_dataframe['RevolvingUtilizationOfUnsecuredLines'].clip(upper=RevolvingUtilizationOfUnsecuredLines_uppercap)

    mean_age = training_dataframe['age'].median()
    training_dataframe['age'] = training_dataframe['age'].apply(lambda x: mean_age if x < 18 else x)
    testing_dataframe['age'] = testing_dataframe['age'].apply(lambda x: mean_age if x < 18 else x)

    NumberOfTime30to59DaysPastDueNotWorse_median = training_dataframe['NumberOfTime30-59DaysPastDueNotWorse'].median()
    training_dataframe["NumberOfTime30-59DaysPastDueNotWorse"] = training_dataframe['NumberOfTime30-59DaysPastDueNotWorse'].replace([98, 96], NumberOfTime30to59DaysPastDueNotWorse_median)
    testing_dataframe["NumberOfTime30-59DaysPastDueNotWorse"] = testing_dataframe['NumberOfTime30-59DaysPastDueNotWorse'].replace([98, 96], NumberOfTime30to59DaysPastDueNotWorse_median)
    
    NumberOfTimes90DaysLate_median = training_dataframe['NumberOfTimes90DaysLate'].median()
    training_dataframe["NumberOfTimes90DaysLate"] = training_dataframe['NumberOfTimes90DaysLate'].replace([98, 96], NumberOfTimes90DaysLate_median)
    testing_dataframe["NumberOfTimes90DaysLate"] = testing_dataframe['NumberOfTimes90DaysLate'].replace([98, 96], NumberOfTimes90DaysLate_median)

    NumberOfTime60to89DaysPastDueNotWorse_median = training_dataframe['NumberOfTime60-89DaysPastDueNotWorse'].median()
    training_dataframe["NumberOfTime60-89DaysPastDueNotWorse"] = training_dataframe['NumberOfTime60-89DaysPastDueNotWorse'].replace([98, 96], NumberOfTime60to89DaysPastDueNotWorse_median)
    testing_dataframe["NumberOfTime60-89DaysPastDueNotWorse"] = testing_dataframe['NumberOfTime60-89DaysPastDueNotWorse'].replace([98, 96], NumberOfTime60to89DaysPastDueNotWorse_median)

    imputer = IterativeImputer(estimator=RandomForestRegressor(n_estimators=10, random_state=42, n_jobs=1), max_iter=10, random_state=42)
    training_dataframe_imputed_values = imputer.fit_transform(training_dataframe)
    testing_dataframe_imputed_values = imputer.transform(testing_dataframe)
    training_dataframe = pd.DataFrame(training_dataframe_imputed_values, columns=training_dataframe.columns)
    testing_dataframe = pd.DataFrame(testing_dataframe_imputed_values, columns=testing_dataframe.columns)

    training_dataframe['MonthlyIncome'] = training_dataframe['MonthlyIncome'].clip(lower=0)
    testing_dataframe['MonthlyIncome'] = testing_dataframe['MonthlyIncome'].clip(lower=0)
    
    monthly_income_upper_cap = training_dataframe['MonthlyIncome'].quantile(0.99)
    training_dataframe['MonthlyIncome'] = training_dataframe['MonthlyIncome'].clip(upper=monthly_income_upper_cap)
    testing_dataframe['MonthlyIncome'] = testing_dataframe['MonthlyIncome'].clip(upper=monthly_income_upper_cap)

    upper_cap_debt_ratio = training_dataframe['DebtRatio'].quantile(0.99)
    training_dataframe['DebtRatio'] = training_dataframe['DebtRatio'].clip(upper=upper_cap_debt_ratio)
    testing_dataframe['DebtRatio'] = testing_dataframe['DebtRatio'].clip(upper=upper_cap_debt_ratio)

    training_dataframe['NumberRealEstateLoansOrLines'] = training_dataframe['NumberRealEstateLoansOrLines'].clip(upper=17)
    testing_dataframe['NumberRealEstateLoansOrLines'] = testing_dataframe['NumberRealEstateLoansOrLines'].clip(upper=17)

    training_dataframe.rename(columns={
        "NumberOfTime30-59DaysPastDueNotWorse": "NumberOfTime30_59DaysPastDueNotWorse", 
        "NumberOfTime60-89DaysPastDueNotWorse": "NumberOfTime60_89DaysPastDueNotWorse"
    }, inplace=True)
    testing_dataframe.rename(columns={
        "NumberOfTime30-59DaysPastDueNotWorse": "NumberOfTime30_59DaysPastDueNotWorse", 
        "NumberOfTime60-89DaysPastDueNotWorse": "NumberOfTime60_89DaysPastDueNotWorse"
    }, inplace=True)
    
    return training_dataframe, testing_dataframe
