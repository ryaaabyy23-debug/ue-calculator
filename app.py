import streamlit as st
import plotly.graph_objects as go
import json
import os
from datetime import datetime

st.set_page_config(page_title="Unit Economics", layout="wide", page_icon="🧮")

# ── Colors ────────────────────────────────────────────────────────────────────
BG       = "#0F0F0F"
CARD     = "#1F1F1F"
BORDER   = "#2A2A2A"
INPUT_BG = "#2A2A2A"
TEXT_DIM = "#8A8A8A"
GREEN    = "#D0F3AF"
BLUE     = "#C8E9FA"
PINK     = "#FFC8E4"

st.markdown(f"""
<style>
    .stApp {{ background-color: {BG}; }}
    [data-testid="stSidebar"] {{ background-color: #111111; }}
    section[data-testid="stMain"] {{ background-color: {BG}; }}
    .stNumberInput input {{ background-color: {INPUT_BG} !important; color: white !important; border: 1px solid {BORDER} !important; border-radius: 8px !important; }}
    .stTextInput input {{ background-color: {INPUT_BG} !important; color: white !important; border: 1px solid {BORDER} !important; border-radius: 8px !important; }}
    div[data-testid="stMetric"] {{ background-color: {CARD}; border-radius: 12px; padding: 16px; }}
    .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}
    h1, h2, h3, h4, p, label {{ color: white !important; }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    .card {{ background-color: {CARD}; border-radius: 16px; padding: 20px; margin-bottom: 16px; }}
    .metric-green {{ background-color: {GREEN}22; border: 1px solid {GREEN}44; border-radius: 12px; padding: 16px; }}
    .metric-blue {{ background-color: {BLUE}22; border: 1px solid {BLUE}44; border-radius: 12px; padding: 16px; }}
    .metric-pink {{ background-color: {PINK}22; border: 1px solid {PINK}44; border-radius: 12px; padding: 16px; }}
</style>
""", unsafe_allow_html=True)

DATA_FILE = "scenarios.json"

