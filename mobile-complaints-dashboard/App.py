"""
========================================================
  Mobile Complaints Dashboard — ΕΕΤΤ 2022–2024
  Ανάλυση παραπόνων κινητής τηλεφωνίας ανά πάροχο
========================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── ΣΕΛΙΔΑ ΡΥΘΜΙΣΕΙΣ ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mobile Complaints | ΕΕΤΤ 2022–2024",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── ΧΡΩΜΑΤΑ ΠΑΡΟΧΩΝ ──────────────────────────────────────────────────────────
PROVIDER_COLORS = {
    "Cosmote" : "#00A650",
    "OTE"     : "#005CA9",
    "Nova"    : "#FF6B00",
    "Vodafone": "#E60000",
    "Wind"    : "#7B2D8B",
}

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #262b3d);
        border: 1px solid #2e3347;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 5px 0;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #e0e6ff; }
    .metric-label { font-size: 0.85rem; color: #8892b0; margin-top: 4px; }
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ccd6f6;
        border-left: 4px solid #64ffda;
        padding-left: 12px;
        margin: 30px 0 16px 0;
    }
    .insight-box {
        background: #1a1f2e;
        border: 1px solid #64ffda33;
        border-radius: 8px;
        padding: 14px 18px;
        color: #8892b0;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    .stTabs [data-baseweb="tab"] { font-size: 0.95rem; font-weight: 600; }
    div[data-testid="stSidebarContent"] { background-color: #131720; }
</style>
""", unsafe_allow_html=True)


# ── ΦΟΡΤΩΣΗ & CACHE ΔΕΔΟΜΕΝΩΝ ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Mobile_clean.csv")
    return df

df = load_data()

# Dataset χωρίς NaN για τις αναλύσεις που χρειάζονται αριθμούς
df_valid = df[~df["has_missing_metrics"]].copy()

# Δημιουργία period_label για όλες τις αναλύσεις
df_valid["period_label"] = df_valid["year"].astype(str) + " " + df_valid["semester"]


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📱 Mobile Complaints")
    st.markdown("**ΕΕΤΤ — 2022 to 2024**")
    st.markdown("---")

    st.markdown("### 🔎 Φίλτρα")

    selected_providers = st.multiselect(
        "Πάροχος",
        options=sorted(df["provider"].unique()),
        default=sorted(df["provider"].unique()),
    )

    selected_years = st.multiselect(
        "Έτος",
        options=sorted(df["year"].unique()),
        default=sorted(df["year"].unique()),
    )

    selected_semesters = st.multiselect(
        "Εξάμηνο",
        options=["A", "B"],
        default=["A", "B"],
        format_func=lambda x: "1ο Εξάμηνο (Α)" if x == "A" else "2ο Εξάμηνο (Β)",
    )

    st.markdown("---")
    st.markdown("### 📊 Μετρική εστίασης")
    metric_choice = st.selectbox(
        "Κύρια μετρική",
        options=["resolved_in_10d_pct", "resolution_median_days", "resolution_p95_days"],
        format_func=lambda x: {
            "resolved_in_10d_pct"      : "✅ % Επίλυση σε 10 μέρες",
            "resolution_median_days"   : "⏱️ Διάμεσος χρόνος (μέρες)",
            "resolution_p95_days"      : "📈 P95 χρόνος (μέρες)",
        }[x],
    )

    st.markdown("---")
    st.caption("Πηγή δεδομένων: ΕΕΤΤ")
    st.caption("Περίοδος: 2022–2024")

# Εφαρμογή φίλτρων
mask = (
    df_valid["provider"].isin(selected_providers) &
    df_valid["year"].isin(selected_years) &
    df_valid["semester"].isin(selected_semesters)
)
df_f = df_valid[mask].copy()


# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("# 📱 Mobile Complaints Dashboard")
st.markdown("#### Ανάλυση παραπόνων κινητής τηλεφωνίας — ΕΕΤΤ 2022–2024")
st.markdown("---")

# ── KPI CARDS ────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

cards = [
    (k1, f"{len(df_f):,}", "Εγγραφές"),
    (k2, f"{df_f['provider'].nunique()}", "Πάροχοι"),
    (k3, f"{df_f['category'].nunique()}", "Κατηγορίες"),
    (k4, f"{df_f['resolved_in_10d_pct'].mean():.1f}%", "Μ.Ο. Επίλυση 10ημ."),
    (k5, f"{df_f['resolution_p95_days'].mean():.1f}", "Μ.Ο. P95 (μέρες)"),
]
for col, val, label in cards:
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{val}</div>
        <div class="metric-label">{label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Επισκόπηση",
    "📈 Τάσεις",
    "🏆 Ranking",
    "📂 Κατηγορίες",
    "⚡ Outliers",
    "🔬 Συσχετίσεις",
    "🌐 Network Type",
])


