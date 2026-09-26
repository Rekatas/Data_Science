▶️ Run the project
1. Install required libraries
pip install streamlit pandas matplotlib numpy

2. Project structure

Make sure your files are like this:

Supermarket/
│
├── Data/
│   └── SuperMarket_Clean.csv
│
├── Visualizations/
│   └── App.py
│
└── exe.py

3. Start the dashboard

Option A (Recommended – one click)
python exe.py
Option B (manual)
streamlit run Visualizations/App.py