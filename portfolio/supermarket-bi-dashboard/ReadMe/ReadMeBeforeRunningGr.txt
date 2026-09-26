▶️ Πώς τρέχει το project
1. Εγκατάσταση βιβλιοθηκών

Άνοιξε terminal / cmd και τρέξε:

pip install streamlit pandas matplotlib numpy

2. Δομή φακέλων
Το project πρέπει να είναι έτσι:

Supermarket/
│
├── Data/
│   └── SuperMarket_Clean.csv
│
├── Visualizations/
│   └── App.py
│
└── exe.py

3. Εκκίνηση εφαρμογής

Προτεινόμενος τρόπος (εύκολος)
python exe.py

Εναλλακτικά (χειροκίνητα)
streamlit run Visualizations/App.py