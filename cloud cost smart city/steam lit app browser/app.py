"""
Cloud Cost Intelligence Platform for Smart City
================================================
Streamlit Web App — converted from Jupyter Notebook
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import io

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cloud Cost Intelligence Platform",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1B3A6B 0%, #2E6DA4 100%);
        padding: 28px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
        text-align: center;
    }
    .main-header h1 { color: white; font-size: 2em; margin: 0; }
    .main-header p  { color: #B3D4F5; margin: 6px 0 0 0; font-size: 1em; }

    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 18px 20px;
        border-left: 5px solid #2E6DA4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 8px;
    }
    .kpi-label { color: #666; font-size: 0.85em; font-weight: 600; text-transform: uppercase; }
    .kpi-value { color: #1B3A6B; font-size: 1.8em; font-weight: 700; margin: 4px 0; }
    .kpi-sub   { color: #888; font-size: 0.8em; }

    .section-header {
        background: #F0F4F8;
        border-left: 4px solid #2E6DA4;
        padding: 10px 16px;
        border-radius: 0 8px 8px 0;
        margin: 24px 0 16px 0;
        font-weight: 700;
        color: #1B3A6B;
        font-size: 1.05em;
    }
    .insight-box {
        background: #EBF5FB;
        border: 1px solid #AED6F1;
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 10px;
    }
    .rec-box {
        background: #FDFEFE;
        border: 1px solid #D5D8DC;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 6px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Color Palette ─────────────────────────────────────────────────────────────
SERVICE_COLORS = {
    "Compute":       "#1565C0",
    "AI/ML Services":"#C62828",
    "Database":      "#F57F17",
    "Networking":    "#6A1B9A",
    "Storage":       "#2E7D32",
}
DEPT_COLORS = ["#1565C0","#C62828","#F57F17","#6A1B9A","#2E7D32","#00838F"]
MONTH_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

# ── Sample Data (mirrors your notebook's smart_city_billing.csv) ──────────────
@st.cache_data
def get_sample_data():
    rows = [
        ("INV-001","January","Compute","Traffic Management",720,1800.00),
        ("INV-002","January","AI/ML Services","Smart Transit",480,1440.00),
        ("INV-003","January","Database","Water Utilities",200,400.00),
        ("INV-004","January","Networking","Smart Grid",150,225.00),
        ("INV-005","January","Storage","Public Safety",90,72.00),
        ("INV-006","February","Compute","Traffic Management",700,1750.00),
        ("INV-007","February","AI/ML Services","Smart Transit",460,1380.00),
        ("INV-008","February","Database","Water Utilities",190,380.00),
        ("INV-009","February","Networking","Smart Grid",140,210.00),
        ("INV-010","February","Storage","Public Safety",95,76.00),
        ("INV-011","March","Compute","Traffic Management",740,1850.00),
        ("INV-012","March","AI/ML Services","Smart Transit",500,1500.00),
        ("INV-013","March","Database","Water Utilities",210,420.00),
        ("INV-014","March","Networking","Smart Grid",160,240.00),
        ("INV-015","March","Storage","Public Safety",100,80.00),
        ("INV-016","April","Compute","Traffic Management",760,1900.00),
        ("INV-017","April","AI/ML Services","Emergency Services",510,1530.00),
        ("INV-018","April","Database","Water Utilities",220,440.00),
        ("INV-019","April","Networking","Smart Grid",170,255.00),
        ("INV-020","April","Storage","Public Safety",105,84.00),
        ("INV-021","May","Compute","Traffic Management",750,1875.00),
        ("INV-022","May","AI/ML Services","Emergency Services",490,1470.00),
        ("INV-023","May","Database","Water Utilities",215,430.00),
        ("INV-024","May","Networking","Smart Grid",165,247.50),
        ("INV-025","May","Storage","Public Safety",110,88.00),
        ("INV-026","June","Compute","Traffic Management",760,1900.00),
        ("INV-027","June","AI/ML Services","Emergency Services",500,1500.00),
        ("INV-028","June","Database","Water Utilities",230,460.00),
        ("INV-029","June","Networking","Smart Grid",175,262.50),
        ("INV-030","June","Storage","Public Safety",115,92.00),
        ("INV-031","July","Compute","Traffic Management",780,1950.00),
        ("INV-032","July","AI/ML Services","Smart Transit",520,1560.00),
        ("INV-033","July","Database","Water Utilities",240,480.00),
        ("INV-034","July","Networking","Smart Grid",180,270.00),
        ("INV-035","July","Storage","Public Safety",120,96.00),
        ("INV-036","August","Compute","Traffic Management",790,1975.00),
        ("INV-037","August","AI/ML Services","Smart Transit",530,1590.00),
        ("INV-038","August","Database","Water Utilities",250,500.00),
        ("INV-039","August","Networking","Smart Grid",185,277.50),
        ("INV-040","August","Storage","Public Safety",125,100.00),
        ("INV-041","September","Compute","Traffic Management",770,1925.00),
        ("INV-042","September","AI/ML Services","Emergency Services",515,1545.00),
        ("INV-043","September","Database","Water Utilities",245,490.00),
        ("INV-044","September","Networking","Smart Grid",182,273.00),
        ("INV-045","September","Storage","Public Safety",122,97.60),
        ("INV-046","October","Compute","Traffic Management",800,2000.00),
        ("INV-047","October","AI/ML Services","Emergency Services",540,1620.00),
        ("INV-048","October","Database","Water Utilities",260,520.00),
        ("INV-049","October","Networking","Smart Grid",190,285.00),
        ("INV-050","October","Storage","Public Safety",130,104.00),
        ("INV-051","November","Compute","Traffic Management",810,2025.00),
        ("INV-052","November","AI/ML Services","Smart Transit",550,1650.00),
        ("INV-053","November","Database","Water Utilities",270,540.00),
        ("INV-054","November","Networking","Smart Grid",195,292.50),
        ("INV-055","November","Storage","Public Safety",135,108.00),
        ("INV-056","December","Compute","Traffic Management",820,2050.00),
        ("INV-057","December","AI/ML Services","Smart Transit",560,1680.00),
        ("INV-058","December","Database","Water Utilities",280,560.00),
        ("INV-059","December","Networking","Smart Grid",200,300.00),
        ("INV-060","December","Storage","Public Safety",140,112.00),
    ]
    df = pd.DataFrame(rows, columns=["Invoice_ID","Month","Service_Type",
                                      "Department","Usage_Hours","Cost_USD"])
    df["Month"] = pd.Categorical(df["Month"], categories=MONTH_ORDER, ordered=True)
    return df

# ── Load Data ─────────────────────────────────────────────────────────────────
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df["Month"] = pd.Categorical(
            df["Month"],
            categories=[m for m in MONTH_ORDER if m in df["Month"].unique()],
            ordered=True
        )
        return df
    return get_sample_data()

# ── Chart helpers ─────────────────────────────────────────────────────────────
def pie_chart(series, title, colors_map=None):
    fig, ax = plt.subplots(figsize=(6, 5), facecolor="none")
    colors = [colors_map.get(k, "#78909C") for k in series.index] if colors_map \
             else plt.cm.Blues_r(np.linspace(0.3, 0.9, len(series)))
    wedges, _, auto = ax.pie(
        series.values, labels=None, autopct="%1.1f%%",
        colors=colors, startangle=140, pctdistance=0.73,
        wedgeprops=dict(edgecolor="white", linewidth=2.5, width=0.7))
    for at in auto: at.set(fontsize=9, fontweight="bold", color="white")
    ax.legend(wedges, series.index, loc="lower center", ncol=2,
              fontsize=8.5, bbox_to_anchor=(0.5,-0.16), framealpha=0)
    ax.set_title(title, fontsize=12, fontweight="bold", color="#1B3A6B", pad=10)
    return fig

def hbar_chart(series, title, color="#1565C0"):
    fig, ax = plt.subplots(figsize=(7, 4), facecolor="none")
    ax.set_facecolor("#F8FBFE")
    colors = [SERVICE_COLORS.get(s, color) for s in series.index] \
             if all(s in SERVICE_COLORS for s in series.index) \
             else [color] * len(series)
    bars = ax.barh(series.index, series.values, color=colors,
                   edgecolor="white", linewidth=0.8, height=0.62)
    for bar, val in zip(bars, series.values):
        ax.text(bar.get_width() + series.max()*0.01,
                bar.get_y() + bar.get_height()/2,
                f"${val:,.0f}", va="center", fontsize=9, color="#212121")
    ax.invert_yaxis()
    ax.set_title(title, fontsize=12, fontweight="bold", color="#1B3A6B")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"${x:,.0f}"))
    ax.spines[["top","right","left"]].set_visible(False)
    ax.set_xlim(0, series.max() * 1.28)
    plt.tight_layout()
    return fig

def line_chart(series, title):
    fig, ax = plt.subplots(figsize=(10, 4), facecolor="none")
    ax.set_facecolor("#F8FBFE")
    ms = [str(m)[:3] for m in series.index]
    budget = series.mean() * 1.10
    ax.plot(ms, series.values, color="#1565C0", lw=2.5, marker="o",
            markersize=9, markerfacecolor="#F57F17",
            markeredgecolor="white", markeredgewidth=2)
    ax.fill_between(ms, series.values, alpha=0.10, color="#1565C0")
    ax.axhline(budget, color="#C62828", ls="--", lw=1.8,
               label=f"Budget Threshold (${budget:,.0f})")
    for x, y in zip(ms, series.values):
        ax.text(x, y + series.max()*0.02, f"${y:,.0f}",
                ha="center", fontsize=8, color="#1B3A6B")
    ax.set_title(title, fontsize=12, fontweight="bold", color="#1B3A6B")
    ax.set_ylabel("Cost (USD)"); ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"${x:,.0f}"))
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout(); return fig

def stacked_bar(pivot_df, title):
    svc_cols = [c for c in pivot_df.columns]
    ms = [str(m)[:3] for m in pivot_df.index]
    fig, ax = plt.subplots(figsize=(12, 5), facecolor="none")
    ax.set_facecolor("#F8FBFE")
    bottom = np.zeros(len(pivot_df))
    for svc in svc_cols:
        vals = pivot_df[svc].values
        ax.bar(ms, vals, bottom=bottom, label=svc,
               color=SERVICE_COLORS.get(svc,"#78909C"),
               edgecolor="white", linewidth=0.6)
        bottom += vals
    ax.set_title(title, fontsize=12, fontweight="bold", color="#1B3A6B")
    ax.set_ylabel("Cost (USD)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"${x:,.0f}"))
    ax.legend(loc="upper left", ncol=2, fontsize=9, framealpha=0.9)
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout(); return fig

# ─────────────────────────────────────────────────────────────────────────────
#                              APP LAYOUT
# ─────────────────────────────────────────────────────────────────────────────

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🏙️ Cloud Cost Intelligence Platform</h1>
  <p>Smart City · AI, Cloud Computing & DevOps — Project B</p>
  <p style="font-size:0.85em; color:#80BBEA;">Python · Pandas · Matplotlib · Streamlit</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/120px-Jupyter_logo.svg.png",
             width=50)
    st.markdown("### ⚙️ Controls")

    uploaded = st.file_uploader(
        "📂 Upload your CSV file",
        type=["csv"],
        help="Upload smart_city_billing.csv or use the built-in sample data"
    )

    st.markdown("---")
    df_full = load_data(uploaded)

    all_months = list(df_full["Month"].cat.categories)
    sel_months = st.multiselect("📅 Filter by Month", all_months,
                                default=all_months)

    all_services = sorted(df_full["Service_Type"].unique())
    sel_services = st.multiselect("🔧 Filter by Service Type", all_services,
                                  default=all_services)

    all_depts = sorted(df_full["Department"].unique())
    sel_depts = st.multiselect("🏛 Filter by Department", all_depts,
                               default=all_depts)

    st.markdown("---")
    show_raw = st.checkbox("📋 Show Raw Data Table", value=False)
    st.markdown("---")
    st.markdown("**📘 About**")
    st.caption("Cloud Cost Intelligence Platform\nSmart City Project B\nPython 3 · Pandas · Streamlit")

# ── Apply Filters ─────────────────────────────────────────────────────────────
df = df_full[
    df_full["Month"].isin(sel_months) &
    df_full["Service_Type"].isin(sel_services) &
    df_full["Department"].isin(sel_depts)
]

if df.empty:
    st.warning("⚠️ No data matches your filters. Please adjust the sidebar selections.")
    st.stop()

# ── Aggregations (mirrors your notebook exactly) ───────────────────────────────
service_cost = df.groupby("Service_Type")["Cost_USD"].sum().sort_values(ascending=False)
monthly_cost = df.groupby("Month", observed=True)["Cost_USD"].sum()
dept_cost    = df.groupby("Department")["Cost_USD"].sum().sort_values(ascending=False)
pivot = df.pivot_table(values="Cost_USD", index="Month",
                       columns="Service_Type", aggfunc="sum",
                       observed=True).fillna(0)

total_spend      = df["Cost_USD"].sum()
avg_monthly      = monthly_cost.mean()
top_service      = service_cost.idxmax()
top_service_cost = service_cost.max()
top_dept         = dept_cost.idxmax()
peak_month       = monthly_cost.idxmax()
budget_limit     = monthly_cost.mean() * 1.10
over_budget_ct   = int((monthly_cost > budget_limit).sum())

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Key Performance Indicators</div>',
            unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">💰 Total Cloud Spend</div>
        <div class="kpi-value">${total_spend:,.0f}</div>
        <div class="kpi-sub">Selected period</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="kpi-card" style="border-left-color:#C62828;">
        <div class="kpi-label">📅 Avg Monthly Spend</div>
        <div class="kpi-value">${avg_monthly:,.0f}</div>
        <div class="kpi-sub">Across selected months</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="kpi-card" style="border-left-color:#F57F17;">
        <div class="kpi-label">🏆 Top Service</div>
        <div class="kpi-value" style="font-size:1.2em;">{top_service}</div>
        <div class="kpi-sub">${top_service_cost:,.0f} ({top_service_cost/total_spend*100:.1f}%)</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""<div class="kpi-card" style="border-left-color:#2E7D32;">
        <div class="kpi-label">📌 Peak Month</div>
        <div class="kpi-value" style="font-size:1.2em;">{peak_month}</div>
        <div class="kpi-sub">${monthly_cost[peak_month]:,.0f} spend</div>
    </div>""", unsafe_allow_html=True)