# ══════════════════════════════════════════════════════
# TAB 1 — ΕΠΙΣΚΟΠΗΣΗ
# ══════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Κατανομή παραπόνων ανά πάροχο</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Πλήθος εγγραφών ανά πάροχο (proxy για όγκο παραπόνων)
        count_by_provider = df_f.groupby("provider").size().reset_index(name="count").sort_values("count", ascending=True)
        fig = px.bar(
            count_by_provider, x="count", y="provider", orientation="h",
            color="provider", color_discrete_map=PROVIDER_COLORS,
            title="Εγγραφές ανά πάροχο",
            labels={"count": "Αριθμός εγγραφών", "provider": ""},
        )
        fig.update_layout(showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                          font_color="#ccd6f6", title_font_size=14)
        fig.update_xaxes(gridcolor="#1e2130")
        fig.update_yaxes(gridcolor="#1e2130")
        st.plotly_chart(fig, width='stretch')

    with col2:
        # Μέσος όρος κύριας μετρικής ανά πάροχο
        metric_labels = {
            "resolved_in_10d_pct"   : "% Επίλυση σε 10 μέρες",
            "resolution_median_days": "Διάμεσος χρόνος (μέρες)",
            "resolution_p95_days"   : "P95 χρόνος (μέρες)",
        }
        avg_by_provider = df_f.groupby("provider")[metric_choice].mean().reset_index().sort_values(metric_choice, ascending=True)
        fig2 = px.bar(
            avg_by_provider, x=metric_choice, y="provider", orientation="h",
            color="provider", color_discrete_map=PROVIDER_COLORS,
            title=f"Μ.Ο. {metric_labels[metric_choice]} ανά πάροχο",
            labels={metric_choice: metric_labels[metric_choice], "provider": ""},
        )
        fig2.update_layout(showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                           font_color="#ccd6f6", title_font_size=14)
        fig2.update_xaxes(gridcolor="#1e2130")
        fig2.update_yaxes(gridcolor="#1e2130")
        st.plotly_chart(fig2, width='stretch')

    st.markdown('<div class="section-title">Κατανομή κατηγοριών παραπόνων</div>', unsafe_allow_html=True)
    cat_counts = df_f.groupby("category").size().reset_index(name="count").sort_values("count", ascending=False)
    fig3 = px.bar(
        cat_counts, x="category", y="count",
        color="count", color_continuous_scale="teal",
        title="Εγγραφές ανά κατηγορία παραπόνου",
        labels={"count": "Αριθμός εγγραφών", "category": "Κατηγορία"},
    )
    fig3.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                       font_color="#ccd6f6", xaxis_tickangle=-35, coloraxis_showscale=False)
    fig3.update_xaxes(gridcolor="#1e2130")
    fig3.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig3, width='stretch')

    st.markdown('<div class="section-title">Στατιστικά ανά πάροχο</div>', unsafe_allow_html=True)
    summary = df_f.groupby("provider").agg(
        Εγγραφές=("provider", "count"),
        Μέση_επίλυση_10ημ=("resolved_in_10d_pct", "mean"),
        Διάμεσος_χρόνος=("resolution_median_days", "mean"),
        P95_χρόνος=("resolution_p95_days", "mean"),
    ).round(2).reset_index()
    summary.columns = ["Πάροχος", "Εγγραφές", "Μέση Επίλυση 10ημ. (%)", "Μέσος Διάμεσος (μέρες)", "Μέσος P95 (μέρες)"]
    st.dataframe(summary, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════
# TAB 2 — ΤΑΣΕΙΣ
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Εξέλιξη απόδοσης 2022–2024</div>', unsafe_allow_html=True)

    trend_data = df_f.groupby(["period_label", "period_order", "provider"])[metric_choice].mean().reset_index()
    trend_data = trend_data.sort_values("period_order")

    fig_trend = px.line(
        trend_data, x="period_label", y=metric_choice,
        color="provider", color_discrete_map=PROVIDER_COLORS,
        markers=True,
        title=f"Τάση: {metric_labels[metric_choice]} ανά πάροχο",
        labels={metric_choice: metric_labels[metric_choice], "period_label": "Περίοδος", "provider": "Πάροχος"},
    )
    fig_trend.update_traces(line_width=2.5, marker_size=8)
    fig_trend.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                            font_color="#ccd6f6", height=420)
    fig_trend.update_xaxes(gridcolor="#1e2130")
    fig_trend.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_trend, width='stretch')

    st.markdown('<div class="section-title">Σύγκριση και των τριών μετρικών</div>', unsafe_allow_html=True)

    selected_p = st.selectbox("Επίλεξε πάροχο για λεπτομερή ανάλυση:", sorted(df_f["provider"].unique()))

    df_prov = df_f[df_f["provider"] == selected_p].groupby(["period_label", "period_order"]).agg(
        resolved_in_10d_pct=("resolved_in_10d_pct", "mean"),
        resolution_median_days=("resolution_median_days", "mean"),
        resolution_p95_days=("resolution_p95_days", "mean"),
    ).reset_index().sort_values("period_order")

    fig_multi = make_subplots(rows=3, cols=1, shared_xaxes=True,
                               subplot_titles=["% Επίλυση σε 10 μέρες", "Διάμεσος χρόνος (μέρες)", "P95 χρόνος (μέρες)"],
                               vertical_spacing=0.08)
    color = PROVIDER_COLORS.get(selected_p, "#64ffda")

    for i, col_name in enumerate(["resolved_in_10d_pct", "resolution_median_days", "resolution_p95_days"], 1):
        fig_multi.add_trace(go.Scatter(
            x=df_prov["period_label"], y=df_prov[col_name],
            mode="lines+markers", line=dict(color=color, width=2.5),
            marker=dict(size=8), showlegend=False,
        ), row=i, col=1)

    fig_multi.update_layout(height=500, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                             font_color="#ccd6f6", title_text=f"Εξέλιξη όλων των μετρικών — {selected_p}")
    for i in range(1, 4):
        fig_multi.update_xaxes(gridcolor="#1e2130", row=i, col=1)
        fig_multi.update_yaxes(gridcolor="#1e2130", row=i, col=1)
    st.plotly_chart(fig_multi, width='stretch')

    # ⭐ Βελτίωση vs Χειροτέρευση
    st.markdown('<div class="section-title">⭐ Ποιος βελτιώθηκε περισσότερο;</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Σύγκριση πρώτης vs τελευταίας περιόδου για κάθε πάροχο. Θετικές τιμές στο resolved_in_10d_pct = βελτίωση.</div>', unsafe_allow_html=True)

    first_last = df_f.groupby(["provider", "period_order"])[metric_choice].mean().reset_index()
    first_period = first_last.groupby("provider")["period_order"].min().reset_index().rename(columns={"period_order": "first_order"})
    last_period  = first_last.groupby("provider")["period_order"].max().reset_index().rename(columns={"period_order": "last_order"})

    first_vals = first_last.merge(first_period, left_on=["provider", "period_order"], right_on=["provider", "first_order"])[["provider", metric_choice]].rename(columns={metric_choice: "first_val"})
    last_vals  = first_last.merge(last_period,  left_on=["provider", "period_order"], right_on=["provider", "last_order"])[["provider", metric_choice]].rename(columns={metric_choice: "last_val"})

    change_df = first_vals.merge(last_vals, on="provider")
    change_df["change"] = change_df["last_val"] - change_df["first_val"]
    change_df["direction"] = change_df["change"].apply(lambda x: "Βελτίωση ✅" if x > 0 else "Χειροτέρευση ❌")

    # Για resolved_in_10d_pct, θετικό = βελτίωση. Για χρόνους, αρνητικό = βελτίωση
    if metric_choice != "resolved_in_10d_pct":
        change_df["direction"] = change_df["change"].apply(lambda x: "Βελτίωση ✅" if x < 0 else "Χειροτέρευση ❌")

    fig_change = px.bar(
        change_df.sort_values("change"), x="change", y="provider",
        orientation="h", color="direction",
        color_discrete_map={"Βελτίωση ✅": "#64ffda", "Χειροτέρευση ❌": "#ff6b6b"},
        title=f"Μεταβολή {metric_labels[metric_choice]}: πρώτη → τελευταία περίοδος",
        labels={"change": "Μεταβολή", "provider": ""},
    )
    fig_change.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                              font_color="#ccd6f6")
    fig_change.update_xaxes(gridcolor="#1e2130")
    fig_change.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_change, width='stretch')


