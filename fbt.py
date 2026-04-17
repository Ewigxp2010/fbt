# -*- coding: utf-8 -*-
# FBT Inventory + Fulfillment Benefit Simulator - Streamlit V2
# Features:
# 1) CN / EN switch
# 2) Sidebar input layout
# 3) Decision / KPI / Profit / Insight
# 4) Break-even estimation
# 5) 3 charts
# 6) Fixed: no hidden widget dependency inside calculation functions

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# =========================================================
# 1. LANGUAGE PACK
# =========================================================

LANG = {
    "en": {
        "title": "FBT Inventory & Fulfillment Benefit Simulator",
        "basic_inputs": "1. Basic Inputs",
        "fbt_inputs": "2. FBT Inputs",
        "current_inputs": "3. Current Solution Inputs",
        "business_inputs": "4. Business Inputs",
        "calculate": "Calculate",
        "reset": "Reset",

        "monthly_orders": "Monthly Orders",
        "avg_items_per_order": "Avg Items per Order",
        "avg_volume_m3_per_item": "Avg Volume per Item (m³)",
        "avg_storage_days": "Avg Storage Days",
        "inventory_coverage_days": "Inventory Coverage Days",
        "return_rate": "Return Rate",
        "avg_order_value": "AOV (€)",

        "share_ge_20": "Share of Orders >= €20",
        "share_lt_20": "Share of Orders < €20",

        "size_xs_share": "XS Share",
        "size_s_share": "S Share",
        "size_m_share": "M Share",
        "size_l_share": "L Share",

        "fbt_storage_cost": "FBT Storage Cost / m³ / day",
        "buyer_shipping_domestic": "Buyer Shipping (Domestic)",
        "buyer_shipping_intra": "Buyer Shipping (Intra-EU)",

        "current_storage_cost": "Current Storage Cost / m³ / day",
        "current_fulfillment_per_order": "Current Fulfillment / order",
        "current_return_processing": "Current Return Processing / order",
        "current_inventory_handling_monthly": "Current Inventory Handling Monthly",
        "current_stock_loss_monthly": "Current Stock Loss / Damage Monthly",
        "current_manpower_monthly": "Current Inventory Manpower Monthly",
        "current_other_fixed_monthly": "Current Other Fixed Monthly Cost",

        "warehouse_country": "Warehouse Country",
        "domestic_share": "Domestic Order Share",
        "intra_eu_share": "Intra-EU Order Share",

        "summary": "SUMMARY",
        "decision": "Decision",
        "recommend_fbt": "✅ Recommend FBT",
        "not_recommend_fbt": "❌ Not Recommended Yet",

        "a_cost": "A. FBT Seller-side Cost",
        "b_cost": "B. Current Solution Cost",
        "c_savings": "C. Seller-side Savings",
        "savings_rate": "Savings Rate",
        "per_order_saving": "Savings per Order",
        "free_shipping_orders": "Free-shipping Eligible Orders (>=€20)",
        "buyer_shipping_saved": "Buyer Shipping Value Saved",

        "monthly_revenue": "Monthly Revenue",
        "fbt_profit": "FBT Profit",
        "current_profit": "Current Profit",
        "profit_uplift": "Profit Uplift",

        "fbt_breakdown": "FBT Breakdown",
        "current_breakdown": "Current Breakdown",

        "chart1": "Cost Curve Comparison",
        "chart2": "Total Comparison",
        "chart3": "Breakdown Comparison",

        "line_fbt": "FBT",
        "line_current": "Current",
        "line_savings": "Savings",

        "x_orders": "Monthly Orders",
        "y_eur": "EUR",

        "storage": "Storage",
        "fulfillment": "Fulfillment",
        "returns": "Returns",
        "handling": "Inventory Handling",
        "stock_loss": "Stock Loss / Damage",
        "manpower": "Manpower",
        "other_fixed": "Other Fixed",

        "sales_insight": "Sales Insight",
        "annual_impact": "Annual Savings Impact",
        "breakeven_found": "Break-even at approximately {orders} orders/month",
        "breakeven_not_found": "No break-even found within the current order range",

        "section_results": "Results",
        "section_profit": "Profit Comparison",
        "section_breakdown": "Cost Breakdown",
    },
    "zh": {
        "title": "FBT 库存与履约收益模拟器",
        "basic_inputs": "1. 基础输入",
        "fbt_inputs": "2. FBT 输入",
        "current_inputs": "3. 客户当前方案输入",
        "business_inputs": "4. 业务输入",
        "calculate": "开始计算",
        "reset": "重置",

        "monthly_orders": "月订单量",
        "avg_items_per_order": "平均每单件数",
        "avg_volume_m3_per_item": "单件平均体积 (m³)",
        "avg_storage_days": "平均仓储天数",
        "inventory_coverage_days": "库存覆盖天数",
        "return_rate": "退货率",
        "avg_order_value": "客单价 AOV (€)",

        "share_ge_20": "订单金额 >=20欧 占比",
        "share_lt_20": "订单金额 <20欧 占比",

        "size_xs_share": "XS 占比",
        "size_s_share": "S 占比",
        "size_m_share": "M 占比",
        "size_l_share": "L 占比",

        "fbt_storage_cost": "FBT 仓储成本 / m³ / 天",
        "buyer_shipping_domestic": "买家运费（Domestic）",
        "buyer_shipping_intra": "买家运费（Intra-EU）",

        "current_storage_cost": "当前仓储成本 / m³ / 天",
        "current_fulfillment_per_order": "当前履约成本 / 单",
        "current_return_processing": "当前退货处理成本 / 单",
        "current_inventory_handling_monthly": "当前库存操作月成本",
        "current_stock_loss_monthly": "当前库损 / 破损月成本",
        "current_manpower_monthly": "当前库存人力月成本",
        "current_other_fixed_monthly": "当前其他固定月成本",

        "warehouse_country": "仓库国家",
        "domestic_share": "Domestic 订单占比",
        "intra_eu_share": "Intra-EU 订单占比",

        "summary": "结果汇总",
        "decision": "建议结论",
        "recommend_fbt": "✅ 推荐使用 FBT",
        "not_recommend_fbt": "❌ 当前暂不推荐 FBT",

        "a_cost": "A. FBT 卖家侧总成本",
        "b_cost": "B. 当前方案总成本",
        "c_savings": "C. 卖家侧节省金额",
        "savings_rate": "节省比例",
        "per_order_saving": "单均节省",
        "free_shipping_orders": "包邮资格订单数 (>=20欧)",
        "buyer_shipping_saved": "买家侧节省运费价值",

        "monthly_revenue": "月销售额",
        "fbt_profit": "FBT 利润",
        "current_profit": "当前方案利润",
        "profit_uplift": "利润提升",

        "fbt_breakdown": "FBT 成本拆分",
        "current_breakdown": "当前方案成本拆分",

        "chart1": "成本曲线对比",
        "chart2": "总额对比",
        "chart3": "成本结构对比",

        "line_fbt": "FBT",
        "line_current": "当前方案",
        "line_savings": "节省金额",

        "x_orders": "月订单量",
        "y_eur": "欧元",

        "storage": "仓储",
        "fulfillment": "履约",
        "returns": "退货",
        "handling": "库存操作",
        "stock_loss": "库损 / 破损",
        "manpower": "人力",
        "other_fixed": "其他固定成本",

        "sales_insight": "销售洞察",
        "annual_impact": "年度节省影响",
        "breakeven_found": "盈亏平衡点约为每月 {orders} 单",
        "breakeven_not_found": "在当前订单范围内未找到盈亏平衡点",

        "section_results": "结果",
        "section_profit": "利润对比",
        "section_breakdown": "成本拆分",
    }
}