# ── Service Type Analysis ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔧 Cost by Service Type</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    fig = pie_chart(service_cost, "Service Type Cost Distribution", SERVICE_COLORS)
    st.pyplot(fig, use_container_width=True)
with col2:
    fig = hbar_chart(service_cost, "Annual Spend by Service Type (Ranked)")
    st.pyplot(fig, use_container_width=True)

# ── Detailed Table ────────────────────────────────────────────────────────────
with st.expander("📋 Service Type — Detailed Table"):
    svc_df = service_cost.reset_index()
    svc_df.columns = ["Service Type", "Total Cost (USD)"]
    svc_df["% Share"]      = (svc_df["Total Cost (USD)"] / total_spend * 100).round(2)
    svc_df["Avg Monthly"]  = (svc_df["Total Cost (USD)"] / max(len(sel_months),1)).round(2)
    svc_df["Total Cost (USD)"] = svc_df["Total Cost (USD)"].apply(lambda x: f"${x:,.2f}")
    svc_df["Avg Monthly"]      = svc_df["Avg Monthly"].apply(lambda x: f"${x:,.2f}")
    svc_df["% Share"]          = svc_df["% Share"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(svc_df, use_container_width=True, hide_index=True)

# ── Monthly Trend ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📅 Monthly Cloud Spend Trend</div>',
            unsafe_allow_html=True)

