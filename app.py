import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Optik Cahaya Murni · Analisis Pelanggan",
    page_icon="👓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
#  GLOBAL STYLE
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Font & base ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #111111; }

    /* ── Background ── */
    .stApp { background: #F5F7FF; }

    /* ── Force semua teks utama jadi hitam ── */
    .stApp p, .stApp span, .stApp div, .stApp label,
    .stApp li, .stApp td, .stApp th {
        color: #111111 !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1F5E 0%, #2B3594 100%) !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label { color: white !important; }

    /* ── Metric cards ── */
    [data-testid="metric-container"] {
        background: white !important;
        border: 1px solid #E8EAFF !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        box-shadow: 0 2px 12px rgba(43,53,148,0.07) !important;
    }
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] span,
    [data-testid="stMetricLabel"] div {
        color: #555555 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div,
    [data-testid="stMetricValue"] span {
        color: #111111 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricDelta"] span { font-size: 12px !important; font-weight: 600 !important; }

    /* ── Selectbox & widget labels ── */
    .stSelectbox label, .stRadio label,
    .stSelectbox > div > label, .stRadio > div > label {
        color: #111111 !important;
        font-weight: 600 !important;
    }
    /* teks nilai terpilih di kotak selectbox → putih biar keliatan di bg gelap */
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] div,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span { color: white !important; }
    /* teks di dalam popup list dropdown → putih */
    [data-baseweb="popover"] *,
    [data-baseweb="menu"] *,
    [role="listbox"] *,
    [role="option"] * { color: white !important; }

    /* ── Card wrapper ── */
    .card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 12px rgba(43,53,148,0.07);
        border: 1px solid #E8EAFF;
        margin-bottom: 16px;
    }

    /* ── Section title ── */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111111 !important;
        margin-bottom: 4px;
        letter-spacing: -0.01em;
    }
    .section-sub {
        font-size: 0.8rem;
        color: #666666 !important;
        margin-bottom: 16px;
    }

    /* ── Segment badges ── */
    .badge {
        display: inline-block;
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .badge-loyal     { background:#DCFCE7; color:#15803D !important; }
    .badge-potensial { background:#DBEAFE; color:#1D4ED8 !important; }
    .badge-baru      { background:#FEF9C3; color:#92400E !important; }
    .badge-pasif     { background:#FEE2E2; color:#B91C1C !important; }

    /* ── Hero banner ── */
    .hero {
        background: linear-gradient(135deg, #1A1F5E 0%, #3B4ECC 60%, #6D7FE8 100%);
        border-radius: 20px;
        padding: 36px 40px;
        margin-bottom: 28px;
    }
    .hero h1 { font-size: 2rem; font-weight: 800; margin: 0 0 6px 0; letter-spacing: -0.02em; color: white !important; }
    .hero p  { font-size: 0.95rem; opacity: 0.85; margin: 0; color: white !important; }

    /* ── Divider ── */
    hr { border: none; border-top: 1px solid #E8EAFF; margin: 20px 0; }

    /* ── Tables ── */
    .stDataFrame { border-radius: 12px !important; overflow: hidden; }

    /* ── Streamlit default tweaks ── */
    .block-container { padding-top: 1.5rem !important; }
    h1, h2, h3 { color: #111111 !important; font-weight: 800; }

    /* ── Alert boxes ── */
    .alert-green  { background:#F0FDF4; border-left:4px solid #22C55E; border-radius:8px; padding:12px 16px; margin:8px 0; font-size:0.88rem; }
    .alert-green  * { color:#166534 !important; }
    .alert-red    { background:#FFF1F2; border-left:4px solid #F43F5E; border-radius:8px; padding:12px 16px; margin:8px 0; font-size:0.88rem; }
    .alert-red    * { color:#9F1239 !important; }
    .alert-blue   { background:#EFF6FF; border-left:4px solid #3B82F6; border-radius:8px; padding:12px 16px; margin:8px 0; font-size:0.88rem; }
    .alert-blue   * { color:#1E40AF !important; }
    .alert-yellow { background:#FFFBEB; border-left:4px solid #F59E0B; border-radius:8px; padding:12px 16px; margin:8px 0; font-size:0.88rem; }
    .alert-yellow * { color:#92400E !important; }

    /* ── Strategy card ── */
    .strat-card {
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 12px;
        border: 1px solid;
    }
    .strat-loyal     { background:#F0FDF4; border-color:#86EFAC; }
    .strat-potensial { background:#EFF6FF; border-color:#93C5FD; }
    .strat-baru      { background:#FFFBEB; border-color:#FCD34D; }
    .strat-pasif     { background:#FFF1F2; border-color:#FCA5A5; }
    .strat-card * { color: #111111 !important; }
    .strat-title { font-weight: 700; font-size: 1rem; margin-bottom: 8px; color: #111111 !important; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  COLOUR SYSTEM
# ──────────────────────────────────────────────
PALETTE = {
    "Loyal":     "#22C55E",
    "Potensial": "#3B82F6",
    "Baru":      "#F59E0B",
    "Pasif":     "#F43F5E",
}
BG_PALETTE = {
    "Loyal":     "#DCFCE7",
    "Potensial": "#DBEAFE",
    "Baru":      "#FEF9C3",
    "Pasif":     "#FEE2E2",
}

def seg_color(label):
    return PALETTE.get(label, "#6B7280")

def badge_html(label):
    cls = f"badge-{label.lower()}"
    return f'<span class="badge {cls}">{label}</span>'


# ──────────────────────────────────────────────
#  MATPLOTLIB THEME
# ──────────────────────────────────────────────
def apply_mpl_theme(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor("white")
    ax.figure.patch.set_facecolor("white")
    for sp in ax.spines.values():
        sp.set_color("#E8EAFF")
    ax.tick_params(colors="#6B7280", labelsize=9)
    ax.set_title(title, fontsize=12, fontweight="bold", color="#1A1F5E", pad=10)
    ax.set_xlabel(xlabel, fontsize=9, color="#9CA3AF")
    ax.set_ylabel(ylabel, fontsize=9, color="#9CA3AF")
    ax.yaxis.grid(True, color="#F3F4F6", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.xaxis.grid(False)


# ──────────────────────────────────────────────
#  LOAD DATA
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("rfm_clustered_all.csv")
    except FileNotFoundError:
        # fallback: generate sample data matching thesis structure
        np.random.seed(42)
        names = [f"pelanggan_{i:03d}" for i in range(1, 101)]
        years = [2021, 2022, 2023, 2024, 2025]
        rows = []
        for yr in years:
            pool = np.random.choice(names, size=int(np.random.randint(35, 70)), replace=False)
            for n in pool:
                freq = np.random.randint(1, 7)
                mon  = np.random.randint(1, 9) * 50000
                rows.append({"NAMA": n, "TAHUN": yr, "Frequency": freq, "Monetary": mon})
        df = pd.DataFrame(rows)
        df["Cluster"] = 0
        # simple label based on combined score
        def label_row(r):
            score = r["Frequency"] + r["Monetary"] / 200000
            if score > 6: return "Loyal"
            if score > 3: return "Potensial"
            if score > 1.5: return "Baru"
            return "Pasif"
        df["Label"] = df.apply(label_row, axis=1)
    return df

df = load_data()
ALL_YEARS  = sorted(df["TAHUN"].unique())
ALL_LABELS = ["Loyal", "Potensial", "Baru", "Pasif"]


# ──────────────────────────────────────────────
#  SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <div style="font-size:2.4rem;">👓</div>
        <div style="font-size:1rem; font-weight:800; letter-spacing:-0.01em;">Optik Cahaya Murni</div>
        <div style="font-size:0.75rem; opacity:0.65; margin-top:2px;">Analisis Perilaku Pelanggan</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio(
        "Navigasi",
        ["🏠  Overview", "🎯  Segmentasi", "📈  Temporal", "💡  Insight Bisnis"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem; opacity:0.55; text-align:center; line-height:1.6;">
        Skripsi · Deo Pratama Putra<br>
        Universitas Bhayangkara Jakarta Raya · 2026
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  PAGE 1 — OVERVIEW
# ──────────────────────────────────────────────
if "Overview" in menu:

    st.markdown("""
    <div class="hero">
        <h1>👓 Dashboard Segmentasi Pelanggan</h1>
        <p>Temporal Clustering · RFM Analysis · K-Means · Optik Cahaya Murni Bekasi · 2021–2025</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Transaksi Mentah", 320, help="Jumlah baris data sebelum proses RFM")
    c2.metric("Total Data RFM / Cluster", len(df), help="Pelanggan unik hasil kalkulasi RFM yang masuk proses K-Means")
    c3.metric("Periode Analisis", f"{ALL_YEARS[0]}–{ALL_YEARS[-1]}", help="Rentang tahun data transaksi yang digunakan")
    c4.metric("Rata-rata Monetary", f"Rp {int(df['Monetary'].mean()):,}", help="Rata-rata total nilai transaksi kumulatif per pelanggan")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row: trend + seg pie ──
    col_a, col_b = st.columns([3, 2], gap="large")

    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Tren Transaksi per Tahun</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Jumlah transaksi & pelanggan unik setiap tahun</div>', unsafe_allow_html=True)

        trend = df.groupby("TAHUN").agg(
            Transaksi=("NAMA", "count"),
            Pelanggan=("NAMA", "nunique"),
            Revenue=("Monetary", "sum"),
        ).reset_index()

        fig, ax1 = plt.subplots(figsize=(7, 3.4))
        bars = ax1.bar(trend["TAHUN"], trend["Transaksi"],
                       color="#3B4ECC", alpha=0.85, width=0.5, zorder=3, label="Transaksi")
        ax1.bar(trend["TAHUN"], trend["Pelanggan"],
                color="#93C5FD", alpha=0.7, width=0.5, zorder=2, label="Pelanggan Unik")
        apply_mpl_theme(ax1, ylabel="Jumlah")

        ax2 = ax1.twinx()
        ax2.plot(trend["TAHUN"], trend["Revenue"]/1e6, "o-",
                 color="#F59E0B", linewidth=2.5, markersize=6, zorder=4, label="Revenue (juta)")
        ax2.set_ylabel("Revenue (Juta Rp)", fontsize=9, color="#F59E0B")
        ax2.tick_params(colors="#F59E0B", labelsize=9)
        ax2.spines["right"].set_color("#FBBF24")

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, fontsize=8, framealpha=0, loc="upper left")

        ax1.set_xticks(trend["TAHUN"])
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🍩 Komposisi Segmen (All Years)</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Proporsi label pelanggan keseluruhan</div>', unsafe_allow_html=True)

        seg_all = df["Label"].value_counts().reindex(ALL_LABELS, fill_value=0)
        colors  = [PALETTE.get(l, "#ccc") for l in seg_all.index]

        fig, ax = plt.subplots(figsize=(4.5, 3.5))
        wedges, texts, autotexts = ax.pie(
            seg_all.values, labels=seg_all.index,
            colors=colors, autopct="%1.0f%%",
            pctdistance=0.75, startangle=90,
            wedgeprops=dict(width=0.6, edgecolor="white", linewidth=2),
        )
        for t in texts: t.set_fontsize(9); t.set_color("#374151"); t.set_fontweight("600")
        for a in autotexts: a.set_fontsize(9); a.set_color("white"); a.set_fontweight("700")
        ax.set_facecolor("white"); fig.patch.set_facecolor("white")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Year-by-year summary table ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Ringkasan per Tahun</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Distribusi segmen pelanggan setiap tahun</div>', unsafe_allow_html=True)

    rows_summary = []
    for yr in ALL_YEARS:
        ydf = df[df["TAHUN"] == yr]
        row = {"Tahun": yr, "Total Pelanggan": len(ydf),
               "Revenue (Rp)": f"Rp {ydf['Monetary'].sum():,.0f}"}
        for lbl in ALL_LABELS:
            row[lbl] = int((ydf["Label"] == lbl).sum())
        rows_summary.append(row)

    summary_df = pd.DataFrame(rows_summary)
    st.dataframe(summary_df.set_index("Tahun"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  PAGE 2 — SEGMENTASI
# ──────────────────────────────────────────────
elif "Segmentasi" in menu:

    st.markdown("""
    <div class="hero">
        <h1>🎯 Segmentasi Pelanggan</h1>
        <p>Distribusi cluster K-Means berdasarkan nilai Frequency dan Monetary setiap tahun</p>
    </div>
    """, unsafe_allow_html=True)

    tahun = st.selectbox("Pilih Tahun", ALL_YEARS, index=len(ALL_YEARS)-1)
    data  = df[df["TAHUN"] == tahun]

    # ── KPI for selected year ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Pelanggan", len(data))
    c2.metric("Rata-rata Frequency", f"{data['Frequency'].mean():.2f}x")
    c3.metric("Total Revenue", f"Rp {data['Monetary'].sum():,.0f}")
    c4.metric("Jumlah Cluster", data["Cluster"].nunique())

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # ── Bar chart ──
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">📊 Distribusi Segmen – {tahun}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Jumlah pelanggan per segmen (semua segmen ditampilkan)</div>', unsafe_allow_html=True)

        seg_count = data["Label"].value_counts().reindex(ALL_LABELS, fill_value=0)
        colors_bar = [PALETTE.get(l, "#ccc") for l in seg_count.index]

        fig, ax = plt.subplots(figsize=(6, 3.5))
        bars = ax.bar(seg_count.index, seg_count.values, color=colors_bar,
                      width=0.55, zorder=3, edgecolor="white", linewidth=1.5)
        for bar, val in zip(bars, seg_count.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(val), ha="center", va="bottom", fontsize=11,
                    fontweight="700", color="#1A1F5E")
        apply_mpl_theme(ax, ylabel="Jumlah Pelanggan")
        ax.set_ylim(0, seg_count.max() * 1.2 + 2)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Scatter F vs M ──
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">🔵 Sebaran Frequency vs Monetary – {tahun}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Posisi setiap pelanggan berdasarkan intensitas dan nilai transaksi</div>', unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(6, 3.5))
        for lbl in ALL_LABELS:
            sub = data[data["Label"] == lbl]
            if len(sub) == 0: continue
            ax.scatter(sub["Frequency"], sub["Monetary"],
                       label=lbl, color=PALETTE[lbl], alpha=0.7,
                       s=50, edgecolors="white", linewidths=0.5, zorder=3)
        apply_mpl_theme(ax, xlabel="Frequency (kumulatif)", ylabel="Monetary (Rp)")
        ax.legend(fontsize=8, framealpha=0)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Segment profiles ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📋 Profil Setiap Segmen – {tahun}</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Rata-rata Frequency, Monetary, dan jumlah pelanggan per segmen</div>', unsafe_allow_html=True)

    profile = data.groupby("Label").agg(
        Jumlah_Pelanggan=("NAMA","count"),
        Rata2_Frequency=("Frequency","mean"),
        Rata2_Monetary=("Monetary","mean"),
        Total_Revenue=("Monetary","sum"),
    ).reindex(ALL_LABELS).dropna()
    profile["Rata2_Frequency"] = profile["Rata2_Frequency"].round(2)
    profile["Rata2_Monetary"]  = profile["Rata2_Monetary"].apply(lambda x: f"Rp {x:,.0f}")
    profile["Total_Revenue"]   = profile["Total_Revenue"].apply(lambda x: f"Rp {x:,.0f}")
    profile.index = [f"{badge_html(i)}" for i in profile.index]

    st.write(profile.to_html(escape=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  PAGE 3 — TEMPORAL
# ──────────────────────────────────────────────
elif "Temporal" in menu:

    st.markdown("""
    <div class="hero">
        <h1>📈 Analisis Temporal</h1>
        <p>Migrasi pelanggan antar segmen, pelanggan baru, dan churn periode 2021–2025</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Period selector ──
    idx = st.selectbox(
        "Pilih Periode Perbandingan",
        range(len(ALL_YEARS)-1),
        format_func=lambda x: f"{ALL_YEARS[x]}  →  {ALL_YEARS[x+1]}",
    )
    t1, t2 = ALL_YEARS[idx], ALL_YEARS[idx+1]

    d1 = df[df["TAHUN"] == t1][["NAMA","Label"]].rename(columns={"Label": f"Label_{t1}"})
    d2 = df[df["TAHUN"] == t2][["NAMA","Label"]].rename(columns={"Label": f"Label_{t2}"})

    merge  = pd.merge(d1, d2, on="NAMA", how="outer")
    baru   = merge[merge[f"Label_{t1}"].isna()]
    churn  = merge[merge[f"Label_{t2}"].isna()]
    migrasi = merge.dropna()

    # ── KPI row ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pelanggan Konsisten", len(migrasi), help="Muncul di kedua tahun")
    c2.metric("Pelanggan Baru", len(baru), f"+{len(baru)}")
    c3.metric("Churn", len(churn), f"-{len(churn)}", delta_color="inverse")
    total_both = len(migrasi) + len(baru) + len(churn)
    churn_pct  = len(churn) / total_both * 100 if total_both else 0
    c4.metric("Churn Rate", f"{churn_pct:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2], gap="large")

    # ── Heatmap migrasi ──
    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">🔄 Heatmap Migrasi Segmen ({t1} → {t2})</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Baris = segmen asal · Kolom = segmen tujuan · Angka = jumlah pelanggan</div>', unsafe_allow_html=True)

        if len(migrasi) > 0:
            pivot = migrasi.groupby(
                [f"Label_{t1}", f"Label_{t2}"]
            ).size().unstack(fill_value=0).reindex(
                index=ALL_LABELS, columns=ALL_LABELS, fill_value=0
            )
            fig, ax = plt.subplots(figsize=(6, 3.8))
            sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues",
                        linewidths=0.5, linecolor="#E8EAFF",
                        annot_kws={"fontsize": 11, "fontweight": "bold"},
                        ax=ax, cbar_kws={"shrink": 0.7})
            ax.set_xlabel(f"Segmen {t2}", fontsize=9, color="#6B7280")
            ax.set_ylabel(f"Segmen {t1}", fontsize=9, color="#6B7280")
            ax.tick_params(colors="#374151", labelsize=9)
            ax.figure.patch.set_facecolor("white")
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close()
        else:
            st.info("Tidak ada pelanggan yang muncul di kedua tahun ini.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Bar migrasi/baru/churn ──
    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">📊 Dinamika Pelanggan per Periode</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Perbandingan antar semua periode</div>', unsafe_allow_html=True)

        periods, n_baru_list, n_churn_list, n_mig_list = [], [], [], []
        for i in range(len(ALL_YEARS)-1):
            t_a, t_b = ALL_YEARS[i], ALL_YEARS[i+1]
            da = df[df["TAHUN"]==t_a][["NAMA","Label"]]
            db = df[df["TAHUN"]==t_b][["NAMA","Label"]]
            m  = pd.merge(da, db, on="NAMA", how="outer", suffixes=("_a","_b"))
            periods.append(f"{t_a}→{t_b}")
            n_baru_list.append(m["Label_a"].isna().sum())
            n_churn_list.append(m["Label_b"].isna().sum())
            n_mig_list.append(m.dropna().shape[0])

        x = np.arange(len(periods))
        w = 0.25
        fig, ax = plt.subplots(figsize=(5.5, 3.8))
        ax.bar(x - w, n_mig_list,   w, label="Konsisten",  color="#3B4ECC", alpha=0.85, zorder=3)
        ax.bar(x,     n_baru_list,  w, label="Baru",        color="#22C55E", alpha=0.85, zorder=3)
        ax.bar(x + w, n_churn_list, w, label="Churn",       color="#F43F5E", alpha=0.85, zorder=3)
        apply_mpl_theme(ax, ylabel="Jumlah Pelanggan")
        ax.set_xticks(x); ax.set_xticklabels(periods, fontsize=7.5, rotation=15)
        ax.legend(fontsize=8, framealpha=0)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Heatmap distribusi semua tahun ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗓️ Heatmap Distribusi Segmen 2021–2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Intensitas warna menunjukkan jumlah pelanggan per segmen per tahun</div>', unsafe_allow_html=True)

    heat_data = df.groupby(["TAHUN","Label"]).size().unstack(fill_value=0).reindex(
        columns=ALL_LABELS, fill_value=0
    )
    fig, axes = plt.subplots(1, len(ALL_YEARS), figsize=(12, 2.8), sharey=True)
    for ax, yr in zip(axes, ALL_YEARS):
        panel = heat_data.loc[[yr]].reindex(columns=ALL_LABELS, fill_value=0)
        sns.heatmap(panel.T, annot=True, fmt="d", cmap="YlGn",
                    linewidths=0.5, linecolor="#E8EAFF",
                    annot_kws={"fontsize":11,"fontweight":"bold"},
                    ax=ax, cbar=False, vmin=0, vmax=heat_data.values.max())
        ax.set_title(str(yr), fontsize=10, fontweight="700", color="#1A1F5E")
        ax.set_xlabel("")
        ax.tick_params(left=False if yr != ALL_YEARS[0] else True,
                       bottom=False, labelbottom=False, labelsize=9)
        ax.figure.patch.set_facecolor("white")
        ax.set_facecolor("white")

    axes[0].set_ylabel("Segmen", fontsize=9, color="#6B7280")
    plt.suptitle("Distribusi Pelanggan per Segmen per Tahun", fontsize=11,
                 fontweight="800", color="#1A1F5E", y=1.02)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  PAGE 4 — INSIGHT BISNIS
# ──────────────────────────────────────────────
elif "Insight" in menu:

    st.markdown("""
    <div class="hero">
        <h1>💡 Insight & Rekomendasi Strategis</h1>
        <p>Analisis kondisi bisnis dan strategi berbasis segmen pelanggan Optik Cahaya Murni</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Period ──
    idx = st.selectbox(
        "Pilih Periode Analisis",
        range(len(ALL_YEARS)-1),
        format_func=lambda x: f"{ALL_YEARS[x]}  →  {ALL_YEARS[x+1]}",
        index=len(ALL_YEARS)-2,
    )
    t1, t2 = ALL_YEARS[idx], ALL_YEARS[idx+1]

    d1 = df[df["TAHUN"] == t1][["NAMA","Label"]]
    d2 = df[df["TAHUN"] == t2][["NAMA","Label"]]
    merge  = pd.merge(d1, d2, on="NAMA", how="outer", suffixes=(f"_{t1}",f"_{t2}"))
    baru   = merge[merge[f"Label_{t1}"].isna()]
    churn  = merge[merge[f"Label_{t2}"].isna()]
    migrasi = merge.dropna()

    total     = len(merge)
    churn_rate = len(churn) / total * 100 if total else 0
    baru_rate  = len(baru)  / total * 100 if total else 0

    # ── KPI ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Churn Rate", f"{churn_rate:.1f}%", delta=f"-{len(churn)} pelanggan", delta_color="inverse")
    c2.metric("New Customer Rate", f"{baru_rate:.1f}%", delta=f"+{len(baru)} pelanggan")
    c3.metric("Pelanggan Konsisten", len(migrasi))
    net = len(baru) - len(churn)
    c4.metric("Net Growth", net, delta="positif" if net >= 0 else "negatif",
              delta_color="normal" if net >= 0 else "inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Kondisi bisnis ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏥 Kondisi Bisnis</div>', unsafe_allow_html=True)

    if churn_rate > baru_rate:
        st.markdown(f"""
        <div class="alert-red">
        ⚠️ <b>Perhatian — Churn lebih tinggi dari akuisisi pelanggan baru.</b><br>
        Sebanyak {len(churn)} pelanggan tidak kembali bertransaksi pada periode {t2}. Ini mengindikasikan
        adanya masalah pada retensi dan kepuasan pelanggan yang perlu segera ditangani.
        </div>""", unsafe_allow_html=True)
    elif baru_rate > churn_rate:
        st.markdown(f"""
        <div class="alert-green">
        ✅ <b>Pertumbuhan Positif — Pelanggan baru lebih banyak dari churn.</b><br>
        Sebanyak {len(baru)} pelanggan baru bergabung pada periode {t2}, melebihi {len(churn)} pelanggan
        yang churn. Bisnis sedang berkembang, pertahankan momentum ini.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-blue">
        📊 <b>Kondisi Stabil — Pertumbuhan stagnan.</b><br>
        Jumlah pelanggan baru dan churn seimbang. Perlu optimasi strategi untuk mendorong pertumbuhan lebih lanjut.
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Grafik baru vs churn semua periode ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 New Customer vs Churn — Semua Periode</div>', unsafe_allow_html=True)

    periods, nb_list, nc_list = [], [], []
    for i in range(len(ALL_YEARS)-1):
        ta, tb = ALL_YEARS[i], ALL_YEARS[i+1]
        da = df[df["TAHUN"]==ta][["NAMA","Label"]]
        db = df[df["TAHUN"]==tb][["NAMA","Label"]]
        m  = pd.merge(da, db, on="NAMA", how="outer", suffixes=("_a","_b"))
        periods.append(f"{ta}→{tb}")
        nb_list.append(m["Label_a"].isna().sum())
        nc_list.append(m["Label_b"].isna().sum())

    x = np.arange(len(periods))
    w = 0.35
    fig, ax = plt.subplots(figsize=(9, 3))
    b1 = ax.bar(x - w/2, nb_list, w, label="Pelanggan Baru", color="#22C55E", alpha=0.85, zorder=3)
    b2 = ax.bar(x + w/2, nc_list, w, label="Churn",          color="#F43F5E", alpha=0.85, zorder=3)
    for bar in list(b1)+list(b2):
        h = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, h+0.2, str(int(h)),
                ha="center", fontsize=9, fontweight="700", color="#1A1F5E")
    apply_mpl_theme(ax, ylabel="Jumlah Pelanggan")
    ax.set_xticks(x); ax.set_xticklabels(periods, fontsize=9)
    ax.legend(fontsize=9, framealpha=0)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Strategi per segmen ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">🎯 Strategi Berdasarkan Segmen Pelanggan — Tahun {t2}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">Rekomendasi aksi berdasarkan komposisi segmen pelanggan pada tahun {t2} (tahun tujuan periode yang dipilih)</div>', unsafe_allow_html=True)

    # Ambil data SESUAI tahun t2 dari periode yang dipilih user
    selected_data = df[df["TAHUN"] == t2]
    seg_counts    = selected_data["Label"].value_counts().reindex(ALL_LABELS, fill_value=0)
    # Hanya tampilkan segmen yang benar-benar ada (jumlah > 0) di tahun t2
    active_labels = [lbl for lbl in ALL_LABELS if seg_counts.get(lbl, 0) > 0]

    strategies = {
        "Loyal": {
            "class": "strat-loyal",
            "emoji": "⭐",
            "deskripsi": "Pelanggan aktif dengan frekuensi dan nilai transaksi tinggi. Aset terpenting bisnis.",
            "aksi": [
                "Berikan reward eksklusif (voucher Rp50.000 atau diskon lensa premium)",
                "Prioritaskan layanan — antrian lebih cepat, konsultasi langsung",
                "Upselling produk premium (anti-reflective, blue light filter, progressive lens)",
                "Kirim ucapan ulang tahun + promo spesial via WhatsApp",
            ],
            "target": "Pertahankan & tingkatkan nilai transaksi",
        },
        "Potensial": {
            "class": "strat-potensial",
            "emoji": "🚀",
            "deskripsi": "Pelanggan yang mulai aktif namun belum konsisten bertransaksi. Paling mudah dikonversi menjadi Loyal.",
            "aksi": [
                "Promo personal via WhatsApp berdasarkan riwayat pembelian",
                "Dorong pembelian ulang dalam 1–2 bulan dengan penawaran waktu terbatas",
                "Tawarkan membership ringan dengan benefit kecil (diskon kontrol mata gratis)",
                "Follow-up setelah kunjungan: tanyakan kepuasan dan tawarkan kontrol gratis",
            ],
            "target": "Konversi ke segmen Loyal dalam 1–2 periode",
        },
        "Baru": {
            "class": "strat-baru",
            "emoji": "🌱",
            "deskripsi": "Pelanggan baru yang baru pertama kali bertransaksi. Kesan pertama sangat menentukan loyalitas.",
            "aksi": [
                "Edukasi produk: jelaskan perbedaan jenis lensa (anti radiasi, blue light, progressive)",
                "Follow-up 3–5 hari setelah pembelian pertama via WhatsApp",
                "Berikan voucher diskon 10% untuk kunjungan kedua",
                "Ajak bergabung ke grup komunitas pelanggan Optik Cahaya Murni",
            ],
            "target": "Bangun loyalitas sejak dini & dorong kunjungan kedua",
        },
        "Pasif": {
            "class": "strat-pasif",
            "emoji": "😴",
            "deskripsi": "Pelanggan dengan transaksi rendah dan jarang kembali. Perlu reaktivasi sebelum benar-benar churn.",
            "aksi": [
                "Kampanye reaktivasi: 'Kami rindu! Diskon 15% khusus untuk kunjungan bulan ini'",
                "Reminder kontrol mata rutin via WhatsApp setiap 6 bulan",
                "Paket bundling hemat: frame + lensa + pemeriksaan mata dengan harga spesial",
                "Survei singkat 2 pertanyaan: cari tahu mengapa mereka tidak kembali",
            ],
            "target": "Reaktivasi & cegah churn permanen",
        },
    }

    if not active_labels:
        st.info(f"Tidak ada data segmen untuk tahun {t2}.")
    else:
        for lbl in active_labels:
            info = strategies[lbl]
            cnt  = int(seg_counts.get(lbl, 0))
            st.markdown(f"""
            <div class="strat-card {info['class']}">
                <div class="strat-title">{info['emoji']} Segmen {lbl}
                    <span style="font-weight:400;font-size:0.85rem;opacity:0.65;">
                        — {cnt} pelanggan di tahun {t2}
                    </span>
                </div>
                <div style="font-size:0.85rem; margin-bottom:10px;">{info['deskripsi']}</div>
                <div style="font-size:0.82rem;">
                    <b>Langkah Aksi:</b>
                    <ul style="margin:6px 0 8px 0; padding-left:18px; line-height:1.9;">
                        {''.join(f"<li>{a}</li>" for a in info['aksi'])}
                    </ul>
                    <b>Target:</b> {info['target']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)