# =========================================================
# 2. RATE CARD
# Replace with your actual rate card if needed
# =========================================================

RATE_CARD = {
    "DE": {
        "storage_per_m3_per_day": 0.58,
        "domestic": {
            "XS": 0.80,
            "S": 1.00,
            "M": 1.30,
            "L": 1.80,
        },
        "intra_eu": {
            "XS": 1.04,
            "S": 1.35,
            "M": 1.75,
            "L": 2.40,
        }
    },
    "ES": {
        "storage_per_m3_per_day": 0.58,
        "domestic": {
            "XS": 0.80,
            "S": 1.00,
            "M": 1.30,
            "L": 1.80,
        },
        "intra_eu": {
            "XS": 1.04,
            "S": 1.35,
            "M": 1.75,
            "L": 2.40,
        }
    }
}

# =========================================================
# 3. HELPERS
# =========================================================

def normalize_shares(values):
    total = sum(max(0, v) for v in values)
    if total <= 0:
        return [0 for _ in values]
    return [max(0, v) / total for v in values]


def weighted_fbt_fulfillment_per_order(warehouse, domestic_share, intra_share, xs, s, m, l):
    size_shares = normalize_shares([xs, s, m, l])
    xs, s, m, l = size_shares

    dom_rate = (
        xs * RATE_CARD[warehouse]["domestic"]["XS"] +
        s  * RATE_CARD[warehouse]["domestic"]["S"] +
        m  * RATE_CARD[warehouse]["domestic"]["M"] +
        l  * RATE_CARD[warehouse]["domestic"]["L"]
    )

    intra_rate = (
        xs * RATE_CARD[warehouse]["intra_eu"]["XS"] +
        s  * RATE_CARD[warehouse]["intra_eu"]["S"] +
        m  * RATE_CARD[warehouse]["intra_eu"]["M"] +
        l  * RATE_CARD[warehouse]["intra_eu"]["L"]
    )

    lane_shares = normalize_shares([domestic_share, intra_share])
    domestic_share, intra_share = lane_shares

    weighted = domestic_share * dom_rate + intra_share * intra_rate
    return weighted, dom_rate, intra_rate


