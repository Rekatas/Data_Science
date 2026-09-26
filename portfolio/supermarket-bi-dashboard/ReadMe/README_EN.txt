# Supermarket Sales Business Intelligence Dashboard

## Project Overview

This project is an end-to-end Business Intelligence system for analyzing supermarket sales data.

The goal is to transform raw retail transaction data into meaningful business insights through data cleaning, processing, and visualization.

The system analyzes:
- Sales performance across cities and product categories
- Customer behavior patterns
- Payment method preferences
- Time-based purchasing trends
- Profitability and customer satisfaction

---

## Dataset

The project uses the Supermarket Sales Dataset, which contains 1,000 retail transactions with the following key features:

- Invoice ID
- Branch and City
- Customer Type and Gender
- Product Line
- Unit Price and Quantity
- Total Sales and Cost of Goods Sold
- Date and Time
- Payment Method
- Customer Rating

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Streamlit
- SQL (PostgreSQL-compatible structure)
- Data Cleaning and Feature Engineering

---

## Data Processing Pipeline

### Data Cleaning
- Standardization of column names
- Date and time conversion to proper formats
- Removal of duplicate records
- Handling of missing values
- Validation of numeric fields

### Feature Engineering
New analytical features were created:
- Hour of transaction
- Day of the week
- Month
- Week number
- Profit margin percentage

---

## Dashboard

The dashboard is built using Streamlit and provides interactive data analysis capabilities.

It includes:
- Interactive filters (City, Product Line, Gender, Payment Method)
- KPI indicators (Revenue, Gross Profit, Rating, Transactions)
- 15+ business analytics visualizations
- Dark theme interface
- Embedded data labels inside charts
- Business-question-driven structure

---

## Business Insights

The analysis reveals the following insights:

- Sales distribution varies significantly across product categories
- Customer behavior is influenced by city and time of purchase
- Clear preferences exist in payment methods
- Customer satisfaction remains relatively stable across segments
- Certain cities consistently outperform others in revenue generation

---

## Analytical Capabilities

This project demonstrates:
- Exploratory Data Analysis (EDA)
- Customer behavior analysis
- Time series trend analysis
- Profitability analysis
- Correlation and distribution analysis
- Business Intelligence dashboard development