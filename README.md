# Credit Risk Prediction

## About the Data
The dataset for this project is from the Kaggle competition, "Give Me Some Credit." It contains historical data on 150,000 borrowers. The features have been anonymized and represent various aspects of a person's financial behavior and history.

[link](https://www.kaggle.com/competitions/GiveMeSomeCredit/data)

| Feature Name | Description |
| :--- | :--- |
| `SeriousDlqin2yrs` | **Target Variable:** A binary indicator of whether the person experienced serious delinquency in the last two years. (1 = Yes, 0 = No). |
| `RevolvingUtilizationOfUnsecuredLines` | The total balance on all unsecured lines of credit (e.g., credit cards) divided by the total credit limits. |
| `age` | The age of the borrower in years. |
| `NumberOfTime30-59DaysPastDueNotWorse` | The number of times the borrower was 30-59 days past due on a payment in the last two years. |
| `DebtRatio` | The ratio of a person's total monthly debt payments to their monthly gross income. |
| `MonthlyIncome` | The borrower's monthly income. |
| `NumberOfOpenCreditLinesAndLoans` | The number of open credit accounts and loans. |
| `NumberOfTimes90DaysLate` | The number of times the borrower was 90 days or more past due on a payment. |
| `NumberRealEstateLoansOrLines` | The number of mortgage and real estate loans. |
| `NumberOfTime60-89DaysPastDueNotWorse` | The number of times the borrower was 60-89 days past due on a payment in the last two years. |
| `NumberOfDependents` | The number of dependents in the household. |

---

## 🚧 Challenges
* **Imbalanced Dataset:** The number of positive cases (`SeriousDlqin2yrs` = 1) is significantly smaller than the number of negative cases (`SeriousDlqin2yrs` = 0). This will require special handling during model training, such as using appropriate evaluation metrics (e.g., F1-score, AUC-ROC) and techniques like oversampling or class weighting.
* **Missing Data:** The `MonthlyIncome` feature has a large number of missing values that will need to be addressed through imputation or other data preprocessing techniques.
* **Outliers:** Some features, particularly `age` and the past-due columns, contain outliers that need to be handled to ensure model robustness.

## Problem Solving Approch

Some of the column have very big outliers. I used quantile and clip method to solve this probelm. Replaced wrong entries with median. Imputed with Iterative imputer so that the distribution of the data does not get affected much.

EDA to extract feature relations and distributions. Graphing plots using Matplotlib and Seaborn.

Experimente with Balanced Bagging Classifier and Cost Sensitive Learning to handle Imbalance in the dataset. Used Stacking Classifier to get the best result. RandomForest, XGBoost, LightGBM base and Logistic Regression as Meta model.

Achived AUC score of 0.87 and the Score on Kaggle is 0.865
