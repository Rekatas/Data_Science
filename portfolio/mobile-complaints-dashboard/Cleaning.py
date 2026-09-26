"""
=============================================================
  Mobile Complaints Dataset — Data Cleaning Script
  Πηγή: ΕΕΤΤ (Εθνική Επιτροπή Τηλεπικοινωνιών & Ταχυδρομείων)
  Δεδομένα: Παράπονα κινητής τηλεφωνίας ανά πάροχο, 2022–2024
=============================================================
"""

import pandas as pd
import numpy as np

# ── 1. ΦΟΡΤΩΣΗ ──────────────────────────────────────────────
df = pd.read_csv("Mobile.csv")
print(f"[INFO] Αρχικό dataset: {df.shape[0]} γραμμές × {df.shape[1]} στήλες")


# ── 2. ΜΕΤΟΝΟΜΑΣΙΑ ΣΤΗΛΩΝ ───────────────────────────────────
# Κάνουμε τα ονόματα πιο περιγραφικά και εύχρηστα
df.rename(columns={
    "year_semester"             : "period",            # Π.χ. "2022 A" = 1ο εξάμηνο 2022
    "provider"                  : "provider",
    "complaint_category"        : "category",
    "network_type"              : "network_type",
    "solved_10days_perc"        : "resolved_in_10d_pct",
    "resolution_time_50th_pcntl": "resolution_median_days",
    "resolution_time_95th_pcntl": "resolution_p95_days",
}, inplace=True)


# ── 3. ΚΑΘΑΡΙΣΜΟΣ ΣΤΗΛΗΣ: period ────────────────────────────
# Χωρίζουμε το "2022 A" σε δύο ξεχωριστές στήλες: year (int) και semester (str)
# Αυτό κάνει πολύ πιο εύκολη τη χρονολογική ανάλυση (sorting, groupby, plots)
df[["year", "semester"]] = df["period"].str.split(" ", expand=True)
df["year"] = df["year"].astype(int)

# Δημιουργούμε επίσης μια αριθμητική στήλη για σωστή χρονολογική ταξινόμηση
# A = 1ο εξάμηνο (Ιαν–Ιουν), B = 2ο εξάμηνο (Ιουλ–Δεκ)
df["period_order"] = df["year"] * 10 + df["semester"].map({"A": 1, "B": 2})

print(f"[INFO] Στήλη 'period' διαχωρίστηκε σε 'year' και 'semester'.")


# ── 4. ΚΑΘΑΡΙΣΜΟΣ ΣΤΗΛΗΣ: network_type ─────────────────────
# Τιμές: 0, 1, 2 — αλλά τι σημαίνουν;
# Βάσει του dataset (ΕΕΤΤ): 0 = κλειστό δίκτυο/MVNO, 1 = 2G/3G, 2 = 4G/5G
# Ή εναλλακτικά: 0 = δεν αναφέρεται, 1 = φωνή, 2 = δεδομένα
# Κρατάμε την αριθμητική τιμή (δεν την αλλάζουμε) αλλά την κωδικοποιούμε και σε label
# ΣΗΜΕΙΩΣΗ: Αν γνωρίζεις τον ακριβή ορισμό από την ΕΕΤΤ, άλλαξε το mapping παρακάτω.
network_map = {0: "unspecified", 1: "voice_2G3G", 2: "data_4G5G"}
df["network_label"] = df["network_type"].map(network_map)

print(f"[INFO] Στήλη 'network_label' δημιουργήθηκε με βάση το network_type mapping.")


# ── 5. ΚΑΘΑΡΙΣΜΟΣ ΣΤΗΛΗΣ: category (τυπογραφικά λάθη) ──────
# Εντοπίσαμε δύο παραλλαγές της ίδιας κατηγορίας με διαφορετικό τονισμό:
#   "καρτοκινητή (αδυναμία ανανέωσης/δυσδιακριτες καρτες)"  ← χωρίς τόνους στο τέλος
#   "καρτοκινητή (αδυναμία ανανέωσης/δυσδιάκριτες κάρτες)"  ← σωστό
# Ενοποιούμε στη σωστή εκδοχή.
df["category"] = df["category"].str.replace(
    "καρτοκινητή (αδυναμία ανανέωσης/δυσδιακριτες καρτες)",
    "καρτοκινητή (αδυναμία ανανέωσης/δυσδιάκριτες κάρτες)",
    regex=False
)

