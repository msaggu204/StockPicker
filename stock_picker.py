import yfinance as yf
import pandas as pd
# from alpha_vantage.fundamentaldata import FundamentalData

stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA']

def stock_metrics(stock):
    ticker = yf.Ticker(stock)
    info = ticker.info
    
    eps = info.get('trailingEps', 'N/A')
    pe_ratio = info.get('trailingPE', 'N/A')
    roe = info.get('returnOnEquity', 'N/A')
    debt_to_equity = info.get('debtToEquity', 'N/A')
    free_cash_flow = info.get('freeCashflow', 'N/A')
    
    return {
        'Ticker': stock,
        'EPS': eps,
        'P/E Ratio': pe_ratio,
        'ROE': roe,
        'Debt to Equity': debt_to_equity,
        'Free Cash Flow': free_cash_flow
    }

def stock_growth_metrics(stock):
    try:
        ticker = yf.Ticker(stock)
        
        # Fetch income statement and balance sheet data
        income_stmt = ticker.income_stmt
        balance_sheet = ticker.balance_sheet

        # Fetch preferred dividends and shares outstanding
        preferred_dividends = income_stmt.loc['Preferred Stock Dividends'].sort_index().tail(3).values if 'Preferred Stock Dividends' in income_stmt.index else [0, 0, 0]
        common_shares = income_stmt.loc['Diluted Average Shares'].sort_index().tail(3).values if 'Diluted Average Shares' in income_stmt.index else None

        # Debug: Print income statement and balance sheet to verify data
        print(f"Income Statement for {stock}:")
        print(income_stmt)
        print(f"Balance Sheet for {stock}:")
        print(balance_sheet)

        if income_stmt is None or income_stmt.empty or common_shares is None:
            return {
                'Ticker': stock,
                'Revenue 3 Years Ago': 'N/A',
                'Revenue Last Year': 'N/A',
                'Revenue Growth (3 Years)': 'N/A',
                'Net Income 3 Years Ago': 'N/A',
                'Net Income Last Year': 'N/A',
                'Net Income Growth (3 Years)': 'N/A',
                'EPS 3 Years Ago': 'N/A',
                'EPS Last Year': 'N/A',
                'EPS Growth (3 Years)': 'N/A'
            }

        # Extract Revenue and Net Income for the last 3 years
        revenue_values = income_stmt.loc['Total Revenue'].sort_index().tail(3).values if 'Total Revenue' in income_stmt.index else None
        net_income_values = income_stmt.loc['Net Income'].sort_index().tail(3).values if 'Net Income' in income_stmt.index else None

        if revenue_values is None or net_income_values is None or len(revenue_values) < 3 or len(net_income_values) < 3:
            return {
                'Ticker': stock,
                'Revenue 3 Years Ago': 'N/A',
                'Revenue Last Year': 'N/A',
                'Revenue Growth (3 Years)': 'N/A',
                'Net Income 3 Years Ago': 'N/A',
                'Net Income Last Year': 'N/A',
                'Net Income Growth (3 Years)': 'N/A',
                'EPS 3 Years Ago': 'N/A',
                'EPS Last Year': 'N/A',
                'EPS Growth (3 Years)': 'N/A'
            }

        # Calculate EPS for each year: (Net Income - Preferred Dividends) / Common Shares
        eps_values = [(net_income - preferred_div) / common_share 
                      for net_income, preferred_div, common_share in zip(net_income_values, preferred_dividends, common_shares)]

        # Extract values after ensuring correct order
        revenue_3_years_ago, revenue_2_years_ago, revenue_last_year = revenue_values
        net_income_3_years_ago, net_income_2_years_ago, net_income_last_year = net_income_values
        eps_3_years_ago, eps_2_years_ago, eps_last_year = eps_values

        # Calculate growth percentages
        revenue_growth = ((revenue_last_year - revenue_3_years_ago) / abs(revenue_3_years_ago)) * 100 if revenue_3_years_ago else 'N/A'
        net_income_growth = ((net_income_last_year - net_income_3_years_ago) / abs(net_income_3_years_ago)) * 100 if net_income_3_years_ago else 'N/A'
        eps_growth = ((eps_last_year - eps_3_years_ago) / abs(eps_3_years_ago)) * 100 if eps_3_years_ago else 'N/A'

        return {
            'Ticker': stock,
            'Revenue 3 Years Ago': revenue_3_years_ago,
            'Revenue Last Year': revenue_last_year,
            'Revenue Growth (3 Years)': f"{revenue_growth:.2f}%" if isinstance(revenue_growth, float) else 'N/A',
            'Net Income 3 Years Ago': net_income_3_years_ago,
            'Net Income Last Year': net_income_last_year,
            'Net Income Growth (3 Years)': f"{net_income_growth:.2f}%" if isinstance(net_income_growth, float) else 'N/A',
            'EPS 3 Years Ago': eps_3_years_ago,
            'EPS Last Year': eps_last_year,
            'EPS Growth (3 Years)': f"{eps_growth:.2f}%" if isinstance(eps_growth, float) else 'N/A'
        }

    except Exception as e:
        print(f"Error fetching data for {stock}: {e}")
        return {
            'Ticker': stock,
            'Revenue 3 Years Ago': 'Error',
            'Revenue Last Year': 'Error',
            'Revenue Growth (3 Years)': 'Error',
            'Net Income 3 Years Ago': 'Error',
            'Net Income Last Year': 'Error',
            'Net Income Growth (3 Years)': 'Error',
            'EPS 3 Years Ago': 'Error',
            'EPS Last Year': 'Error',
            'EPS Growth (3 Years)': 'Error'
        }
        
if __name__ == '__main__':
    stock_data = [stock_metrics(stock) for stock in stocks]
    df = pd.DataFrame(stock_data)
    print(df)

    # Collect data for all stocks
    stock_growth_data = [stock_growth_metrics(stock) for stock in stocks]

    # Convert to DataFrame for easier visualization
    df_growth = pd.DataFrame(stock_growth_data)

    # Display the DataFrame
    print(df_growth)