# ══════════════════════════════════════════════════════
# TAB 3 — RANKING ⭐
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">⭐ Composite Performance Score</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Το score συνδυάζει και τις 3 μετρικές σε ένα αριθμό (0–100). Υψηλό % επίλυσης σε 10 μέρες = καλό. Χαμηλός χρόνος επίλυσης = καλό. Κάθε μετρική κανονικοποιείται και συνδυάζεται με ίσα βάρη.</div>', unsafe_allow_html=True)

    score_data = df_f.groupby(["provider", "period_label", "period_order"]).agg(
        resolved_in_10d_pct=("resolved_in_10d_pct", "mean"),
        resolution_median_days=("resolution_median_days", "mean"),
        resolution_p95_days=("resolution_p95_days", "mean"),
    ).reset_index()

    # Normalize: για resolved → higher is better, για χρόνους → lower is better
    for col in ["resolved_in_10d_pct", "resolution_median_days", "resolution_p95_days"]:
        col_min, col_max = score_data[col].min(), score_data[col].max()
        if col_max > col_min:
            if col == "resolved_in_10d_pct":
                score_data[f"{col}_norm"] = (score_data[col] - col_min) / (col_max - col_min) * 100
            else:
                score_data[f"{col}_norm"] = (1 - (score_data[col] - col_min) / (col_max - col_min)) * 100
        else:
            score_data[f"{col}_norm"] = 100

    score_data["composite_score"] = (
        score_data["resolved_in_10d_pct_norm"] * 0.40 +
        score_data["resolution_median_days_norm"] * 0.30 +
        score_data["resolution_p95_days_norm"] * 0.30
    ).round(1)

    # Overall ranking
    overall_rank = score_data.groupby("provider")["composite_score"].mean().reset_index().sort_values("composite_score", ascending=False).reset_index(drop=True)
    overall_rank.index += 1
    overall_rank.columns = ["Πάροχος", "Composite Score"]
    overall_rank["Composite Score"] = overall_rank["Composite Score"].round(1)
    overall_rank["🏅"] = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][:len(overall_rank)]

    col_r1, col_r2 = st.columns([1, 2])

    with col_r1:
        st.markdown("##### 🏆 Overall Ranking")
        st.dataframe(overall_rank[["🏅", "Πάροχος", "Composite Score"]], use_container_width=True, hide_index=True)

    with col_r2:
        fig_score = px.bar(
            overall_rank.sort_values("Composite Score"), x="Composite Score", y="Πάροχος",
            orientation="h", color="Πάροχος", color_discrete_map=PROVIDER_COLORS,
            title="Composite Score ανά πάροχο (μ.ό. όλων των περιόδων)",
            range_x=[0, 100],
        )
        fig_score.update_layout(showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                                 font_color="#ccd6f6")
        fig_score.update_xaxes(gridcolor="#1e2130")
        fig_score.update_yaxes(gridcolor="#1e2130")
        st.plotly_chart(fig_score, width='stretch')

    st.markdown('<div class="section-title">Εξέλιξη Composite Score ανά εξάμηνο</div>', unsafe_allow_html=True)
    score_trend = score_data.sort_values("period_order")
    fig_st = px.line(
        score_trend, x="period_label", y="composite_score",
        color="provider", color_discrete_map=PROVIDER_COLORS,
        markers=True, title="Composite Score — χρονική εξέλιξη",
        labels={"composite_score": "Score (0–100)", "period_label": "Περίοδος", "provider": "Πάροχος"},
    )
    fig_st.update_traces(line_width=2.5, marker_size=8)
    fig_st.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6", height=380)
    fig_st.update_xaxes(gridcolor="#1e2130")
    fig_st.update_yaxes(gridcolor="#1e2130", range=[0, 100])
    st.plotly_chart(fig_st, width='stretch')

    st.markdown('<div class="section-title">Heatmap: Πάροχοι × Κατηγορίες</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Ποιος πάροχος τα πάει καλά σε ποια κατηγορία; Πιο σκούρο = καλύτερη απόδοση στην επιλεγμένη μετρική.</div>', unsafe_allow_html=True)

    heatmap_data = df_f.pivot_table(index="category", columns="provider", values=metric_choice, aggfunc="mean").round(2)
    fig_heat = px.imshow(
        heatmap_data,
        color_continuous_scale="teal" if metric_choice == "resolved_in_10d_pct" else "RdYlGn_r",
        title=f"Heatmap: {metric_labels[metric_choice]}",
        aspect="auto",
        text_auto=".1f",
    )
    fig_heat.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6", height=480)
    st.plotly_chart(fig_heat, width='stretch')


