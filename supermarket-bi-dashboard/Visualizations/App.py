import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.gridspec import GridSpec
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket BI Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Syne', sans-serif !important;
    }
    .main { background-color: #0f1117; }

    .kpi-card {
        background: linear-gradient(135deg, #1c1f2e, #252840);
        border: 1px solid #2e3250;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }
    .kpi-value {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #7dd3fc;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .section-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .badge-simple   { background:#1e3a5f; color:#7dd3fc; }
    .badge-inter    { background:#2d1b4e; color:#c084fc; }
    .badge-expert   { background:#1e3d2f; color:#6ee7b7; }

    div[data-testid="stSidebar"] {
        background: #0d0f1a;
        border-right: 1px solid #1e2235;
    }
    .chart-question {
        font-size: 0.85rem;
        color: #64748b;
        font-style: italic;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MATPLOTLIB DARK THEME
# ─────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0f1117",
    "axes.facecolor":    "#1a1d2e",
    "axes.edgecolor":    "#2e3250",
    "axes.labelcolor":   "#94a3b8",
    "axes.titlecolor":   "#e2e8f0",
    "text.color":        "#e2e8f0",
    "xtick.color":       "#64748b",
    "ytick.color":       "#64748b",
    "grid.color":        "#1e2235",
    "grid.linewidth":    0.6,
    "font.family":       "sans-serif",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

COLORS_MAIN   = ["#7dd3fc","#c084fc","#6ee7b7","#fbbf24","#f87171","#a78bfa"]
ACCENT        = "#7dd3fc"
ACCENT2       = "#c084fc"
ACCENT3       = "#6ee7b7"

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
DATA_PATH = Path(__file__).resolve().parent.parent / "Data" / "SuperMarket_Clean.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ─────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────
st.sidebar.markdown("## 🎛️ Filters")
city_opts    = df["city"].unique().tolist()
product_opts = df["product_line"].unique().tolist()
payment_opts = df["payment"].unique().tolist()

city_sel    = st.sidebar.multiselect("City",         city_opts,    default=city_opts)
product_sel = st.sidebar.multiselect("Product Line", product_opts, default=product_opts)
payment_sel = st.sidebar.multiselect("Payment",      payment_opts, default=payment_opts)
gender_sel  = st.sidebar.multiselect("Gender",       df["gender"].unique().tolist(), default=df["gender"].unique().tolist())

fdf = df[
    df["city"].isin(city_sel) &
    df["product_line"].isin(product_sel) &
    df["payment"].isin(payment_sel) &
    df["gender"].isin(gender_sel)
]

# ─────────────────────────────────────────
# HEADER + KPIs
# ─────────────────────────────────────────
st.markdown("# 🛒 Supermarket Business Intelligence")
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
kpis = [
    (c1, f"${fdf['sales'].sum():,.0f}",                   "Total Revenue"),
    (c2, f"${fdf['gross_income'].sum():,.0f}",             "Gross Profit"),
    (c3, f"{fdf['rating'].mean():.2f} ⭐",                 "Avg Customer Rating"),
    (c4, f"{len(fdf):,}",                                  "Total Transactions"),
]
for col, val, label in kpis:
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{val}</div>
        <div class="kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# ░░░  SECTION 1 – SIMPLE (5 charts)  ░░░
# ═══════════════════════════════════════════
st.markdown('<span class="section-badge badge-simple">● Simple</span>', unsafe_allow_html=True)
st.markdown("## 📊 Basic Business Questions")

# ── S1: Total Sales by City ──────────────────
col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="chart-question">❓ Ποια πόλη παράγει τα περισσότερα έσοδα;</p>', unsafe_allow_html=True)
    st.markdown("**Sales by City**")
    city_sales = fdf.groupby("city")["sales"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.barh(city_sales.index, city_sales.values,
                   color=COLORS_MAIN[:len(city_sales)], height=0.5)
    for bar, val in zip(bars, city_sales.values):
        ax.text(val + 200, bar.get_y() + bar.get_height()/2,
                f"${val:,.0f}", va="center", fontsize=8, color="#94a3b8")
    ax.set_xlabel("Total Sales ($)")
    ax.xaxis.grid(True, alpha=0.3)
    ax.yaxis.grid(False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── S2: Sales by Product Line ────────────────
with col2:
    st.markdown('<p class="chart-question">❓ Ποια κατηγορία προϊόντων πωλείται περισσότερο;</p>', unsafe_allow_html=True)
    st.markdown("**Revenue by Product Line**")
    prod_sales = fdf.groupby("product_line")["sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(range(len(prod_sales)), prod_sales.values,
           color=COLORS_MAIN[:len(prod_sales)], width=0.6)
    ax.set_xticks(range(len(prod_sales)))
    ax.set_xticklabels([x.replace(" And ", "\n& ") for x in prod_sales.index], fontsize=7.5)
    ax.set_ylabel("Sales ($)")
    ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

col3, col4 = st.columns(2)
# ── S3: Payment Methods ──────────────────────
with col3:
    st.markdown('<p class="chart-question">❓ Πώς πληρώνουν οι πελάτες μας;</p>', unsafe_allow_html=True)
    st.markdown("**Payment Method Distribution**")
    pay_counts = fdf["payment"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    wedges, texts, autotexts = ax.pie(
        pay_counts.values, labels=pay_counts.index,
        autopct="%1.1f%%", colors=COLORS_MAIN[:3],
        wedgeprops={"linewidth": 2, "edgecolor": "#0f1117"},
        startangle=140
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color("white")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── S4: Gender Distribution ──────────────────
with col4:
    st.markdown('<p class="chart-question">❓ Ποιο φύλο κάνει τις περισσότερες αγορές;</p>', unsafe_allow_html=True)
    st.markdown("**Transactions by Gender**")
    gender_counts = fdf["gender"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(gender_counts.index, gender_counts.values,
                  color=[ACCENT, ACCENT2], width=0.4)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 4,
                str(int(bar.get_height())), ha="center", fontsize=10, fontweight="bold")
    ax.set_ylabel("Number of Transactions")
    ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── S5: Customer Type ────────────────────────
col5, _ = st.columns([1, 1])
with col5:
    st.markdown('<p class="chart-question">❓ Έχουμε περισσότερους μέλη ή περιστασιακούς πελάτες;</p>', unsafe_allow_html=True)
    st.markdown("**Member vs Normal Customers**")
    ctype = fdf["customer_type"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.barh(ctype.index, ctype.values, color=[ACCENT3, "#fbbf24"], height=0.4)
    for i, v in enumerate(ctype.values):
        ax.text(v + 3, i, str(v), va="center", fontsize=10)
    ax.xaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ═══════════════════════════════════════════
# ░░░  SECTION 2 – INTERMEDIATE (5 charts)  ░░░
# ═══════════════════════════════════════════
st.markdown('<span class="section-badge badge-inter">● Intermediate</span>', unsafe_allow_html=True)
st.markdown("## 🔍 Deeper Business Insights")

col1, col2 = st.columns(2)

# ── I1: Monthly Revenue Trend ───────────────
with col1:
    st.markdown('<p class="chart-question">❓ Πώς εξελίχθηκαν τα έσοδά μας ανά μήνα;</p>', unsafe_allow_html=True)
    st.markdown("**Monthly Revenue Trend by City**")
    month_city = fdf.groupby(["month","city"])["sales"].sum().unstack(fill_value=0)
    month_names = {1:"Jan", 2:"Feb", 3:"Mar"}
    fig, ax = plt.subplots(figsize=(6, 3.8))
    for i, city in enumerate(month_city.columns):
        ax.plot(month_city.index, month_city[city], marker="o",
                label=city, color=COLORS_MAIN[i], linewidth=2.5, markersize=6)
    ax.set_xticks([1,2,3])
    ax.set_xticklabels(["January","February","March"])
    ax.set_ylabel("Sales ($)")
    ax.legend(framealpha=0)
    ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── I2: Avg Rating per Product Line ─────────
with col2:
    st.markdown('<p class="chart-question">❓ Ποια προϊόντα έχουν την υψηλότερη ικανοποίηση πελατών;</p>', unsafe_allow_html=True)
    st.markdown("**Avg Customer Rating by Product Line**")
    avg_rating = fdf.groupby("product_line")["rating"].mean().sort_values()
    colors_rating = [ACCENT3 if v >= avg_rating.mean() else "#475569" for v in avg_rating.values]
    fig, ax = plt.subplots(figsize=(6, 3.8))
    bars = ax.barh(avg_rating.index, avg_rating.values, color=colors_rating, height=0.55)
    ax.axvline(avg_rating.mean(), color="#f87171", linestyle="--", linewidth=1.2, label=f"Avg: {avg_rating.mean():.2f}")
    ax.set_xlim(6, 7.5)
    for bar, val in zip(bars, avg_rating.values):
        ax.text(val + 0.01, bar.get_y() + bar.get_height()/2,
                f"{val:.2f}", va="center", fontsize=8.5)
    ax.legend(framealpha=0, fontsize=8)
    ax.xaxis.grid(True, alpha=0.3)
    ax.yaxis.grid(False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

col3, col4 = st.columns(2)

# ── I3: Sales Heatmap (Day × Hour) ──────────
with col3:
    st.markdown('<p class="chart-question">❓ Ποιες ώρες και ημέρες έχουν τη μεγαλύτερη κίνηση;</p>', unsafe_allow_html=True)
    st.markdown("**Transaction Heatmap: Day × Hour**")
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    heat = fdf.groupby(["day_name","hour"]).size().unstack(fill_value=0)
    heat = heat.reindex([d for d in day_order if d in heat.index])
    fig, ax = plt.subplots(figsize=(6, 3.8))
    im = ax.imshow(heat.values, aspect="auto",
                   cmap="Blues", interpolation="nearest")
    ax.set_yticks(range(len(heat.index)))
    ax.set_yticklabels(heat.index, fontsize=8)
    ax.set_xticks(range(len(heat.columns)))
    ax.set_xticklabels(heat.columns, fontsize=7, rotation=45)
    ax.set_xlabel("Hour of Day")
    plt.colorbar(im, ax=ax, label="Transactions")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── I4: Gross Income per Product per City ───
with col4:
    st.markdown('<p class="chart-question">❓ Ποια προϊόντα αποδίδουν καλύτερα σε κάθε πόλη;</p>', unsafe_allow_html=True)
    st.markdown("**Gross Income: Product Line × City**")
    gi = fdf.groupby(["product_line","city"])["gross_income"].sum().unstack(fill_value=0)
    x = np.arange(len(gi.index))
    width = 0.28
    fig, ax = plt.subplots(figsize=(6, 3.8))
    for i, city in enumerate(gi.columns):
        ax.bar(x + i*width, gi[city], width, label=city, color=COLORS_MAIN[i])
    ax.set_xticks(x + width)
    ax.set_xticklabels([p.replace(" And ", "\n& ") for p in gi.index], fontsize=7)
    ax.set_ylabel("Gross Income ($)")
    ax.legend(framealpha=0, fontsize=8)
    ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── I5: Quantity vs Sales Scatter ────────────
col5, _ = st.columns([1,1])
with col5:
    st.markdown('<p class="chart-question">❓ Υπάρχει συσχέτιση μεταξύ ποσότητας αγοράς και αξίας;</p>', unsafe_allow_html=True)
    st.markdown("**Quantity Purchased vs Total Sale Value**")
    fig, ax = plt.subplots(figsize=(6, 3.8))
    for i, pl in enumerate(fdf["product_line"].unique()):
        sub = fdf[fdf["product_line"] == pl]
        ax.scatter(sub["quantity"], sub["sales"], alpha=0.45, s=20,
                   color=COLORS_MAIN[i], label=pl)
    # trend line
    z = np.polyfit(fdf["quantity"], fdf["sales"], 1)
    p = np.poly1d(z)
    xs = np.linspace(fdf["quantity"].min(), fdf["quantity"].max(), 100)
    ax.plot(xs, p(xs), "--", color="#f87171", linewidth=1.5, label="Trend")
    ax.set_xlabel("Quantity")
    ax.set_ylabel("Sales ($)")
    ax.legend(framealpha=0, fontsize=7, ncol=2)
    ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ═══════════════════════════════════════════
# ░░░  SECTION 3 – EXPERT (5 charts)  ░░░
# ═══════════════════════════════════════════
st.markdown('<span class="section-badge badge-expert">● Expert</span>', unsafe_allow_html=True)
st.markdown("## 🧠 Advanced Analytics")

col1, col2 = st.columns(2)

# ── E1: Revenue Contribution (Waterfall) ─────
with col1:
    st.markdown('<p class="chart-question">❓ Πώς συνεισφέρει κάθε κατηγορία στα συνολικά έσοδα (waterfall);</p>', unsafe_allow_html=True)
    st.markdown("**Cumulative Revenue Contribution (Waterfall)**")
    prod_rev = fdf.groupby("product_line")["sales"].sum().sort_values(ascending=False)
    cumulative = prod_rev.cumsum()
    running_start = pd.Series([0] + list(cumulative[:-1].values), index=prod_rev.index)
    fig, ax = plt.subplots(figsize=(6, 4))
    bar_colors = [ACCENT if i % 2 == 0 else ACCENT2 for i in range(len(prod_rev))]
    ax.bar(range(len(prod_rev)), prod_rev.values, bottom=running_start.values,
           color=bar_colors, width=0.6, linewidth=0)
    ax.bar(len(prod_rev), cumulative.iloc[-1], color=ACCENT3, width=0.6, label="Total")
    ax.set_xticks(list(range(len(prod_rev))) + [len(prod_rev)])
    ax.set_xticklabels(
        [p.replace(" And ", "\n& ") for p in prod_rev.index] + ["TOTAL"],
        fontsize=7, rotation=15
    )
    ax.set_ylabel("Sales ($)")
    for i, (val, start) in enumerate(zip(prod_rev.values, running_start.values)):
        ax.text(i, start + val/2, f"${val:,.0f}", ha="center", fontsize=7, color="white", fontweight="bold")
    ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── E2: Rating Distribution per Product ─────
with col2:
    st.markdown('<p class="chart-question">❓ Πώς κατανέμεται η ικανοποίηση πελατών ανά κατηγορία; (violin)</p>', unsafe_allow_html=True)
    st.markdown("**Rating Distribution by Product Line (Violin)**")
    groups = [fdf[fdf["product_line"] == pl]["rating"].values for pl in product_opts]
    labels = [pl.replace(" And ", "\n& ") for pl in product_opts]
    fig, ax = plt.subplots(figsize=(6, 4))
    parts = ax.violinplot(groups, positions=range(len(groups)), showmedians=True,
                          showextrema=True)
    for pc, col in zip(parts["bodies"], COLORS_MAIN):
        pc.set_facecolor(col)
        pc.set_alpha(0.65)
    parts["cmedians"].set_color("#f87171")
    parts["cmins"].set_color("#475569")
    parts["cmaxes"].set_color("#475569")
    parts["cbars"].set_color("#475569")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("Rating")
    ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

col3, col4 = st.columns(2)

# ── E3: RFM-style Segment Bar (Frequency × Value) ──
with col3:
    st.markdown('<p class="chart-question">❓ Ποια συνδυαστική στρατηγική πόλης/τύπου πελάτη αποδίδει καλύτερα;</p>', unsafe_allow_html=True)
    st.markdown("**Avg Sales: City × Customer Type (Grouped)**")
    seg = fdf.groupby(["city","customer_type"])["sales"].mean().unstack(fill_value=0)
    x = np.arange(len(seg.index))
    width = 0.35
    fig, ax = plt.subplots(figsize=(6, 4))
    for i, ct in enumerate(seg.columns):
        bars = ax.bar(x + i*width - width/2, seg[ct], width, label=ct,
                      color=COLORS_MAIN[i], alpha=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(seg.index)
    ax.set_ylabel("Avg Sale Value ($)")
    ax.legend(framealpha=0)
    ax.yaxis.grid(True, alpha=0.3)
    # annotation: best performer
    best_city = seg.mean(axis=1).idxmax()
    best_idx  = list(seg.index).index(best_city)
    ax.annotate("🏆 Best", xy=(best_idx, seg.loc[best_city].max()),
                xytext=(best_idx + 0.5, seg.loc[best_city].max() + 5),
                arrowprops=dict(arrowstyle="->", color="#fbbf24"),
                color="#fbbf24", fontsize=9)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── E4: Profit Margin % per Product Boxplot ─
with col4:
    st.markdown('<p class="chart-question">❓ Ποια κατηγορία έχει σταθερά υψηλά gross margins;</p>', unsafe_allow_html=True)
    st.markdown("**Gross Margin Spread per Product Line**")
    # gross_income / sales * 100 per transaction
    fdf = fdf.copy()
    fdf["margin_pct"] = fdf["gross_income"] / fdf["sales"] * 100
    groups_m = [fdf[fdf["product_line"] == pl]["margin_pct"].values for pl in product_opts]
    fig, ax = plt.subplots(figsize=(6, 4))
    bp = ax.boxplot(groups_m, patch_artist=True, medianprops={"color": "#f87171", "linewidth": 2},
                    whiskerprops={"color": "#475569"},
                    capprops={"color": "#475569"},
                    flierprops={"marker": "o", "markersize": 3, "color": "#475569"})
    for patch, col in zip(bp["boxes"], COLORS_MAIN):
        patch.set_facecolor(col)
        patch.set_alpha(0.7)
    ax.set_xticklabels([p.replace(" And ", "\n& ") for p in product_opts], fontsize=7)
    ax.set_ylabel("Gross Margin %")
    ax.yaxis.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── E5: Weekly Sales Trend (Area) ────────────
col5, _ = st.columns([1,1])
with col5:
    st.markdown('<p class="chart-question">❓ Ποιες εβδομάδες είχαν αιχμή; Υπάρχει εβδομαδιαία τάση ανά πόλη;</p>', unsafe_allow_html=True)
    st.markdown("**Weekly Revenue Trend per City (Stacked Area)**")
    weekly = fdf.groupby(["week","city"])["sales"].sum().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.stackplot(weekly.index, [weekly[c] for c in weekly.columns],
                 labels=weekly.columns,
                 colors=COLORS_MAIN[:len(weekly.columns)], alpha=0.75)
    ax.set_xlabel("Week of Year")
    ax.set_ylabel("Total Sales ($)")
    ax.legend(loc="upper left", framealpha=0, fontsize=9)
    ax.yaxis.grid(True, alpha=0.3)
    # mark peak week
    peak_week = weekly.sum(axis=1).idxmax()
    peak_val  = weekly.sum(axis=1).max()
    ax.axvline(peak_week, color="#fbbf24", linestyle="--", linewidth=1.4, label=f"Peak week {peak_week}")
    ax.text(peak_week + 0.2, peak_val * 0.8, f"Peak\nWk {peak_week}", color="#fbbf24", fontsize=8)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#475569;font-size:0.78rem;'>Supermarket BI Dashboard · Data: 1,000 transactions · Jan–Mar 2019</div>",
    unsafe_allow_html=True
)