fig = line_chart(monthly_cost, "Monthly Cloud Spend vs Budget Threshold")
st.pyplot(fig, use_container_width=True)

col_a, col_b, col_c = st.columns(3)
col_a.metric("📈 Highest Month", str(peak_month),
             f"${monthly_cost[peak_month]:,.0f}")
col_b.metric("📉 Lowest Month", str(monthly_cost.idxmin()),
             f"${monthly_cost.min():,.0f}")
col_c.metric("⚠️ Months Over Budget", f"{over_budget_ct} / {len(monthly_cost)}")

with st.expander("📋 Monthly Trend — Detailed Table"):
    mon_df = monthly_cost.reset_index()
    mon_df.columns = ["Month", "Total Cost (USD)"]
    mon_df["MoM Change"]   = mon_df["Total Cost (USD)"].diff().fillna(0)
    mon_df["MoM Change %"] = mon_df["Total Cost (USD)"].pct_change().fillna(0) * 100
    mon_df["Cumulative"]   = mon_df["Total Cost (USD)"].cumsum()
    mon_df["Status"]       = mon_df["Total Cost (USD)"].apply(
        lambda x: "✅ On Budget" if x <= budget_limit else "⚠️ Over Budget")
    for col in ["Total Cost (USD)", "MoM Change", "Cumulative"]:
        mon_df[col] = mon_df[col].apply(lambda x: f"${x:,.2f}")
    mon_df["MoM Change %"] = mon_df["MoM Change %"].apply(lambda x: f"{x:+.1f}%")
    st.dataframe(mon_df, use_container_width=True, hide_index=True)