# =========================================================
# 4. CORE CALCULATION
# =========================================================

def calculate_fbt_cost(
    monthly_orders,
    avg_items_per_order,
    avg_volume_m3_per_item,
    avg_storage_days,
    inventory_coverage_days,
    return_rate,
    warehouse,
    domestic_share,
    intra_eu_share,
    xs_share,
    s_share,
    m_share,
    l_share,
    share_ge_20,
    share_lt_20,
    buyer_shipping_domestic,
    buyer_shipping_intra,
    lang_pack
):
    total_items_month = monthly_orders * avg_items_per_order
    avg_inventory_items = total_items_month * (inventory_coverage_days / 30.0)
    avg_inventory_volume = avg_inventory_items * avg_volume_m3_per_item

    storage_per_m3_per_day = RATE_CARD[warehouse]["storage_per_m3_per_day"]
    storage_cost = avg_inventory_volume * avg_storage_days * storage_per_m3_per_day

    weighted_fulfillment, dom_f_rate, intra_f_rate = weighted_fbt_fulfillment_per_order(
        warehouse, domestic_share, intra_eu_share, xs_share, s_share, m_share, l_share
    )
    fulfillment_cost = monthly_orders * weighted_fulfillment

    # Simplified assumption: return processing = 50% of fulfillment
    return_cost = monthly_orders * return_rate * weighted_fulfillment * 0.5

    seller_total = storage_cost + fulfillment_cost + return_cost

    lane_shares = normalize_shares([domestic_share, intra_eu_share])
    domestic_share, intra_eu_share = lane_shares

    order_value_shares = normalize_shares([share_ge_20, share_lt_20])
    ge20_share, _ = order_value_shares

    free_shipping_orders = monthly_orders * ge20_share
    avg_buyer_shipping = domestic_share * buyer_shipping_domestic + intra_eu_share * buyer_shipping_intra
    buyer_shipping_saved = free_shipping_orders * avg_buyer_shipping

    breakdown = {
        lang_pack["storage"]: storage_cost,
        lang_pack["fulfillment"]: fulfillment_cost,
        lang_pack["returns"]: return_cost,
    }

    extra = {
        "weighted_fulfillment_per_order": weighted_fulfillment,
        "domestic_fulfillment_avg": dom_f_rate,
        "intra_eu_fulfillment_avg": intra_f_rate,
        "free_shipping_orders": free_shipping_orders,
        "buyer_shipping_saved": buyer_shipping_saved
    }

    return seller_total, breakdown, extra


