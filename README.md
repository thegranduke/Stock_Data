# Stock Data Collection and Comparison

This script collects and processes historical stock price data from Yahoo Finance and Alpha Vantage.

## Features

- **Data Collection:**
  - Retrieve daily(can be adjusted) stock price data for a specified symbol and date range from Yahoo Finance and Alpha Vantage.

- **Data Cleaning:**
  - Standardize column names.
  - Remove unnecessary columns and handle missing values.
  - Ensure consistent data types and timezone handling.
  - Sort data by date and filter out non-trading days.

- **Data Export:**
  - Save the cleaned data to CSV and Excel files.

- **Data Comparison:**
  - Align and compare the data from both sources to identify any discrepancies.

## Functions

- `collect_yfinance_data(symbol, start_date, end_date, interval)`: 
  - Downloads stock data from Yahoo Finance, processes it, and returns a cleaned DataFrame.

- `collect_alpha_vantage_data(symbol, api_key, output_size)`: 
  - Retrieves stock data from Alpha Vantage, processes it, and returns a cleaned DataFrame.

- `toCsv(data, filename)`: 
  - Exports the DataFrame to a CSV file.

- `toExcel(data, filename)`: 
  - Exports the DataFrame to an Excel file (timezone removed).

- `clean_stock_data(data)`: 
  - Cleans and preprocesses the stock data, including handling duplicates and missing values.

- `compare_data(yf_data, av_data)`: 
  - Compares data from Yahoo Finance and Alpha Vantage to find discrepancies.

## Usage

1. Set the `start_date`, `end_date`, and `symbol` in the `main()` function.
2. Run the script to collect data, clean it, export it, and compare it.