# ══════════════════════════════════════════════════════
# TAB 4 — ΚΑΤΗΓΟΡΙΕΣ ⭐
# ══════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">⭐ "Δύσκολες" vs "Εύκολες" κατηγορίες</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Κατηγορίες με σταθερά υψηλό P95 σε ΟΛΟΥΣ τους παρόχους υποδηλώνουν structural πρόβλημα του κλάδου — όχι αδυναμία ενός παρόχου.</div>', unsafe_allow_html=True)

    cat_stats = df_f.groupby("category").agg(
        mean_resolved=("resolved_in_10d_pct", "mean"),
        mean_p95=("resolution_p95_days", "mean"),
        std_p95=("resolution_p95_days", "std"),
    ).reset_index().sort_values("mean_p95", ascending=False)
    # Κατηγορίες με μία μόνο εγγραφή έχουν std=NaN → fillna(0)
    cat_stats["std_p95"] = cat_stats["std_p95"].fillna(0)
    # Plotly απαιτεί size > 0 → ελάχιστο 0.5
    cat_stats["bubble_size"] = (cat_stats["std_p95"] + 0.5)

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        fig_cat1 = px.bar(
            cat_stats.sort_values("mean_p95", ascending=True),
            x="mean_p95", y="category", orientation="h",
            color="mean_p95", color_continuous_scale="RdYlGn_r",
            title="Μέσος P95 χρόνος ανά κατηγορία (όλοι οι πάροχοι)",
            labels={"mean_p95": "P95 (μέρες)", "category": ""},
        )
        fig_cat1.update_layout(coloraxis_showscale=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6")
        fig_cat1.update_xaxes(gridcolor="#1e2130")
        fig_cat1.update_yaxes(gridcolor="#1e2130")
        st.plotly_chart(fig_cat1, width='stretch')

    with col_c2:
        fig_cat2 = px.bar(
            cat_stats.sort_values("mean_resolved", ascending=True),
            x="mean_resolved", y="category", orientation="h",
            color="mean_resolved", color_continuous_scale="teal",
            title="Μέση % επίλυση σε 10 μέρες ανά κατηγορία",
            labels={"mean_resolved": "% Επίλυση 10ημ.", "category": ""},
        )
        fig_cat2.update_layout(coloraxis_showscale=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6")
        fig_cat2.update_xaxes(gridcolor="#1e2130")
        fig_cat2.update_yaxes(gridcolor="#1e2130")
        st.plotly_chart(fig_cat2, width='stretch')

    st.markdown('<div class="section-title">Bubble chart: Δυσκολία κατηγοριών</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Ο άξονας Χ δείχνει το % επίλυσης σε 10 μέρες, ο Υ τον P95 χρόνο. Πάνω-αριστερά = δύσκολες κατηγορίες. Κάτω-δεξιά = εύκολες.</div>', unsafe_allow_html=True)

    fig_bubble = px.scatter(
        cat_stats, x="mean_resolved", y="mean_p95",
        text="category", size="bubble_size",
        color="mean_p95", color_continuous_scale="RdYlGn_r",
        title="Κατηγορίες: ευκολία επίλυσης vs χρόνος P95",
        labels={"mean_resolved": "% Επίλυση σε 10 μέρες", "mean_p95": "P95 χρόνος (μέρες)", "std_p95": "Std P95"},
    )
    fig_bubble.update_traces(textposition="top center", textfont_size=10)
    fig_bubble.update_layout(coloraxis_showscale=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                              font_color="#ccd6f6", height=450)
    fig_bubble.update_xaxes(gridcolor="#1e2130")
    fig_bubble.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_bubble, width='stretch')

    st.markdown('<div class="section-title">Βελτίωση κατηγοριών 2022 → 2024</div>', unsafe_allow_html=True)
    cat_trend = df_f.groupby(["category", "year"])[metric_choice].mean().reset_index()
    first_y = cat_trend.groupby("category")["year"].min().reset_index().rename(columns={"year": "first_year"})
    last_y  = cat_trend.groupby("category")["year"].max().reset_index().rename(columns={"year": "last_year"})
    fv = cat_trend.merge(first_y, left_on=["category", "year"], right_on=["category", "first_year"])[["category", metric_choice]].rename(columns={metric_choice: "first_val"})
    lv = cat_trend.merge(last_y,  left_on=["category", "year"], right_on=["category", "last_year"])[["category", metric_choice]].rename(columns={metric_choice: "last_val"})
    cat_change = fv.merge(lv, on="category")
    cat_change["change"] = cat_change["last_val"] - cat_change["first_val"]

    fig_cat_ch = px.bar(
        cat_change.sort_values("change"), x="change", y="category", orientation="h",
        color="change",
        color_continuous_scale="RdYlGn" if metric_choice == "resolved_in_10d_pct" else "RdYlGn_r",
        title=f"Μεταβολή {metric_labels[metric_choice]} ανά κατηγορία (2022→2024)",
        labels={"change": "Μεταβολή", "category": ""},
    )
    fig_cat_ch.update_layout(coloraxis_showscale=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                              font_color="#ccd6f6")
    fig_cat_ch.update_xaxes(gridcolor="#1e2130")
    fig_cat_ch.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_cat_ch, width='stretch')