def calculate_current_cost(
    monthly_orders,
    avg_items_per_order,
    avg_volume_m3_per_item,
    avg_storage_days,
    inventory_coverage_days,
    return_rate,
    current_storage_cost_per_m3_per_day,
    current_fulfillment_per_order,
    current_return_processing_per_order,
    current_inventory_handling_monthly,
    current_stock_loss_monthly,
    current_manpower_monthly,
    current_other_fixed_monthly_cost,
    lang_pack
):
    total_items_month = monthly_orders * avg_items_per_order
    avg_inventory_items = total_items_month * (inventory_coverage_days / 30.0)
    avg_inventory_volume = avg_inventory_items * avg_volume_m3_per_item

    storage_cost = avg_inventory_volume * avg_storage_days * current_storage_cost_per_m3_per_day
    fulfillment_cost = monthly_orders * current_fulfillment_per_order
    return_cost = monthly_orders * return_rate * current_return_processing_per_order

    total = (
        storage_cost +
        fulfillment_cost +
        return_cost +
        current_inventory_handling_monthly +
        current_stock_loss_monthly +
        current_manpower_monthly +
        current_other_fixed_monthly_cost
    )

    breakdown = {
        lang_pack["storage"]: storage_cost,
        lang_pack["fulfillment"]: fulfillment_cost,
        lang_pack["returns"]: return_cost,
        lang_pack["handling"]: current_inventory_handling_monthly,
        lang_pack["stock_loss"]: current_stock_loss_monthly,
        lang_pack["manpower"]: current_manpower_monthly,
        lang_pack["other_fixed"]: current_other_fixed_monthly_cost,
    }

    return total, breakdown


# =========================================================
# 5. PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FBT Simulator",
    layout="wide"
)

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

# =========================================================
# 6. SIDEBAR INPUTS
# =========================================================

with st.sidebar:
    language = st.selectbox(
        "Language / 语言",
        options=["en", "zh"],
        format_func=lambda x: "English" if x == "en" else "中文",
        key=f"language_{st.session_state.reset_counter}"
    )

lang = LANG[language]

st.title(lang["title"])

