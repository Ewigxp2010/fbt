# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# =========================
# 语言包
# =========================

LANG = {
    "en": {
        "title": "FBT Cost & Profit Simulator",
        "subtitle": "Business version – for client-facing usage",
        "orders": "Monthly Orders",
        "aov": "AOV (€)",
        "return_rate": "Return Rate",
        "fbt_cost": "FBT Cost / Order",
        "current_cost": "Current Cost / Order",
        "fixed_cost": "Current Fixed Cost",
        "decision": "Decision",
        "use_fbt": "Use FBT",
        "not_yet": "Not Recommended Yet",
        "monthly_saving": "Monthly Saving",
        "per_order": "Saving / Order",
        "annual": "Annual Impact",
        "fbt_total": "FBT Cost",
        "current_total": "Current Cost",
        "profit_uplift": "Profit Uplift",
        "summary": "Executive Summary",
        "cost_curve": "Cost Curve",
        "total_cost": "Total Cost",
        "profit_compare": "Profit Comparison",
        "summary_text": lambda s, p, a: f"""
We recommend adopting **FBT**.

- Monthly saving: **€{s:,.0f}**
- Saving per order: **€{p:.2f}**
- Annual impact: **€{a:,.0f}**

⚠️ Profit uplift is driven purely by cost reduction.
"""
    },
    "de": {
        "title": "FBT Kosten- & Gewinn-Simulator",
        "subtitle": "Business-Version – geeignet für Kundengespräche",
        "orders": "Monatliche Bestellungen",
        "aov": "Durchschnittlicher Warenkorb (€)",
        "return_rate": "Rückgabequote",
        "fbt_cost": "FBT Kosten / Bestellung",
        "current_cost": "Aktuelle Kosten / Bestellung",
        "fixed_cost": "Fixkosten aktuell",
        "decision": "Empfehlung",
        "use_fbt": "FBT verwenden",
        "not_yet": "Noch nicht empfohlen",
        "monthly_saving": "Monatliche Einsparung",
        "per_order": "Einsparung pro Bestellung",
        "annual": "Jährlicher Effekt",
        "fbt_total": "FBT Kosten",
        "current_total": "Aktuelle Kosten",
        "profit_uplift": "Gewinnsteigerung",
        "summary": "Management Summary",
        "cost_curve": "Kostenkurve",
        "total_cost": "Gesamtkosten",
        "profit_compare": "Gewinnvergleich",
        "summary_text": lambda s, p, a: f"""
Wir empfehlen die Nutzung von **FBT**.

- Monatliche Einsparung: **€{s:,.0f}**
- Einsparung pro Bestellung: **€{p:.2f}**
- Jährlicher Effekt: **€{a:,.0f}**

⚠️ Gewinnsteigerung basiert ausschließlich auf Kostensenkung.
"""
    }
}

# =========================
# 语言选择
# =========================

lang_key = st.selectbox("Language", ["en", "de"])
lang = LANG[lang_key]

st.title(lang["title"])
st.caption(lang["subtitle"])

# =========================
# 输入区
# =========================

c1, c2, c3 = st.columns(3)

with c1:
    orders = st.number_input(lang["orders"], value=3000)
    aov = st.number_input(lang["aov"], value=30.0)
    return_rate = st.number_input(lang["return_rate"], value=0.05)

with c2:
    fbt_cost = st.number_input(lang["fbt_cost"], value=1.6)
    current_cost = st.number_input(lang["current_cost"], value=3.2)

with c3:
    fixed_cost = st.number_input(lang["fixed_cost"], value=2500)

# =========================
# 计算
# =========================

revenue = orders * aov

fbt_total = orders * fbt_cost
current_total = orders * current_cost + fixed_cost

savings = current_total - fbt_total
per_order = savings / orders if orders else 0
annual = savings * 12

profit_fbt = revenue - fbt_total
profit_current = revenue - current_total

# =========================
# KPI
# =========================

st.markdown("## Key Metrics")

k1, k2, k3, k4 = st.columns(4)

k1.metric(lang["decision"], "✅ "+lang["use_fbt"] if savings > 0 else "❌ "+lang["not_yet"])
k2.metric(lang["monthly_saving"], f"€ {savings:,.0f}")
k3.metric(lang["per_order"], f"€ {per_order:.2f}")
k4.metric(lang["annual"], f"€ {annual:,.0f}")

k5, k6, k7 = st.columns(3)

k5.metric(lang["fbt_total"], f"€ {fbt_total:,.0f}")
k6.metric(lang["current_total"], f"€ {current_total:,.0f}")
k7.metric(lang["profit_uplift"], f"€ {savings:,.0f}")

# =========================
# Summary
# =========================

st.markdown(f"## {lang['summary']}")
st.info(lang["summary_text"](savings, per_order, annual))

# =========================
# 图1
# =========================

order_range = np.linspace(500, orders*2, 20)

fig1, ax = plt.subplots(figsize=(7,3))
ax.plot(order_range, order_range*fbt_cost, label="FBT")
ax.plot(order_range, order_range*current_cost+fixed_cost, label="Current")

ax.set_title(lang["cost_curve"])
ax.legend()
st.pyplot(fig1, use_container_width=True)

# =========================
# 图2 + 图3
# =========================

col1, col2 = st.columns(2)

with col1:
    fig2, ax2 = plt.subplots()
    ax2.bar(["FBT", "Current"], [fbt_total, current_total])
    ax2.set_title(lang["total_cost"])
    st.pyplot(fig2, use_container_width=True)

with col2:
    fig3, ax3 = plt.subplots()
    ax3.bar(["FBT Profit", "Current Profit"], [profit_fbt, profit_current])
    ax3.set_title(lang["profit_compare"])
    st.pyplot(fig3, use_container_width=True)