# ══════════════════════════════════════════════════════
# TAB 5 — OUTLIERS ⭐
# ══════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">⭐ Ανίχνευση "κρίσεων" — P95 spikes</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Εντοπισμός εξαμήνων όπου ένας πάροχος είχε ξαφνική εκτίναξη στον P95 χρόνο επίλυσης. Αυτά συχνά αντιστοιχούν σε δικτυακά συμβάντα ή αλλαγές πολιτικής.</div>', unsafe_allow_html=True)

    spike_data = df_f.groupby(["provider", "period_label", "period_order"])["resolution_p95_days"].mean().reset_index()
    spike_data = spike_data.sort_values("period_order")

    # Z-score ανά πάροχο για εντοπισμό spikes
    spike_data["z_score"] = spike_data.groupby("provider")["resolution_p95_days"].transform(
        lambda x: (x - x.mean()) / x.std() if x.std() > 0 else 0
    )
    spike_data["is_spike"] = spike_data["z_score"].abs() > 1.5
    spike_data["point_size"] = spike_data["z_score"].abs() * 8 + 6

    fig_spike = px.scatter(
        spike_data, x="period_label", y="resolution_p95_days",
        color="provider", color_discrete_map=PROVIDER_COLORS,
        size="point_size", symbol="is_spike",
        symbol_map={True: "x", False: "circle"},
        title="P95 χρόνος επίλυσης — εντοπισμός spikes (✕ = Z-score > 1.5)",
        labels={"resolution_p95_days": "P95 (μέρες)", "period_label": "Περίοδος", "provider": "Πάροχος"},
        hover_data={"z_score": ":.2f", "is_spike": True, "point_size": False},
    )
    fig_spike.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6", height=420)
    fig_spike.update_xaxes(gridcolor="#1e2130")
    fig_spike.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_spike, width='stretch')

    spikes_found = spike_data[spike_data["is_spike"]].sort_values("z_score", ascending=False)
    if not spikes_found.empty:
        st.markdown("##### 🚨 Περίοδοι με ανώμαλη συμπεριφορά")
        st.dataframe(spikes_found[["provider", "period_label", "resolution_p95_days", "z_score"]].rename(columns={
            "provider": "Πάροχος", "period_label": "Περίοδος",
            "resolution_p95_days": "P95 (μέρες)", "z_score": "Z-score"
        }).round(2), width='stretch', hide_index=True)

    st.markdown('<div class="section-title">Box plots — κατανομή P95 ανά πάροχο</div>', unsafe_allow_html=True)
    fig_box = px.box(
        df_f, x="provider", y="resolution_p95_days",
        color="provider", color_discrete_map=PROVIDER_COLORS,
        title="Κατανομή P95 χρόνου επίλυσης (box plot)",
        labels={"resolution_p95_days": "P95 (μέρες)", "provider": "Πάροχος"},
        points="outliers",
    )
    fig_box.update_layout(showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6")
    fig_box.update_xaxes(gridcolor="#1e2130")
    fig_box.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_box, width='stretch')

    st.markdown('<div class="section-title">Consistency Score — ποιος έχει τη μεγαλύτερη σταθερότητα;</div>', unsafe_allow_html=True)
    consistency = df_f.groupby("provider")[metric_choice].agg(["mean", "std"]).reset_index()
    consistency["cv"] = (consistency["std"] / consistency["mean"] * 100).round(1)  # coefficient of variation
    consistency = consistency.sort_values("cv")
    consistency.columns = ["Πάροχος", "Μέσος", "Std", "CV (%)"]
    st.markdown('<div class="insight-box">Coefficient of Variation (CV) = std/mean. Χαμηλό CV = σταθερή απόδοση. Υψηλό CV = ανομοιόμορφη εξυπηρέτηση.</div>', unsafe_allow_html=True)

    fig_cv = px.bar(
        consistency.sort_values("CV (%)"), x="CV (%)", y="Πάροχος", orientation="h",
        color="Πάροχος", color_discrete_map=PROVIDER_COLORS,
        title="Coefficient of Variation — σταθερότητα απόδοσης (χαμηλότερο = πιο σταθερός)",
    )
    fig_cv.update_layout(showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6")
    fig_cv.update_xaxes(gridcolor="#1e2130")
    fig_cv.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_cv, width='stretch')