def load_scenarios():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_scenarios(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def metric_html(label, value, pct, color):
    return f"""
    <div style="background:{color}15;border:1px solid {color}44;border-radius:12px;padding:16px;text-align:left">
        <p style="color:{TEXT_DIM};font-size:11px;margin:0 0 6px 0;text-transform:uppercase;letter-spacing:0.5px">{label}</p>
        <p style="color:{color};font-size:28px;font-weight:700;margin:0 0 6px 0">{value}</p>
        <span style="background:{color}22;color:{color};border-radius:20px;padding:2px 10px;font-size:12px;font-weight:600">↑ {pct}</span>
    </div>
    """

def section(title):
    st.markdown(f"<h3 style='color:white;font-size:16px;font-weight:600;margin:0 0 16px 0'>{title}</h3>", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_actions = st.columns([2, 1])

with col_title:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px">
        <span style="font-size:28px">🧮</span>
        <div>
            <h1 style="color:white;font-size:22px;font-weight:700;margin:0">Unit Economics</h1>
            <p style="color:#8A8A8A;font-size:12px;margin:0">Per order & monthly analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_actions:
    scenarios = load_scenarios()
    col_h, col_s, col_c = st.columns(3)
    with col_h:
        show_history = st.button(f"History {len(scenarios)}", key="history_btn")
    with col_s:
        show_save = st.button("💾 Save", key="save_btn")
    with col_c:
        currency = st.selectbox("", ["$", "€", "£"], label_visibility="collapsed")

st.markdown(f"<hr style='border-color:{BORDER};margin:16px 0'>", unsafe_allow_html=True)

# ── History panel ──────────────────────────────────────────────────────────────
if show_history:
    if not scenarios:
        st.info("No saved scenarios yet.")
    else:
        st.markdown(f"<div style='background:{CARD};border-radius:16px;padding:20px;margin-bottom:20px'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:white;margin:0 0 16px 0'>Saved Scenarios</h4>", unsafe_allow_html=True)
        for s in reversed(scenarios):
            inp = s.get("inputs", {})
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"""
                <div style="background:{INPUT_BG};border-radius:10px;padding:12px 16px;margin-bottom:8px;border:1px solid {BORDER}">
                    <p style="color:white;font-weight:600;margin:0 0 2px 0;font-size:14px">{s['name']}</p>
                    <p style="color:{TEXT_DIM};font-size:12px;margin:0">{s['saved_at']} &nbsp;·&nbsp; AOV: {currency}{inp.get('aov',0)} &nbsp;·&nbsp; Orders: {inp.get('new_orders',0)}</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Save modal ─────────────────────────────────────────────────────────────────
if show_save:
    with st.form("save_form"):
        scenario_name = st.text_input("Scenario name", placeholder="e.g. My Store Q2 2026")
        submitted = st.form_submit_button("Save", type="primary")

# ── Main inputs ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"<div style='background:{CARD};border-radius:16px;padding:20px;margin-bottom:16px'>", unsafe_allow_html=True)
    section("Unit / Order gross margin")
    aov = st.number_input("AOV (average order value)", value=320.0, step=1.0, key="aov")
    st.markdown(f"<p style='color:white;font-weight:600;font-size:13px;margin:8px 0'>Variable costs per order</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        cogs = st.number_input("Landed COGS", value=160.0, step=0.1, key="cogs")
        returns = st.number_input("Returns (cost per order)", value=0.0, step=0.1, key="returns")
        package = st.number_input("Package", value=0.0, step=0.1, key="package")
    with c2:
        processing = st.number_input("Processing (fees)", value=4.0, step=0.01, key="processing")
        tpl = st.number_input("3PL", value=0.0, step=0.1, key="tpl")
        label = st.number_input("Label", value=0.0, step=0.1, key="label")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='background:{CARD};border-radius:16px;padding:20px;margin-bottom:16px'>", unsafe_allow_html=True)
    section("Margins per order")
    ncac = st.number_input("nCAC (marketing per order)", value=75.0, step=1.0, key="ncac")

    total_var = cogs + processing + returns + tpl + package + label
    cm = aov - total_var
    cm_pct = cm / aov * 100 if aov else 0
    ncac_pct = ncac / aov * 100 if aov else 0
    om = cm - ncac
    om_pct = om / aov * 100 if aov else 0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(metric_html("Contribution<br>margin", f"{currency}{cm:,.0f}", f"{cm_pct:.2f}%", PINK), unsafe_allow_html=True)
    with m2:
        st.markdown(metric_html("nCAC", f"{currency}{ncac:,.0f}", f"{ncac_pct:.2f}%", BLUE), unsafe_allow_html=True)
    with m3:
        st.markdown(metric_html("Operating<br>margin", f"{currency}{om:,.0f}", f"{om_pct:.2f}%", GREEN), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='background:{CARD};border-radius:16px;padding:20px;margin-bottom:16px'>", unsafe_allow_html=True)
    section("Cost breakdown per order")
    cost_rows = [("Landed COGS", cogs), ("Returns", returns), ("Package", package),
                 ("Processing", processing), ("3PL", tpl), ("Labels", label)]
    table_html = f"""
    <table style="width:100%;border-collapse:collapse">
        <thead><tr>
            <th style="color:{TEXT_DIM};padding:6px 12px;text-align:left;font-size:12px;font-weight:500">Name</th>
            <th style="color:{TEXT_DIM};padding:6px 12px;text-align:right;font-size:12px;font-weight:500">Amount</th>
            <th style="color:{TEXT_DIM};padding:6px 12px;text-align:right;font-size:12px;font-weight:500">% of AOV</th>
        </tr></thead><tbody>
    """
    for name, val in cost_rows:
        pct_aov = val / aov * 100 if aov else 0
        table_html += f"""
        <tr style="border-top:1px solid {BORDER}">
            <td style="color:white;padding:8px 12px;font-size:13px">{name}</td>
            <td style="color:white;padding:8px 12px;text-align:right;font-size:13px">{currency}{val:.2f}</td>
            <td style="color:{TEXT_DIM};padding:8px 12px;text-align:right;font-size:13px">{pct_aov:.2f}%</td>
        </tr>"""
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown(f"<div style='background:{CARD};border-radius:16px;padding:20px;margin-bottom:16px'>", unsafe_allow_html=True)
    section("Monthly view (orders)")
    new_orders = st.number_input("New orders", value=135, step=1, key="new_orders")
    returning_orders = st.number_input("Returning orders", value=10, step=1, key="returning_orders")
    total_orders = new_orders + returning_orders
    ret_share = returning_orders / total_orders * 100 if total_orders else 0
    o1, o2 = st.columns(2)
    with o1:
        st.markdown(f"<div style='background:{INPUT_BG};border-radius:10px;padding:12px 16px'><p style='color:{TEXT_DIM};font-size:12px;margin:0 0 2px 0'>Total orders</p><p style='color:white;font-size:24px;font-weight:700;margin:0'>{total_orders:,}</p></div>", unsafe_allow_html=True)
    with o2:
        st.markdown(f"<div style='background:{INPUT_BG};border-radius:10px;padding:12px 16px'><p style='color:{TEXT_DIM};font-size:12px;margin:0 0 2px 0'>Returning share</p><p style='color:white;font-size:24px;font-weight:700;margin:0'>{ret_share:.2f}%</p></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='background:{CARD};border-radius:16px;padding:20px;margin-bottom:16px'>", unsafe_allow_html=True)
    section("Contribution margin (monthly)")
    revenue_m = aov * total_orders
    cm_rows = [("Revenue", revenue_m), ("COGS", cogs * total_orders),
               ("Returns", returns * total_orders), ("Processing", processing * total_orders),
               ("Package", package * total_orders), ("3PL", tpl * total_orders),
               ("Labels", label * total_orders), ("Contribution", cm * total_orders)]
    cm_table = f"<table style='width:100%;border-collapse:collapse'><thead><tr><th style='color:{TEXT_DIM};padding:6px 12px;text-align:left;font-size:12px'>Name</th><th style='color:{TEXT_DIM};padding:6px 12px;text-align:right;font-size:12px'>Amount</th></tr></thead><tbody>"
    for name, val in cm_rows:
        color = GREEN if name == "Contribution" else "white"
        weight = "700" if name == "Contribution" else "normal"
        cm_table += f"<tr style='border-top:1px solid {BORDER}'><td style='color:{color};padding:8px 12px;font-size:13px;font-weight:{weight}'>{name}</td><td style='color:{color};padding:8px 12px;text-align:right;font-size:13px;font-weight:{weight}'>{currency}{val:,.0f}</td></tr>"
    cm_table += "</tbody></table>"
    st.markdown(cm_table, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='background:{CARD};border-radius:16px;padding:20px;margin-bottom:16px'>", unsafe_allow_html=True)
    section("Operating margin (monthly)")
    marketing = st.number_input("Marketing spend (monthly)", value=10000.0, step=100.0)
    warehouse = st.number_input("Warehouse", value=0.0, step=100.0)
    payroll = st.number_input("Payroll", value=1000.0, step=100.0)
    software = st.number_input("Software", value=500.0, step=100.0)
    content_misc = st.number_input("Content", value=620.0, step=100.0)
    st.markdown("</div>", unsafe_allow_html=True)

    fixed = warehouse + payroll + software + content_misc
    op_profit = cm * total_orders - marketing - fixed
    op_pct = op_profit / revenue_m * 100 if revenue_m else 0
    op_color = GREEN if op_pct > 10 else "#F5A623" if op_pct > 0 else "#FF4D4D"

    st.markdown(f"""
    <div style='background:{CARD};border-radius:16px;padding:20px;margin-bottom:16px'>
        <p style='color:{TEXT_DIM};font-size:13px;margin:0 0 8px 0'>Operating profit (monthly)</p>
        <p style='color:{op_color};font-size:36px;font-weight:700;margin:0 0 6px 0'>{currency}{op_profit:,.0f}</p>
        <span style='background:{op_color}22;color:{op_color};border-radius:20px;padding:2px 10px;font-size:13px;font-weight:600'>↑ {op_pct:.2f}%</span>
    </div>
    """, unsafe_allow_html=True)

# ── Forecast ───────────────────────────────────────────────────────────────────
st.markdown(f"<div style='background:{CARD};border-radius:16px;padding:20px;margin-top:8px'>", unsafe_allow_html=True)
section("📈 Forecast")
fc1, fc2 = st.columns([3, 1])
with fc1:
    forecast_months = st.slider("Months to forecast", 1, 12, 6)
with fc2:
    growth_rate = st.number_input("Order growth % / month", value=10, step=1)

growth = growth_rate / 100
cm_unit = cm
labels_f, revenues_f, profits_f, margins_f = [], [], [], []
now = datetime.now()
for i in range(forecast_months):
    m = (now.month + i - 1) % 12 + 1
    y = now.year + (now.month + i - 1) // 12
    labels_f.append(datetime(y, m, 1).strftime("%b %Y"))
    o = int(new_orders * (1 + growth) ** i)
    rev = aov * o
    prof = cm_unit * o - marketing - fixed
    revenues_f.append(rev)
    profits_f.append(prof)
    margins_f.append(prof / rev * 100 if rev else 0)

fig = go.Figure()
fig.add_trace(go.Bar(x=labels_f, y=revenues_f, name="Revenue", marker_color=BLUE, opacity=0.7))
fig.add_trace(go.Bar(x=labels_f, y=profits_f, name="Operating Profit",
                     marker_color=[GREEN if p > 0 else "#FF4D4D" for p in profits_f]))
fig.add_trace(go.Scatter(x=labels_f, y=margins_f, name="Margin %", yaxis="y2",
                         mode="lines+markers", line={"color": PINK, "width": 2}, marker={"size": 6}))
fig.update_layout(
    paper_bgcolor=BG, plot_bgcolor=CARD,
    font={"color": "white", "family": "system-ui"},
    barmode="group", height=320,
    legend={"orientation": "h", "y": -0.2, "font": {"color": "white"}},
    xaxis={"showgrid": False, "linecolor": BORDER},
    yaxis={"showgrid": False, "linecolor": BORDER, "title": f"Amount ({currency})"},
    yaxis2={"overlaying": "y", "side": "right", "showgrid": False, "title": "Margin %", "ticksuffix": "%"},
    margin={"l": 20, "r": 60, "t": 20, "b": 60},
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── Save logic ─────────────────────────────────────────────────────────────────
if show_save and 'submitted' in dir() and submitted and scenario_name:
    scenario = {
        "id": int(datetime.now().timestamp() * 1000),
        "name": scenario_name,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "inputs": {
            "aov": aov, "cogs": cogs, "processing": processing,
            "returns": returns, "tpl": tpl, "package": package,
            "label": label, "ncac": ncac, "new_orders": new_orders,
            "returning_orders": returning_orders, "marketing": marketing,
            "warehouse": warehouse, "payroll": payroll,
            "software": software, "content": content_misc,
        }
    }
    data = load_scenarios()
    data.append(scenario)
    save_scenarios(data)
    st.success(f"✅ Saved: {scenario_name}")
