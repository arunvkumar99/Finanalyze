import streamlit as st
import pandas as pd
from PyPDF2 import PdfFileReader
import openpyxl

# File Processing
def process_files(uploaded_files):
    consolidated_data = pd.DataFrame()

    for file in uploaded_files:
        if 'pdf' in file.type:
            pdf = PdfFileReader(file)
            text = ""
            for page_num in range(pdf.numPages):
                text += pdf.getPage(page_num).extractText()
            st.text_area("Extracted PDF Data:", text)
            # Convert text to DataFrame if needed
            # Example: consolidated_data = pdf_to_df(text)
        else:
            temp_df = pd.read_excel(file)
            consolidated_data = pd.concat([consolidated_data, temp_df])

    return consolidated_data

# Income Analysis
def income_analysis(df):
    monthly_income = df[df['category'] == 'income'].groupby(df['date'].dt.month)['amount'].sum()
    avg_monthly_income = monthly_income.mean()
    income_trend = monthly_income.pct_change()
    
    return avg_monthly_income, income_trend

# Expense Analysis
def expense_analysis(df):
    monthly_expenses = df[df['category'] != 'income'].groupby(df['date'].dt.month)['amount'].sum()
    avg_category_expense = df[df['category'] != 'income'].groupby('category')['amount'].mean()
    expense_trend = df[df['category'] != 'income'].groupby([df['date'].dt.month, 'category'])['amount'].sum().unstack().pct_change()
    
    return monthly_expenses, avg_category_expense, expense_trend

# Savings and Investments
def savings_analysis(df):
    monthly_income = df[df['category'] == 'income'].groupby(df['date'].dt.month)['amount'].sum()
    monthly_expenses = df[df['category'] != 'income'].groupby(df['date'].dt.month)['amount'].sum()
    monthly_savings = monthly_income - monthly_expenses
    
    return monthly_savings

# Debt Analysis
def debt_analysis(df):
    credit_card_debt = df[df['description'].str.contains('credit card payment', case=False, na=False)]['amount'].sum()
    
    return credit_card_debt

# High Expenditure Alerts
def expenditure_alerts(df):
    avg_category_expense = df[df['category'] != 'income'].groupby('category')['amount'].mean()
    monthly_category_expense = df[df['category'] != 'income'].groupby([df['date'].dt.month, 'category'])['amount'].sum().unstack()

    high_expenditure_alerts = {}
    for category in monthly_category_expense.columns:
        high_months = monthly_category_expense[monthly_category_expense[category] > 1.5 * avg_category_expense[category]].index.tolist()
        if high_months:
            high_expenditure_alerts[category] = high_months

    return high_expenditure_alerts

# Financial Health Score
def financial_health_score(df):
    avg_monthly_income, _ = income_analysis(df)
    monthly_savings = savings_analysis(df)
    avg_monthly_savings = monthly_savings.mean()
    credit_card_debt = debt_analysis(df)

    score = avg_monthly_savings / avg_monthly_income - credit_card_debt / avg_monthly_income
    score = round(score * 100)  # Convert score to a percentage for interpretability

    return score

# Main Function
def main():
    st.title("Financial Analysis App")

    uploaded_files = st.file_uploader("Upload your statements", type=['pdf', 'xls', 'xlsx', 'csv'], accept_multiple_files=True)

    if uploaded_files:
        consolidated_data = process_files(uploaded_files)
        
        st.subheader("Income Analysis")
        avg_monthly_income, income_trend = income_analysis(consolidated_data)
        st.write(f"Average Monthly Income: ${avg_monthly_income:.2f}")
        st.line_chart(income_trend, use_container_width=True)

        st.subheader("Expense Analysis")
        monthly_expenses, avg_category_expense, expense_trend = expense_analysis(consolidated_data)
        st.write(f"Average Monthly Expenses: ${monthly_expenses.mean():.2f}")
        st.line_chart(expense_trend, use_container_width=True)

        st.subheader("Savings Analysis")
        monthly_savings = savings_analysis(consolidated_data)
        st.write(f"Average Monthly Savings: ${monthly_savings.mean():.2f}")
        st.line_chart(monthly_savings, use_container_width=True)

        st.subheader("Debt Analysis")
        credit_card_debt = debt_analysis(consolidated_data)
        st.write(f"Credit Card Debt: ${credit_card_debt:.2f}")

        st.subheader("High Expenditure Alerts")
        high_expenditure_alerts = expenditure_alerts(consolidated_data)
        for category, months in high_expenditure_alerts.items():
            st.write(f"In category {category}, higher than average expenditures were observed in months: {', '.join(map(str, months))}")

        st.subheader("Financial Health Score")
        score = financial_health_score(consolidated_data)
        st.write(f"Your Financial Health Score is: {score} (Higher is better)")

if __name__ == "__main__":
    main()
