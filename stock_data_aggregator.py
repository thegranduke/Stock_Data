import yfinance as yf
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import datetime
import time

# Get stock price data from Yahoo Finance
def collect_yfinance_data(symbol, start_date, end_date, interval='1d'):
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    if data.empty:
        print("Data collection failed")
    else:
        print("Data collected successfully")
    data.reset_index(inplace=True)

    # Standardise Column names
    data.columns = data.columns.str.lower()

    # Rename the 'date' column to 'datetime'
    data.rename(columns={'date': 'datetime'}, inplace=True)

    # Remove 'adj close' column from Yahoo Finance data
    if 'adj close' in data.columns:
        data.drop(columns=['adj close'], inplace=True)

    
    return data

# Used free API key from Alpha Vantage
def collect_alpha_vantage_data(symbol, api_key, output_size):
    ts = TimeSeries(key="Z5CWMEJRQWYBT4R3", output_format='pandas')
    data, _ = ts.get_daily(symbol=symbol, outputsize= output_size)
    data.reset_index(inplace=True)

    # Rename the 'date' column to 'datetime'
    data.rename(columns={'date': 'datetime'}, inplace=True)

    # Standardise Column names
    data.columns = data.columns.str.lower()
    
    # Remove leading numbers and periods from the column names
    data.columns = data.columns.str.replace(r'^\d+\.\s*', '', regex=True)  # Remove leading numbers and periods
    data.columns = data.columns.str.strip()  # Remove any leading or trailing whitespace

    return data

def toCsv(data, filename):
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def toExcel(data, filename):
    # Remove timezone from datetime since excel does not support timezones
    data['datetime'] = data['datetime'].dt.tz_localize(None)
    data.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def clean_stock_data(data):
    # Remove any duplicate rows in the data
    data.drop_duplicates(inplace=True)

    # Handle missing values by forward filling and backward filling
    data.ffill(inplace=True)
    data.bfill(inplace=True)

    # Ensurint data has correct datatypes
    data['datetime'] = pd.to_datetime(data['datetime'])
    numeric_columns = ['open', 'high', 'low', 'close', 'volume']
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Correcting timezones
    try:
        data['datetime'] = data['datetime'].dt.tz_localize("UTC")
    except TypeError:
        print("Timezone already set")

    # Standardise Column names
    data.columns = data.columns.str.lower()

    # Sort data by date
    data.sort_values(by='datetime', inplace=True)

    # Remove non-trading days
    data = data[data["datetime"].dt.dayofweek < 5]

    return data

def compare_data(yf_data, av_data):
    # Align data by date
    print("yfinance_data columns:", yf_data.columns)
    print("alpha_vantage_data columns:", av_data.columns)

    # Ensure 'Datetime' column in yf_data and 'date' in av_data
    if 'datetime' not in yf_data.columns:
        raise KeyError("The 'datetime' column is missing in the Yahoo Finance data.")
    if 'datetime' not in av_data.columns:
        raise KeyError("The 'datetime' column is missing in the Alpha Vantage data.")
    
    # Reindex Alpha Vantage data to match the dates of Yahoo Finance data
    yf_data.set_index('datetime', inplace=True)
    av_data.set_index('datetime', inplace=True)

    # Round numeric columns to 2 decimal places (for comparison since differnt sites have different granularity)
    yf_data = yf_data.round(2)
    av_data = av_data.round(2)

    # Reindex Alpha Vantage data to match the dates of Yahoo Finance data
    av_data = av_data.reindex(yf_data.index)

    # Compare the data
    comparison = yf_data.compare(av_data)
    
    # Report differences
    if not comparison.empty:
        print("Differences found:")
        print(comparison)
    else:
        print("No differences found. The data is consistent.")

    return comparison

def main():
    # Set the start and end date for the data collection
    start_date = '2024-08-01'
    end_date = '2024-08-07'
    interval = '1d'
    symbol = 'AAPL'

    # Collect data from Yahoo Finance
    yfinance_data = collect_yfinance_data(symbol, start_date, end_date, interval)
    yfinance_data = clean_stock_data(yfinance_data)
    toCsv(yfinance_data, 'yfinance_stock_data.csv')

    # Collect data from Alpha Vantage
    alpha_vantage_data = collect_alpha_vantage_data('AAPL', 'Z5CWMEJRQWYBT4R3', 'full')
    alpha_vantage_data = clean_stock_data(alpha_vantage_data)
    toCsv(alpha_vantage_data, 'alpha_vantage_stock_data.csv')

    # Compare the data    
    compare_data(yfinance_data, alpha_vantage_data)

if __name__ == "__main__":
    main()








    




