import streamlit as st
import pandas as pd
import repository.company_repository as comp
import repository.company_identifiers_repository as compid
import repository.income_statements_repository as income
import repository.balance_sheets_repository as balance

st.set_page_config(page_title="StockPlatform", layout="wide")
st.title("Company Financials")

ticker = st.text_input("Enter ticker symbol (e.g., IBM):")


if ticker:
    st.header(ticker + ' Fundamentals')

    comp_id = compid.get_id_by_ticker(ticker.upper())

    if comp_id is not None:
        
        # Company Section
        comp__data = comp.get_company(comp_id)
        df_comp_data = pd.DataFrame(comp__data, columns=['Company Id', 'Name'])
        comp_id_data = compid.get_company_identifiers(comp_id)
        df_compid_data = pd.DataFrame(comp_id_data, columns=['Company Id', 'Ticker', 'ISIN', 'WKN'])
        st.subheader("Comp Identifiers Data")
        st.write(f"**Name:** {df_comp_data['Name'].iloc[0]}")
        st.write(f"**Company Id:** {df_comp_data['Company Id'].iloc[0]}")
        st.write(f"**Ticker:** {df_compid_data['Ticker'].iloc[0]}")
        st.write(f"**ISIN:** {df_compid_data['ISIN'].iloc[0]}")
        st.write(f"**WKN:** {df_compid_data['WKN'].iloc[0]}")




        # Income Data Section


        income_data = income.get_income_statements(comp_id)
        df_income_data = pd.DataFrame(income_data, columns=['Income Id', 'Company Id', 'Year', 'Revenue', 'Gross Profit',
                                                            'Operating Income', 'Net Income', 'EBIT', 'EBITDA',
                                                            'Cost of Revenue', 'Operating Expense', 'Interest Cost', 'Taxes', 'Checked'])

        full_df_income_data = df_income_data[['Year', 'Revenue', 'Gross Profit', 'Operating Income', 'Net Income', 'EBIT', 'EBITDA', 'Cost of Revenue',
                                            'Operating Expense', 'Interest Cost', 'Taxes']]

        focussed_df_income_data = df_income_data[['Year', 'Revenue', 'Gross Profit', 'EBIT', 'Net Income']]


        st.subheader("Income Data")

        show_all_income = st.checkbox("Show all columns", key="income_all")

        if show_all_income:
            display_df_income_data = full_df_income_data
        else:
            display_df_income_data = focussed_df_income_data

        st.dataframe(display_df_income_data,
                    column_config={
                        "Revenue": st.column_config.NumberColumn(format="$%,.0f"),
                        "Gross Profit": st.column_config.NumberColumn(format="$%,.0f"),
                        "Operating Income": st.column_config.NumberColumn(format="$%,.0f"),
                        "Net Income": st.column_config.NumberColumn(format="$%,.0f"),
                        "EBIT": st.column_config.NumberColumn(format="$%,.0f"),
                        "EBITDA": st.column_config.NumberColumn(format="$%,.0f"),
                        "Cost of Revenue": st.column_config.NumberColumn(format="$%,.0f"),
                        "Operating Expense": st.column_config.NumberColumn(format="$%,.0f"),
                        "Interest Cost": st.column_config.NumberColumn(format="$%,.0f"),
                        "Taxes": st.column_config.NumberColumn(format="$%,.0f")
                    })



        # Balance Sheet Section

        balance_data = balance.get_balance_sheets(comp_id)
        df_balance_data = pd.DataFrame(balance_data, columns=['Balance Id', 'Company Id', 'Year', 'Type', 'Total Assets', 'Total Current Assets',
                                                            'Cash', 'Receivables', 'Inventories', 'Properties, Plants & Equipment', 'Intangible Assets',
                                                            'Total Liabilities and Equity', 'Short Debt', 'Long Debt', 'Total Debt', 'Total Liabilities',
                                                            'Total Equity', 'Retained Earnings', 'Total Shares', 'Treasury Shares', 'Shares Outstanding', 'Checked'])


        full_df_balance_data = df_balance_data[['Year', 'Total Assets', 'Total Current Assets', 'Cash', 'Receivables',
                                                'Inventories', 'Properties, Plants & Equipment', 'Intangible Assets',
                                                'Total Liabilities and Equity', 'Short Debt', 'Long Debt', 'Total Debt', 'Total Liabilities',
                                                'Total Equity', 'Retained Earnings', 'Total Shares', 'Treasury Shares', 'Shares Outstanding']]


        focussed_df_balance_data = df_balance_data[['Year', 'Total Assets', 'Cash', 'Total Debt', 'Total Liabilities', 'Total Equity']]

        st.subheader("Balance Sheets")

        show_all_balance = st.checkbox("Show all columns", key="balance_all")

        if show_all_balance:
            display_df_balance_data = full_df_balance_data
        else:
            display_df_balance_data = focussed_df_balance_data

        st.dataframe(display_df_balance_data, column_config={
                        "Total Assets": st.column_config.NumberColumn(format="$%,.0f"),
                        "Total Current Assets": st.column_config.NumberColumn(format="$%,.0f"),
                        "Cash": st.column_config.NumberColumn(format="$%,.0f"),
                        "Receivables": st.column_config.NumberColumn(format="$%,.0f"),
                        "Inventories": st.column_config.NumberColumn(format="$%,.0f"),
                        "Properties, Plants & Equipment": st.column_config.NumberColumn(format="$%,.0f"),
                        "Intangible Assets": st.column_config.NumberColumn(format="$%,.0f"),
                        "Total Liabilities and Equity": st.column_config.NumberColumn(format="$%,.0f"),
                        "Short Debt": st.column_config.NumberColumn(format="$%,.0f"),
                        "Long Debt": st.column_config.NumberColumn(format="$%,.0f"),
                        "Total Debt": st.column_config.NumberColumn(format="$%,.0f"),
                        "Total Liabilities": st.column_config.NumberColumn(format="$%,.0f"),
                        "Total Equity": st.column_config.NumberColumn(format="$%,.0f"),
                        "Retained Earnings": st.column_config.NumberColumn(format="$%,.0f"),
                        "Total Shares": st.column_config.NumberColumn(format="%,.0f"),
                        "Treasury Shares": st.column_config.NumberColumn(format="%,.0f"),
                        "Shares Outstanding": st.column_config.NumberColumn(format="%,.0f")
                    })