# ── Pivot Table + Stacked Bar ──────────────────────────────────────────────────
st.markdown('<div class="section-header">📐 Pivot Table — Monthly × Service Type</div>',
            unsafe_allow_html=True)

fig = stacked_bar(pivot, "Monthly Cloud Spend — Stacked by Service Type")
st.pyplot(fig, use_container_width=True)

with st.expander("📋 Pivot Table — Raw Numbers"):
    pivot_display = pivot.copy()
    pivot_display.index = pivot_display.index.astype(str)
    pivot_display["ROW TOTAL"] = pivot_display.sum(axis=1)
    st.dataframe(pivot_display.style.format("${:,.2f}"), use_container_width=True)

# ── Department Analysis ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🏛 Cost by Department</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns([1.3, 1])
with col1:
    fig = hbar_chart(dept_cost, "Annual Spend by Smart City Department",
                     color="#1565C0")
    st.pyplot(fig, use_container_width=True)
with col2:
    fig = pie_chart(dept_cost, "Department Cost Distribution")
    st.pyplot(fig, use_container_width=True)

# ── Raw Data ───────────────────────────────────────────────────────────────────
if show_raw:
    st.markdown('<div class="section-header">📋 Raw Billing Data</div>',
                unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(df)} records")

# ── Excel Export ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📤 Export to Excel</div>',
            unsafe_allow_html=True)

