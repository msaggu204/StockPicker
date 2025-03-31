# StockPicker

Stock Picker is a Python-based financial analysis tool designed to evaluate the performance and growth potential of publicly traded companies. It leverages real-time data from Yahoo Finance via the yfinance library to calculate and compare key financial metrics.

🔍 Features
	•	Retrieves financial metrics like:
	•	EPS (Earnings Per Share)
	•	P/E Ratio
	•	Return on Equity (ROE)
	•	Debt to Equity Ratio
	•	Free Cash Flow
	•	Analyzes 3-year growth trends for:
	•	Revenue
	•	Net Income
	•	EPS
	•	Outputs clean, readable summaries using pandas DataFrames
	•	Includes robust error handling and fallback values for missing data

🧠 Use Case

This tool is useful for:
	•	Investors looking to compare financial health of top companies
	•	Students and developers learning financial data analysis in Python
	•	Quick prototyping or exploration before deeper investment research

🛠 Tech Stack
	•	Python
	•	pandas
	•	yfinance
	•	Object-Oriented Programming
	•	CLI interface (optional future extension)

 🚀 Getting Started
	1.	Clone the repo

      git clone https://github.com/msaggu204/StockPicker.git
      cd StockPicker

	2.	Install dependencies

      pip install yfinance pandas

	3.	Run the script

      python stockpicker.py


  📂 Output Example
  
  The script outputs two DataFrames:
  	•	One for current financial ratios
  	•	One for 3-year growth metrics