# ══════════════════════════════════════════════════════
# TAB 6 — ΣΥΣΧΕΤΙΣΕΙΣ ⭐
# ══════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-title">⭐ Correlation Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Υπάρχει trade-off μεταξύ "λύνω γρήγορα το 90%" (resolved_in_10d) και "λύνω και τις δύσκολες υποθέσεις" (P95);</div>', unsafe_allow_html=True)

    corr_df = df_f[["resolved_in_10d_pct", "resolution_median_days", "resolution_p95_days"]].copy()
    corr_matrix = corr_df.corr().round(2)

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        title="Correlation Matrix — μετρικές απόδοσης",
        labels=dict(color="Correlation"),
    )
    fig_corr.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6", height=350)
    st.plotly_chart(fig_corr, width='stretch')

    st.markdown('<div class="section-title">Scatter: resolved_in_10d vs P95 ανά πάροχο</div>', unsafe_allow_html=True)

    fig_scatter = px.scatter(
        df_f, x="resolved_in_10d_pct", y="resolution_p95_days",
        color="provider", color_discrete_map=PROVIDER_COLORS,
        title="% Επίλυση 10ημ. vs P95 χρόνος — ανά πάροχο",
        labels={
            "resolved_in_10d_pct": "% Επίλυση σε 10 μέρες",
            "resolution_p95_days": "P95 χρόνος (μέρες)",
            "provider": "Πάροχος",
        },
        opacity=0.65,
        hover_data=["category", "period"],
    )
    # Regression line με numpy (δεν χρειάζεται statsmodels)
    _x = df_f["resolved_in_10d_pct"].dropna()
    _y = df_f["resolution_p95_days"].dropna()
    _common = df_f[["resolved_in_10d_pct","resolution_p95_days"]].dropna()
    _m, _b = np.polyfit(_common["resolved_in_10d_pct"], _common["resolution_p95_days"], 1)
    _xr = np.linspace(_common["resolved_in_10d_pct"].min(), _common["resolved_in_10d_pct"].max(), 100)
    fig_scatter.add_trace(go.Scatter(x=_xr, y=_m*_xr+_b, mode="lines",
        line=dict(color="rgba(255,255,255,0.4)", dash="dash", width=1.5), name="Regression (overall)", showlegend=True))
    fig_scatter.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6", height=450)
    fig_scatter.update_xaxes(gridcolor="#1e2130")
    fig_scatter.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_scatter, width='stretch')

    st.markdown('<div class="section-title">Scatter: Median vs P95 — consistency test</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Αν median και P95 είναι πολύ κοντά → ομοιόμορφη εξυπηρέτηση. Αν P95 >> median → υπάρχουν ακραίες περιπτώσεις που "χαλάνε" την εικόνα.</div>', unsafe_allow_html=True)

    fig_sc2 = px.scatter(
        df_f, x="resolution_median_days", y="resolution_p95_days",
        color="provider", color_discrete_map=PROVIDER_COLORS,
        title="Διάμεσος vs P95 χρόνος επίλυσης",
        labels={"resolution_median_days": "Διάμεσος (μέρες)", "resolution_p95_days": "P95 (μέρες)", "provider": "Πάροχος"},
        opacity=0.65,
        hover_data=["category", "period"],
    )
    # Γραμμή y=x για αναφορά (τέλεια συνέπεια)
    max_val = max(df_f["resolution_p95_days"].max(), df_f["resolution_median_days"].max())
    fig_sc2.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val], mode="lines",
                                  line=dict(dash="dash", color="rgba(255,255,255,0.27)"), name="y=x (τέλεια συνέπεια)", showlegend=True))
    fig_sc2.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6", height=430)
    fig_sc2.update_xaxes(gridcolor="#1e2130")
    fig_sc2.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_sc2, width='stretch')