def to_excel_bytes(df, service_cost, monthly_cost, dept_cost, pivot):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Raw Billing Data", index=False)

        svc = service_cost.reset_index()
        svc.columns = ["Service Type", "Total Cost (USD)"]
        svc["% Share"] = (svc["Total Cost (USD)"] / svc["Total Cost (USD)"].sum() * 100).round(2)
        svc.to_excel(writer, sheet_name="By Service Type", index=False)

        mon = monthly_cost.reset_index()
        mon.columns = ["Month", "Total Cost (USD)"]
        mon.to_excel(writer, sheet_name="By Month", index=False)

        dep = dept_cost.reset_index()
        dep.columns = ["Department", "Total Cost (USD)"]
        dep.to_excel(writer, sheet_name="By Department", index=False)

        pivot.to_excel(writer, sheet_name="Monthly x Service Pivot")
    buf.seek(0)
    return buf.read()

excel_bytes = to_excel_bytes(df, service_cost, monthly_cost, dept_cost, pivot)
st.download_button(
    label="⬇️ Download Excel Report (.xlsx)",
    data=excel_bytes,
    file_name="smart_city_cloud_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# ── Insights & Recommendations ─────────────────────────────────────────────────
st.markdown('<div class="section-header">🧠 Key Insights & Recommendations</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""<div class="insight-box">
        <b>📊 Cost Intelligence Summary</b><br><br>
        💵 <b>Total Cloud Spend:</b> ${total_spend:,.2f}<br>
        📅 <b>Average Monthly:</b> ${avg_monthly:,.2f}<br>
        🔴 <b>Highest Cost Service:</b> {top_service} (${top_service_cost:,.2f}, {top_service_cost/total_spend*100:.1f}%)<br>
        🏢 <b>Highest Spending Dept:</b> {top_dept}<br>
        📈 <b>Peak Spending Month:</b> {peak_month} (${monthly_cost[peak_month]:,.2f})<br>
        ⚠️ <b>Over-Budget Months:</b> {over_budget_ct} of {len(monthly_cost)}
    </div>""", unsafe_allow_html=True)

with col2:
    recs = [
        ("🤖 AI/ML Services", "Largest cost driver. Consider reserved instances or spot pricing to reduce by 30–40%."),
        ("💻 Compute", "Costs are high and growing. Implement auto-scaling policies and right-sizing."),
        ("💾 Storage", "Well optimized. Continue current tiered storage strategy."),
        ("🏛 Traffic Mgmt", "Largest departmental spender. Review VM count and usage hours."),
        ("📅 Budget Alerts", f"Set cloud alerts at 80% & 100% of ${budget_limit:,.0f}/month."),
    ]
    st.markdown("**💡 Recommendations**")
    for title, detail in recs:
        st.markdown(f"""<div class="rec-box">
            <b>{title}</b><br>
            <span style="color:#555; font-size:0.9em;">{detail}</span>
        </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:#999; font-size:0.85em;'>"
    "☁️ Cloud Cost Intelligence Platform · Smart City Project B · "
    "Python · Pandas · Matplotlib · Streamlit"
    "</center>",
    unsafe_allow_html=True
)