with st.sidebar:
    st.markdown("---")
    st.subheader(lang["basic_inputs"])

    warehouse = st.selectbox(
        lang["warehouse_country"],
        options=["DE", "ES"],
        key=f"warehouse_{st.session_state.reset_counter}"
    )

    monthly_orders = st.number_input(
        lang["monthly_orders"],
        min_value=0,
        value=3000,
        step=100,
        key=f"monthly_orders_{st.session_state.reset_counter}"
    )

    avg_items_per_order = st.number_input(
        lang["avg_items_per_order"],
        min_value=0.0,
        value=1.0,
        step=0.1,
        format="%.2f",
        key=f"avg_items_per_order_{st.session_state.reset_counter}"
    )

    avg_volume_m3_per_item = st.number_input(
        lang["avg_volume_m3_per_item"],
        min_value=0.0,
        value=0.01,
        step=0.001,
        format="%.4f",
        key=f"avg_volume_{st.session_state.reset_counter}"
    )

    avg_storage_days = st.number_input(
        lang["avg_storage_days"],
        min_value=0,
        value=30,
        step=1,
        key=f"avg_storage_days_{st.session_state.reset_counter}"
    )

    inventory_coverage_days = st.number_input(
        lang["inventory_coverage_days"],
        min_value=0,
        value=30,
        step=1,
        key=f"inventory_coverage_days_{st.session_state.reset_counter}"
    )

    return_rate = st.number_input(
        lang["return_rate"],
        min_value=0.0,
        value=0.05,
        step=0.01,
        format="%.4f",
        key=f"return_rate_{st.session_state.reset_counter}"
    )

    avg_order_value = st.number_input(
        lang["avg_order_value"],
        min_value=0.0,
        value=30.0,
        step=1.0,
        format="%.2f",
        key=f"aov_{st.session_state.reset_counter}"
    )

    domestic_share = st.number_input(
        lang["domestic_share"],
        min_value=0.0,
        value=0.6,
        step=0.05,
        format="%.4f",
        key=f"domestic_share_{st.session_state.reset_counter}"
    )

    intra_eu_share = st.number_input(
        lang["intra_eu_share"],
        min_value=0.0,
        value=0.4,
        step=0.05,
        format="%.4f",
        key=f"intra_eu_share_{st.session_state.reset_counter}"
    )

    share_ge_20 = st.number_input(
        lang["share_ge_20"],
        min_value=0.0,
        value=0.6,
        step=0.05,
        format="%.4f",
        key=f"share_ge_20_{st.session_state.reset_counter}"
    )

    share_lt_20 = st.number_input(
        lang["share_lt_20"],
        min_value=0.0,
        value=0.4,
        step=0.05,
        format="%.4f",
        key=f"share_lt_20_{st.session_state.reset_counter}"
    )

    size_xs_share = st.number_input(
        lang["size_xs_share"],
        min_value=0.0,
        value=0.25,
        step=0.05,
        format="%.4f",
        key=f"size_xs_share_{st.session_state.reset_counter}"
    )

    size_s_share = st.number_input(
        lang["size_s_share"],
        min_value=0.0,
        value=0.25,
        step=0.05,
        format="%.4f",
        key=f"size_s_share_{st.session_state.reset_counter}"
    )

    size_m_share = st.number_input(
        lang["size_m_share"],
        min_value=0.0,
        value=0.25,
        step=0.05,
        format="%.4f",
        key=f"size_m_share_{st.session_state.reset_counter}"
    )

    size_l_share = st.number_input(
        lang["size_l_share"],
        min_value=0.0,
        value=0.25,
        step=0.05,
        format="%.4f",
        key=f"size_l_share_{st.session_state.reset_counter}"
    )

    st.markdown("---")
    st.subheader(lang["fbt_inputs"])

    st.number_input(
        lang["fbt_storage_cost"],
        value=float(RATE_CARD[warehouse]["storage_per_m3_per_day"]),
        disabled=True,
        key=f"fbt_storage_cost_display_{st.session_state.reset_counter}"
    )

    buyer_shipping_domestic = st.number_input(
        lang["buyer_shipping_domestic"],
        min_value=0.0,
        value=4.99,
        step=0.1,
        format="%.2f",
        key=f"buyer_shipping_domestic_{st.session_state.reset_counter}"
    )

    buyer_shipping_intra = st.number_input(
        lang["buyer_shipping_intra"],
        min_value=0.0,
        value=4.99,
        step=0.1,
        format="%.2f",
        key=f"buyer_shipping_intra_{st.session_state.reset_counter}"
    )

    st.markdown("---")
    st.subheader(lang["current_inputs"])

    current_storage_cost = st.number_input(
        lang["current_storage_cost"],
        min_value=0.0,
        value=1.10,
        step=0.1,
        format="%.2f",
        key=f"current_storage_cost_{st.session_state.reset_counter}"
    )

    current_fulfillment_per_order = st.number_input(
        lang["current_fulfillment_per_order"],
        min_value=0.0,
        value=2.20,
        step=0.1,
        format="%.2f",
        key=f"current_fulfillment_per_order_{st.session_state.reset_counter}"
    )

    current_return_processing = st.number_input(
        lang["current_return_processing"],
        min_value=0.0,
        value=2.20,
        step=0.1,
        format="%.2f",
        key=f"current_return_processing_{st.session_state.reset_counter}"
    )

    current_inventory_handling_monthly = st.number_input(
        lang["current_inventory_handling_monthly"],
        min_value=0.0,
        value=700.0,
        step=50.0,
        format="%.2f",
        key=f"current_inventory_handling_monthly_{st.session_state.reset_counter}"
    )

    current_stock_loss_monthly = st.number_input(
        lang["current_stock_loss_monthly"],
        min_value=0.0,
        value=300.0,
        step=50.0,
        format="%.2f",
        key=f"current_stock_loss_monthly_{st.session_state.reset_counter}"
    )

    current_manpower_monthly = st.number_input(
        lang["current_manpower_monthly"],
        min_value=0.0,
        value=1500.0,
        step=100.0,
        format="%.2f",
        key=f"current_manpower_monthly_{st.session_state.reset_counter}"
    )

    current_other_fixed_monthly = st.number_input(
        lang["current_other_fixed_monthly"],
        min_value=0.0,
        value=300.0,
        step=50.0,
        format="%.2f",
        key=f"current_other_fixed_monthly_{st.session_state.reset_counter}"
    )

    st.markdown("---")
    calculate_clicked = st.button(lang["calculate"], use_container_width=True)
    reset_clicked = st.button(lang["reset"], use_container_width=True)

