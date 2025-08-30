# app.py
import streamlit as st
import requests

# === Configure your FastAPI endpoint here ===
API_URL = "http://127.0.0.1:8000/predict"   # <-- change to your actual endpoint

st.set_page_config(page_title="Credit Risk Predictor", page_icon="💳", layout="centered")

st.title("💳 Credit Risk Predictor")
st.caption("Fill in the borrower details. Fields are validated and explained. "
           "Computed metrics are shown for transparency and are not user-editable.")

with st.sidebar:
    st.header("ℹ️ About the rules")
    st.markdown(
        """
- **Revolving Utilization of Unsecured Lines** = `total_unsecured_balance / total_unsecured_credit_limit`.  
- If **Total Unsecured Credit Limit = 0**, then:
  - Revolving Utilization is **0.0** by definition.
  - **Total Unsecured Balance is locked to 0** (not editable).
- **Debt Ratio** = 
  - `total_monthly_debt_payment` if **Monthly Income = 0**  
  - otherwise `total_monthly_debt_payment / Monthly Income`
        """
    )

st.subheader("Borrower Information")

# Layout rows
col1, col2 = st.columns(2)

# --- Core money/credit fields (limit first so balance can depend on it) ---
with col1:
    age = st.number_input(
        "Age of the borrower",
        min_value=10, max_value=110, value=30, step=1, format="%d",
        help="Age of the borrower in years. Range: 10–110."
    )

    total_unsecured_credit_limit = st.number_input(
        "Total Unsecured Credit Limit ($)",
        min_value=0.0, value=10000.0, step=100.0,
        help=("The total credit limit available across all credit cards and personal lines of credit "
              "(in dollars). Set to 0 if the borrower has no such accounts.")
    )

with col2:
    if total_unsecured_credit_limit == 0:
        # Force and lock balance to 0 when limit is 0
        total_unsecured_balance = st.number_input(
            "Total Unsecured Balance ($)",
            min_value=0.0, max_value=0.0, value=0.0, step=0.0, disabled=True,
            help=("Because Total Unsecured Credit Limit is 0, the balance must also be 0. "
                  "Revolving Utilization will be 0.0.")
        )
    else:
        # Allow entering a balance, but not exceeding the limit
        default_balance = min(5000.0, float(total_unsecured_credit_limit))
        total_unsecured_balance = st.number_input(
            "Total Unsecured Balance ($)",
            min_value=0.0,
            max_value=float(total_unsecured_credit_limit),
            value=default_balance,
            step=100.0,
            help=("The current amount owed on all unsecured credit (in dollars). "
                  "Cannot exceed the Total Unsecured Credit Limit.")
        )

# --- Income & payments ---
col3, col4 = st.columns(2)
with col3:
    total_monthly_debt_payment = st.number_input(
        "Total Monthly Debt Payment ($)",
        min_value=0.0, value=500.0, step=10.0,
        help="Total amount of debt paid every month (in dollars). Includes all loans/EMIs/credit cards."
    )
with col4:
    MonthlyIncome = st.number_input(
        "Total Monthly Income ($)",
        min_value=0.0, value=3000.0, step=50.0,
        help="Borrower’s total monthly income (in dollars). Set to 0 if no income."
    )

# --- Account counts & delinquencies ---
col5, col6 = st.columns(2)
with col5:
    NumberOfOpenCreditLinesAndLoans = st.number_input(
        "Number of Open Credit Accounts",
        min_value=0, max_value=60, value=5, step=1, format="%d",
        help=("Number of open credit accounts (credit cards, car loans, personal loans, etc.). "
              "Example: 2 credit cards + 1 car loan + 1 personal loan = 4.")
    )
    NumberOfTime30_59DaysPastDueNotWorse = st.number_input(
        "Times late by 30–59 days",
        min_value=0, max_value=15, value=0, step=1, format="%d",
        help=("Count of payments that were late by 30–59 days. "
              "Example: missed a credit card bill and paid it 40 days late → counts here.")
    )
    NumberOfTimes90DaysLate = st.number_input(
        "Times late by 90+ days",
        min_value=0, max_value=20, value=0, step=1, format="%d",
        help=("Count of payments late by 90 days or more (3+ months).")
    )

with col6:
    NumberRealEstateLoansOrLines = st.number_input(
        "Number of Mortgage or Real Estate Loans",
        min_value=0, max_value=60, value=1, step=1, format="%d",
        help=("Number of mortgage/real estate loans (e.g., home loan, plot loan).")
    )
    NumberOfTime60_89DaysPastDueNotWorse = st.number_input(
        "Times late by 60–89 days",
        min_value=0, max_value=12, value=0, step=1, format="%d",
        help=("Count of payments that were late by 60–89 days (about 2 months).")
    )
    NumberOfDependents = st.number_input(
        "Number of Dependents",
        min_value=0, max_value=10, value=0, step=1, format="%d",
        help=("People financially dependent on the borrower (children, elderly parents, etc.).")
    )

# --- Computed metrics (read-only, mirrored from your Pydantic model logic) ---
if total_unsecured_credit_limit == 0:
    revolving_utilization = 0.0
else:
    revolving_utilization = total_unsecured_balance / total_unsecured_credit_limit

if MonthlyIncome == 0:
    debt_ratio = total_monthly_debt_payment
else:
    debt_ratio = total_monthly_debt_payment / MonthlyIncome

st.subheader("Computed (read-only)")
c1, c2 = st.columns(2)
with c1:
    st.metric(
        "Revolving Utilization of Unsecured Lines",
        value=f"{revolving_utilization:.4f}",
        help="total_unsecured_balance / total_unsecured_credit_limit (0.0 when limit is 0)."
    )
with c2:
    st.metric(
        "Debt Ratio",
        value=f"{debt_ratio:.4f}",
        help=("total_monthly_debt_payment / MonthlyIncome (or equals total_monthly_debt_payment "
              "when MonthlyIncome = 0).")
    )

# --- Action ---
st.markdown("---")
send = st.button("🔮 Predict with Backend")

if send:
    # Enforce the constraint again before sending
    if total_unsecured_credit_limit == 0 and total_unsecured_balance != 0:
        total_unsecured_balance = 0.0

    payload = {
        "age": age,
        "total_unsecured_balance": total_unsecured_balance,
        "total_unsecured_credit_limit": total_unsecured_credit_limit,
        "total_monthly_debt_payment": total_monthly_debt_payment,
        "MonthlyIncome": MonthlyIncome,
        "NumberOfOpenCreditLinesAndLoans": NumberOfOpenCreditLinesAndLoans,
        "NumberOfTime30_59DaysPastDueNotWorse": NumberOfTime30_59DaysPastDueNotWorse,
        "NumberOfTimes90DaysLate": NumberOfTimes90DaysLate,
        "NumberRealEstateLoansOrLines": NumberRealEstateLoansOrLines,
        "NumberOfTime60_89DaysPastDueNotWorse": NumberOfTime60_89DaysPastDueNotWorse,
        "NumberOfDependents": NumberOfDependents
    }

    with st.expander("🔍 Debug: payload being sent"):
        st.json(payload)

    try:
        resp = requests.post(API_URL, json=payload, timeout=15)
        if resp.ok:
            result = resp.json()
            prob_default = result.get("Probability of Default ")

            st.success("✅ Request successful")
            st.subheader("📌 Model Prediction")
            st.markdown(
                f"<h3 style='color:#d9534f;'>Probability of Default: {prob_default}</h3>",
                unsafe_allow_html=True
            )

        else:
            st.error(f"❌ Error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"⚠️ Could not connect to API: {e}")