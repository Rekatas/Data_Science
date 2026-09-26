# Mobile Complaints Dashboard (EETT 2022–2024)

## Project Overview

This project analyzes mobile telecommunications complaints in Greece using data published by the Hellenic Telecommunications and Post Commission (EETT).

The dashboard provides an interactive view of complaint handling performance across mobile providers, complaint categories, and network technologies for the period 2022–2024.

The application was developed using Python, Streamlit, Plotly, and Pandas.

---

## Objectives

* Analyze complaint resolution performance across providers.
* Compare service quality indicators over time.
* Identify trends and performance changes.
* Detect unusual periods and outliers.
* Explore complaint categories and network-related differences.
* Create an interactive business intelligence dashboard.

---

## Dataset

The dataset contains complaint performance indicators reported by mobile operators in Greece.

Main variables include:

* Provider
* Year
* Semester
* Complaint Category
* Resolution Rate within 10 Days (%)
* Median Resolution Time (Days)
* 95th Percentile Resolution Time (P95)
* Network Type (2G/3G, 4G/5G)

---

## Project Structure

Telecom/

├── App.py

├── Cleaning.py

├── Mobile.csv

├── Mobile_clean.csv

└── README.md

### Files

**Mobile.csv**

* Original dataset.

**Cleaning.py**

* Data cleaning and preprocessing pipeline.

**Mobile_clean.csv**

* Cleaned dataset used by the dashboard.

**App.py**

* Main Streamlit dashboard application.

---

## Dashboard Features

### 1. Overview

* Provider comparison
* Category distribution
* Key Performance Indicators (KPIs)

### 2. Trends Analysis

* Performance evolution over time
* Provider trend comparison
* Improvement vs deterioration analysis

### 3. Ranking System

* Composite Performance Score
* Provider ranking
* Heatmap analysis

### 4. Category Analysis

* Difficult vs easy complaint categories
* Category improvement tracking
* Bubble chart analysis

### 5. Outlier Detection

* P95 spike detection
* Z-score analysis
* Consistency scoring

### 6. Correlation Analysis

* Correlation matrix
* Scatter plots
* Resolution performance relationships

### 7. Network Type Analysis

* 2G/3G vs 4G/5G comparison
* Network performance differences
* Distribution analysis

---

## Technologies Used

* Python
* Pandas
* NumPy
* Streamlit
* Plotly

---

## Key Analytics Techniques

* Data Cleaning
* Feature Engineering
* KPI Design
* Time Series Analysis
* Composite Scoring
* Z-Score Outlier Detection
* Correlation Analysis
* Interactive Data Visualization

---

## How to Run

Install dependencies:

pip install streamlit pandas numpy plotly

Run the application:

streamlit run App.py

---

## Author

Giorgos Rekatas

Data Analytics & Business Intelligence Portfolio Project