if reset_clicked:
    st.session_state.reset_counter += 1
    st.rerun()

# =========================================================
# 7. MAIN CALCULATION
# =========================================================

if calculate_clicked:
    mo = max(0, monthly_orders)
    items = max(0.0, avg_items_per_order)
    vol = max(0.0, avg_volume_m3_per_item)
    storage_days = max(0, avg_storage_days)
    coverage_days = max(0, inventory_coverage_days)
    ret = max(0.0, return_rate)
    aov = max(0.0, avg_order_value)

    fbt_total, fbt_breakdown, fbt_extra = calculate_fbt_cost(
        monthly_orders=mo,
        avg_items_per_order=items,
        avg_volume_m3_per_item=vol,
        avg_storage_days=storage_days,
        inventory_coverage_days=coverage_days,
        return_rate=ret,
        warehouse=warehouse,
        domestic_share=max(0.0, domestic_share),
        intra_eu_share=max(0.0, intra_eu_share),
        xs_share=max(0.0, size_xs_share),
        s_share=max(0.0, size_s_share),
        m_share=max(0.0, size_m_share),
        l_share=max(0.0, size_l_share),
        share_ge_20=max(0.0, share_ge_20),
        share_lt_20=max(0.0, share_lt_20),
        buyer_shipping_domestic=max(0.0, buyer_shipping_domestic),
        buyer_shipping_intra=max(0.0, buyer_shipping_intra),
        lang_pack=lang
    )

    current_total, current_breakdown = calculate_current_cost(
        monthly_orders=mo,
        avg_items_per_order=items,
        avg_volume_m3_per_item=vol,
        avg_storage_days=storage_days,
        inventory_coverage_days=coverage_days,
        return_rate=ret,
        current_storage_cost_per_m3_per_day=max(0.0, current_storage_cost),
        current_fulfillment_per_order=max(0.0, current_fulfillment_per_order),
        current_return_processing_per_order=max(0.0, current_return_processing),
        current_inventory_handling_monthly=max(0.0, current_inventory_handling_monthly),
        current_stock_loss_monthly=max(0.0, current_stock_loss_monthly),
        current_manpower_monthly=max(0.0, current_manpower_monthly),
        current_other_fixed_monthly_cost=max(0.0, current_other_fixed_monthly),
        lang_pack=lang
    )

    savings = current_total - fbt_total
    savings_rate = (savings / current_total * 100) if current_total > 0 else 0
    per_order = (savings / mo) if mo > 0 else 0

    revenue = mo * aov
    profit_fbt = revenue - fbt_total
    profit_current = revenue - current_total
    profit_uplift = profit_fbt - profit_current
    annual_impact = savings * 12

    # =========================================================
    # 8. DECISION
    # =========================================================

    if savings > 0:
        verdict = lang["recommend_fbt"]
        color = "green"
    else:
        verdict = lang["not_recommend_fbt"]
        color = "red"

    st.markdown("---")
    st.subheader(lang["decision"])
    st.markdown(
        f"""
        <div style="
            padding: 16px 20px;
            border-radius: 12px;
            background-color: #f7f7f7;
            border-left: 8px solid {color};
            margin-bottom: 12px;
        ">
            <span style="font-size: 28px; font-weight: 700; color: {color};">
                {verdict}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # 9. KPI
    # =========================================================

    st.subheader(lang["section_results"])

    k1, k2, k3, k4 = st.columns(4)
    k5, k6, k7, k8 = st.columns(4)

    k1.metric(lang["a_cost"], f"€ {fbt_total:,.2f}")
    k2.metric(lang["b_cost"], f"€ {current_total:,.2f}")
    k3.metric(lang["c_savings"], f"€ {savings:,.2f}")
    k4.metric(lang["savings_rate"], f"{savings_rate:.2f}%")

    k5.metric(lang["per_order_saving"], f"€ {per_order:,.2f}")
    k6.metric(lang["free_shipping_orders"], f"{fbt_extra['free_shipping_orders']:,.0f}")
    k7.metric(lang["buyer_shipping_saved"], f"€ {fbt_extra['buyer_shipping_saved']:,.2f}")
    k8.metric(lang["monthly_revenue"], f"€ {revenue:,.2f}")

    # =========================================================
    # 10. PROFIT
    # =========================================================

    st.subheader(lang["section_profit"])
    p1, p2, p3 = st.columns(3)
    p1.metric(lang["fbt_profit"], f"€ {profit_fbt:,.2f}")
    p2.metric(lang["current_profit"], f"€ {profit_current:,.2f}")
    p3.metric(lang["profit_uplift"], f"€ {profit_uplift:,.2f}")

    # =========================================================
    # 11. COST BREAKDOWN
    # =========================================================

    st.subheader(lang["section_breakdown"])
    bd1, bd2 = st.columns(2)

    with bd1:
        st.markdown(f"**{lang['fbt_breakdown']}**")
        for k, v in fbt_breakdown.items():
            st.write(f"- {k}: € {v:,.2f}")

    with bd2:
        st.markdown(f"**{lang['current_breakdown']}**")
        for k, v in current_breakdown.items():
            st.write(f"- {k}: € {v:,.2f}")

    # =========================================================
    # 12. SALES INSIGHT
    # =========================================================

    st.subheader(lang["sales_insight"])
    st.info(
        f"""
• {lang['c_savings']}: **€ {savings:,.2f} / month**

• {lang['per_order_saving']}: **€ {per_order:,.2f}**

• {lang['annual_impact']}: **€ {annual_impact:,.2f}**

• {lang['buyer_shipping_saved']}: **€ {fbt_extra['buyer_shipping_saved']:,.2f}**

👉 This supports both **margin improvement** and **buyer experience**
        """
    )

    # =========================================================
    # 13. ORDER RANGE CURVES
    # =========================================================

    max_orders = max(100, int(mo * 2)) if mo > 0 else 1000
    start_orders = max(100, int(max(mo, 100) * 0.2))
    order_range = np.linspace(start_orders, max_orders, 25)

    fbt_curve = []
    cur_curve = []
    save_curve = []

    for orders in order_range:
        f_cost, _, _ = calculate_fbt_cost(
            monthly_orders=orders,
            avg_items_per_order=items,
            avg_volume_m3_per_item=vol,
            avg_storage_days=storage_days,
            inventory_coverage_days=coverage_days,
            return_rate=ret,
            warehouse=warehouse,
            domestic_share=max(0.0, domestic_share),
            intra_eu_share=max(0.0, intra_eu_share),
            xs_share=max(0.0, size_xs_share),
            s_share=max(0.0, size_s_share),
            m_share=max(0.0, size_m_share),
            l_share=max(0.0, size_l_share),
            share_ge_20=max(0.0, share_ge_20),
            share_lt_20=max(0.0, share_lt_20),
            buyer_shipping_domestic=max(0.0, buyer_shipping_domestic),
            buyer_shipping_intra=max(0.0, buyer_shipping_intra),
            lang_pack=lang
        )

        c_cost, _ = calculate_current_cost(
            monthly_orders=orders,
            avg_items_per_order=items,
            avg_volume_m3_per_item=vol,
            avg_storage_days=storage_days,
            inventory_coverage_days=coverage_days,
            return_rate=ret,
            current_storage_cost_per_m3_per_day=max(0.0, current_storage_cost),
            current_fulfillment_per_order=max(0.0, current_fulfillment_per_order),
            current_return_processing_per_order=max(0.0, current_return_processing),
            current_inventory_handling_monthly=max(0.0, current_inventory_handling_monthly),
            current_stock_loss_monthly=max(0.0, current_stock_loss_monthly),
            current_manpower_monthly=max(0.0, current_manpower_monthly),
            current_other_fixed_monthly_cost=max(0.0, current_other_fixed_monthly),
            lang_pack=lang
        )

        fbt_curve.append(f_cost)
        cur_curve.append(c_cost)
        save_curve.append(c_cost - f_cost)

    # =========================================================
    # 14. BREAK-EVEN
    # =========================================================

    breakeven_orders = None
    for i, v in enumerate(save_curve):
        if v > 0:
            breakeven_orders = int(order_range[i])
            break

    if breakeven_orders is not None:
        st.success(lang["breakeven_found"].format(orders=breakeven_orders))
    else:
        st.warning(lang["breakeven_not_found"])

    # =========================================================
    # 15. CHART 1 - COST CURVE
    # =========================================================

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(order_range, fbt_curve, linewidth=3, label=lang["line_fbt"])
    ax1.plot(order_range, cur_curve, linewidth=3, label=lang["line_current"])

    lower = np.minimum(fbt_curve, cur_curve)
    upper = np.maximum(fbt_curve, cur_curve)
    ax1.fill_between(order_range, lower, upper, alpha=0.2)

    if mo > 0:
        ax1.axvline(mo, linestyle="--", alpha=0.5)

    ax1.set_xlabel(lang["x_orders"])
    ax1.set_ylabel(lang["y_eur"])
    ax1.set_title(lang["chart1"])
    ax1.legend()
    ax1.grid(alpha=0.3)
    st.pyplot(fig1)

    # =========================================================
    # 16. CHART 2 - TOTAL COMPARISON
    # =========================================================

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    labels = [lang["line_fbt"], lang["line_current"], lang["line_savings"]]
    values = [fbt_total, current_total, savings]
    bars = ax2.bar(labels, values)

    ax2.set_ylabel(lang["y_eur"])
    ax2.set_title(lang["chart2"])
    ax2.grid(axis="y", alpha=0.3)

    for bar, val in zip(bars, values):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"€ {val:,.0f}",
            ha="center",
            va="bottom"
        )

    st.pyplot(fig2)

    # =========================================================
    # 17. CHART 3 - BREAKDOWN COMPARISON
    # =========================================================

    all_keys = list(dict.fromkeys(list(fbt_breakdown.keys()) + list(current_breakdown.keys())))
    f_vals = [fbt_breakdown.get(k, 0) for k in all_keys]
    c_vals = [current_breakdown.get(k, 0) for k in all_keys]

    x = np.arange(len(all_keys))
    width = 0.38

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.bar(x - width / 2, f_vals, width, label=lang["line_fbt"])
    ax3.bar(x + width / 2, c_vals, width, label=lang["line_current"])

    ax3.set_xticks(x)
    ax3.set_xticklabels(all_keys, rotation=30, ha="right")
    ax3.set_ylabel(lang["y_eur"])
    ax3.set_title(lang["chart3"])
    ax3.legend()
    ax3.grid(axis="y", alpha=0.3)

    st.pyplot(fig3)

else:
    st.info("请在左侧输入参数后点击 Calculate / 开始计算。")