# ══════════════════════════════════════════════════════
# TAB 7 — NETWORK TYPE ⭐
# ══════════════════════════════════════════════════════
with tab7:
    st.markdown('<div class="section-title">⭐ 2G/3G vs 4G/5G — διαφέρει η εξυπηρέτηση;</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Αν οι πάροχοι εξυπηρετούν καλύτερα παράπονα 4G/5G (data_4G5G) vs φωνής (voice_2G3G), αυτό υποδηλώνει επιλεκτική επένδυση στην εξυπηρέτηση.</div>', unsafe_allow_html=True)

    net_data = df_f.groupby(["provider", "network_label"])[metric_choice].mean().reset_index()

    fig_net = px.bar(
        net_data, x="provider", y=metric_choice,
        color="network_label",
        color_discrete_map={"voice_2G3G": "#6c9bcc", "data_4G5G": "#64ffda", "unspecified": "#888"},
        barmode="group",
        title=f"{metric_labels[metric_choice]} ανά πάροχο & τύπο δικτύου",
        labels={metric_choice: metric_labels[metric_choice], "provider": "Πάροχος", "network_label": "Τύπος δικτύου"},
    )
    fig_net.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6")
    fig_net.update_xaxes(gridcolor="#1e2130")
    fig_net.update_yaxes(gridcolor="#1e2130")
    st.plotly_chart(fig_net, width='stretch')

    st.markdown('<div class="section-title">Διαφορά απόδοσης μεταξύ δικτύων ανά πάροχο</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-box">Ποιος πάροχος έχει τη μεγαλύτερη διαφορά απόδοσης μεταξύ 2G/3G και 4G/5G;</div>', unsafe_allow_html=True)

    net_pivot = net_data[net_data["network_label"].isin(["voice_2G3G", "data_4G5G"])].pivot_table(
        index="provider", columns="network_label", values=metric_choice
    ).reset_index()

    if "voice_2G3G" in net_pivot.columns and "data_4G5G" in net_pivot.columns:
        net_pivot["diff"] = net_pivot["data_4G5G"] - net_pivot["voice_2G3G"]
        fig_diff = px.bar(
            net_pivot.sort_values("diff"), x="diff", y="provider", orientation="h",
            color="provider", color_discrete_map=PROVIDER_COLORS,
            title=f"Διαφορά {metric_labels[metric_choice]}: 4G/5G minus 2G/3G",
            labels={"diff": "Διαφορά (4G/5G − 2G/3G)", "provider": ""},
        )
        fig_diff.update_layout(showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ccd6f6")
        fig_diff.update_xaxes(gridcolor="#1e2130")
        fig_diff.update_yaxes(gridcolor="#1e2130")
        st.plotly_chart(fig_diff, width='stretch')

    st.markdown('<div class="section-title">Box plot: κατανομή P95 ανά τύπο δικτύου</div>', unsafe_allow_html=True)
    fig_box_net = px.box(
        df_f[df_f["network_label"] != "unspecified"],
        x="network_label", y="resolution_p95_days",
        color="network_label",
        color_discrete_map={"voice_2G3G": "#6c9bcc", "data_4G5G": "#64ffda"},
        facet_col="provider",
        title="Κατανομή P95 ανά τύπο δικτύου & πάροχο",
        labels={"resolution_p95_days": "P95 (μέρες)", "network_label": "Δίκτυο"},
        points="outliers",
    )
    fig_box_net.update_layout(showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                               font_color="#ccd6f6", height=400)
    for ax in fig_box_net.layout:
        if ax.startswith("xaxis"):
            fig_box_net.layout[ax].gridcolor = "#1e2130"
        if ax.startswith("yaxis"):
            fig_box_net.layout[ax].gridcolor = "#1e2130"
    st.plotly_chart(fig_box_net, width='stretch')


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#4a5568; font-size:0.8rem;'>"
    "📊 Mobile Complaints Dashboard · Δεδομένα: ΕΕΤΤ 2022–2024 · "
    "Built with Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True,
)