before = df["category"].nunique()
print(f"[INFO] Τυπογραφικό λάθος στο category διορθώθηκε. Μοναδικές κατηγορίες: {before}")


# ── 6. ΑΝΤΙΜΕΤΩΠΙΣΗ NULL ΤΙΜΩΝ ──────────────────────────────
# Εντοπίσαμε 3 γραμμές με NaN στα Vodafone 2022A — πιθανόν αδύνατη αναφορά τότε.
# Επιλογή: ΔΕΝ τις διαγράφουμε — κρατάμε τις γραμμές αλλά τις σημειώνουμε.
# Αυτό μας επιτρέπει να έχουμε πλήρες ιστορικό και να φιλτράρουμε αργότερα αν χρειαστεί.
null_rows = df[df[["resolved_in_10d_pct", "resolution_median_days", "resolution_p95_days"]].isnull().any(axis=1)]
print(f"[INFO] Γραμμές με NaN: {len(null_rows)} (Vodafone 2022A — κρατιούνται με flag)")

df["has_missing_metrics"] = df[["resolved_in_10d_pct", "resolution_median_days", "resolution_p95_days"]].isnull().any(axis=1)


# ── 7. ΕΛΕΓΧΟΣ ΛΟΓΙΚΗΣ ΣΥΝΕΠΕΙΑΣ ───────────────────────────
# Ο 95ος εκατοστιαίος χρόνος επίλυσης δεν μπορεί να είναι μικρότερος από τη διάμεσο
inconsistent = df[
    (df["resolution_p95_days"] < df["resolution_median_days"]) &
    (~df["has_missing_metrics"])
]
print(f"[INFO] Γραμμές με p95 < median (λογικά ύποπτες): {len(inconsistent)}")
# → Αν βρεθούν, τις εμφανίζουμε για manual review
if len(inconsistent) > 0:
    print(inconsistent[["period", "provider", "category", "resolution_median_days", "resolution_p95_days"]])


# ── 8. ΕΛΕΓΧΟΣ ΕΓΚΥΡΟΤΗΤΑΣ ΤΙΜΩΝ ───────────────────────────
# Το ποσοστό επίλυσης σε 10 μέρες πρέπει να είναι μεταξύ 0 και 100
invalid_pct = df[
    (df["resolved_in_10d_pct"] < 0) | (df["resolved_in_10d_pct"] > 100)
]
print(f"[INFO] Γραμμές με resolved_in_10d_pct εκτός [0,100]: {len(invalid_pct)}")


# ── 9. ΤΕΛΙΚΗ ΕΠΙΛΟΓΗ ΚΑΙ ΤΑΞΙΝΟΜΗΣΗ ΣΤΗΛΩΝ ────────────────
# Ταξινομούμε χρονολογικά και επιλέγουμε σαφή σειρά στηλών
df_clean = df.sort_values(["period_order", "provider", "category"]).reset_index(drop=True)

final_columns = [
    "period", "year", "semester", "period_order",
    "provider",
    "category",
    "network_type", "network_label",
    "resolved_in_10d_pct",
    "resolution_median_days",
    "resolution_p95_days",
    "has_missing_metrics"
]
df_clean = df_clean[final_columns]


# ── 10. ΑΠΟΘΗΚΕΥΣΗ ──────────────────────────────────────────
output_path = "Mobile_clean.csv"
df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")  # utf-8-sig για σωστή εμφάνιση ελληνικών στο Excel

print(f"\n[DONE] Clean dataset αποθηκεύτηκε: '{output_path}'")
print(f"       Τελικό σχήμα: {df_clean.shape[0]} γραμμές × {df_clean.shape[1]} στήλες")
print(f"\n── Προεπισκόπηση ──")
print(df_clean.head(5).to_string())
print(f"\n── Στατιστικά ──")
print(df_clean.describe().to_string())
