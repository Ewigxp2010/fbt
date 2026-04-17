# -*- coding: utf-8 -*-
# FBT Inventory + Fulfillment Benefit Simulator - Streamlit V6
# Centered input layout version
# ------------------------------------------------------------

import io
import textwrap
from datetime import date

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import streamlit as st

# =========================================================
# 1. LANGUAGE PACK
# =========================================================

LANG = {
    "en": {
        "title": "FBT Inventory & Fulfillment Benefit Simulator",
        "subtitle": "Compare FBT vs current fulfillment model from cost and profit perspectives.",
        "basic_inputs": "1. Basic Inputs",
        "fbt_inputs": "2. FBT Inputs",
        "current_inputs": "3. Current Solution Inputs",
        "business_inputs": "4. Business Inputs",
        "report_inputs": "Report Inputs",
        "calculate": "Calculate",
        "reset": "Reset",

        "client_name": "Client Name",
        "report_date": "Report Date",

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
        "profit_uplift": "Profit Uplift (Cost Savings Only)",

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
        "executive_summary": "Executive Summary",
        "annual_impact": "Annual Savings Impact",
        "breakeven_found": "Break-even at approximately {orders} orders/month",
        "breakeven_not_found": "No break-even found within the current order range",

        "section_results": "Results",
        "section_profit": "Profit Comparison",
        "section_breakdown": "Cost Breakdown",
        "section_assumptions": "Normalized Shares Used",
        "download_csv": "Download results CSV",
        "download_pdf": "Download PDF report",

        "note_input": "Input note",
        "note_input_text": "Shares do not need to sum to 1.0. The simulator will normalize them automatically.",
        "profit_note": "Profit uplift here only reflects cost reduction. No GMV uplift or conversion uplift is assumed.",

        "placeholder": "Fill in the inputs above and click Calculate.",
        "domestic_norm": "Domestic share (normalized)",
        "intra_norm": "Intra-EU share (normalized)",
        "ge20_norm": ">= €20 share (normalized)",
        "lt20_norm": "< €20 share (normalized)",
        "xs_norm": "XS share (normalized)",
        "s_norm": "S share (normalized)",
        "m_norm": "M share (normalized)",
        "l_norm": "L share (normalized)",

        "pdf_title": "FBT Benefit Simulation Report",
        "pdf_subtitle": "Generated by Streamlit Simulator",
        "pdf_inputs": "Input Summary",
        "pdf_outputs": "Output Summary",
        "pdf_notes": "Notes",
        "pdf_cover_for": "Prepared for",
        "pdf_cover_date": "Report date",
        "pdf_conclusion": "Conclusion",
        "pdf_exec_summary": "Executive Summary",
        "default_client_name": "Client",
    },
    "zh": {
        "title": "FBT 库存与履约收益模拟器",
        "subtitle": "从成本和利润两个视角，对比 FBT 与客户当前履约方案。",
        "basic_inputs": "1. 基础输入",
        "fbt_inputs": "2. FBT 输入",
        "current_inputs": "3. 客户当前方案输入",
        "business_inputs": "4. 业务输入",
        "report_inputs": "报告信息",
        "calculate": "开始计算",
        "reset": "重置",

        "client_name": "客户名称",
        "report_date": "报告日期",

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
        "profit_uplift": "利润提升（仅成本节省）",

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
        "executive_summary": "管理摘要",
        "annual_impact": "年度节省影响",
        "breakeven_found": "盈亏平衡点约为每月 {orders} 单",
        "breakeven_not_found": "在当前订单范围内未找到盈亏平衡点",

        "section_results": "结果",
        "section_profit": "利润对比",
        "section_breakdown": "成本拆分",
        "section_assumptions": "归一化后的占比",
        "download_csv": "下载结果 CSV",
        "download_pdf": "下载 PDF 报告",

        "note_input": "输入说明",
        "note_input_text": "各类 share 不必手动加总为 1.0，系统会自动归一化。",
        "profit_note": "这里的利润提升只反映成本下降带来的改善，不假设任何 GMV 或转化率提升。",

        "placeholder": "请在上方填写参数后点击开始计算。",
        "domestic_norm": "Domestic 占比（归一化）",
        "intra_norm": "Intra-EU 占比（归一化）",
        "ge20_norm": ">= €20 占比（归一化）",
        "lt20_norm": "< €20 占比（归一化）",
        "xs_norm": "XS 占比（归一化）",
        "s_norm": "S 占比（归一化）",
        "m_norm": "M 占比（归一化）",
        "l_norm": "L 占比（归一化）",

        "pdf_title": "FBT 收益模拟报告",
        "pdf_subtitle": "由 Streamlit 模拟器生成",
        "pdf_inputs": "输入摘要",
        "pdf_outputs": "输出摘要",
        "pdf_notes": "备注",
        "pdf_cover_for": "客户",
        "pdf_cover_date": "报告日期",
        "pdf_conclusion": "结论",
        "pdf_exec_summary": "管理摘要",
        "default_client_name": "客户",
    },
}

# =========================================================
# 2. RATE CARD
# =========================================================

RATE_CARD = {
    "DE": {
        "storage_per_m3_per_day": 0.58,
        "domestic": {"XS": 0.80, "S": 1.00, "M": 1.30, "L": 1.80},
        "intra_eu": {"XS": 1.04, "S": 1.35, "M": 1.75, "L": 2.40},
    },
    "ES": {
        "storage_per_m3_per_day": 0.58,
        "domestic": {"XS": 0.80, "S": 1.00, "M": 1.30, "L": 1.80},
        "intra_eu": {"XS": 1.04, "S": 1.35, "M": 1.75, "L": 2.40},
    },
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
    xs, s, m, l = normalize_shares([xs, s, m, l])
    dom_rate = (
        xs * RATE_CARD[warehouse]["domestic"]["XS"]
        + s * RATE_CARD[warehouse]["domestic"]["S"]
        + m * RATE_CARD[warehouse]["domestic"]["M"]
        + l * RATE_CARD[warehouse]["domestic"]["L"]
    )
    intra_rate = (
        xs * RATE_CARD[warehouse]["intra_eu"]["XS"]
        + s * RATE_CARD[warehouse]["intra_eu"]["S"]
        + m * RATE_CARD[warehouse]["intra_eu"]["M"]
        + l * RATE_CARD[warehouse]["intra_eu"]["L"]
    )
    domestic_share, intra_share = normalize_shares([domestic_share, intra_share])
    weighted = domestic_share * dom_rate + intra_share * intra_rate
    return weighted, dom_rate, intra_rate


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
    lang_pack,
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
    return_cost = monthly_orders * return_rate * weighted_fulfillment * 0.5
    seller_total = storage_cost + fulfillment_cost + return_cost

    domestic_share_n, intra_eu_share_n = normalize_shares([domestic_share, intra_eu_share])
    ge20_share_n, lt20_share_n = normalize_shares([share_ge_20, share_lt_20])

    free_shipping_orders = monthly_orders * ge20_share_n
    avg_buyer_shipping = domestic_share_n * buyer_shipping_domestic + intra_eu_share_n * buyer_shipping_intra
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
        "buyer_shipping_saved": buyer_shipping_saved,
        "domestic_share_norm": domestic_share_n,
        "intra_share_norm": intra_eu_share_n,
        "ge20_share_norm": ge20_share_n,
        "lt20_share_norm": lt20_share_n,
        "xs_s_m_l_norm": normalize_shares([xs_share, s_share, m_share, l_share]),
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
    lang_pack,
):
    total_items_month = monthly_orders * avg_items_per_order
    avg_inventory_items = total_items_month * (inventory_coverage_days / 30.0)
    avg_inventory_volume = avg_inventory_items * avg_volume_m3_per_item

    storage_cost = avg_inventory_volume * avg_storage_days * current_storage_cost_per_m3_per_day
    fulfillment_cost = monthly_orders * current_fulfillment_per_order
    return_cost = monthly_orders * return_rate * current_return_processing_per_order

    total = (
        storage_cost
        + fulfillment_cost
        + return_cost
        + current_inventory_handling_monthly
        + current_stock_loss_monthly
        + current_manpower_monthly
        + current_other_fixed_monthly_cost
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


def format_eur(x):
    return f"€ {x:,.2f}"


def build_results_dataframe(metrics_dict):
    return pd.DataFrame([{"Metric": k, "Value": v} for k, v in metrics_dict.items()])


def df_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def make_cost_curve_figure(lang, order_range, fbt_curve, cur_curve, mo):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(order_range, fbt_curve, linewidth=3, label=lang["line_fbt"])
    ax.plot(order_range, cur_curve, linewidth=3, label=lang["line_current"])
    lower = np.minimum(fbt_curve, cur_curve)
    upper = np.maximum(fbt_curve, cur_curve)
    ax.fill_between(order_range, lower, upper, alpha=0.18)
    if mo > 0:
        ax.axvline(mo, linestyle="--", alpha=0.5)
    ax.set_xlabel(lang["x_orders"])
    ax.set_ylabel(lang["y_eur"])
    ax.set_title(lang["chart1"])
    ax.legend()
    ax.grid(alpha=0.3)
    return fig


def make_total_comparison_figure(lang, fbt_total, current_total, savings):
    fig, ax = plt.subplots(figsize=(8, 6))
    labels = [lang["line_fbt"], lang["line_current"], lang["line_savings"]]
    values = [fbt_total, current_total, savings]
    bars = ax.bar(labels, values)
    ax.set_ylabel(lang["y_eur"])
    ax.set_title(lang["chart2"])
    ax.grid(axis="y", alpha=0.3)

    ymax = max(values) if values else 0
    ymin = min(values) if values else 0
    offset = max(abs(ymax), abs(ymin), 1) * 0.03

    for bar, val in zip(bars, values):
        x = bar.get_x() + bar.get_width() / 2
        if val >= 0:
            ax.text(x, val + offset, f"€ {val:,.0f}", ha="center", va="bottom")
        else:
            ax.text(x, val - offset, f"€ {val:,.0f}", ha="center", va="top")
    return fig


def make_breakdown_figure(lang, fbt_breakdown, current_breakdown):
    all_keys = list(dict.fromkeys(list(fbt_breakdown.keys()) + list(current_breakdown.keys())))
    f_vals = [fbt_breakdown.get(k, 0) for k in all_keys]
    c_vals = [current_breakdown.get(k, 0) for k in all_keys]

    x = np.arange(len(all_keys))
    width = 0.38

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width / 2, f_vals, width, label=lang["line_fbt"])
    ax.bar(x + width / 2, c_vals, width, label=lang["line_current"])
    ax.set_xticks(x)
    ax.set_xticklabels(all_keys, rotation=30, ha="right")
    ax.set_ylabel(lang["y_eur"])
    ax.set_title(lang["chart3"])
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    return fig


def wrap_and_draw(fig, x, y, text, width=90, fontsize=10, line_height=0.018):
    lines = textwrap.wrap(text, width=width) or [text]
    for line in lines:
        fig.text(x, y, line, fontsize=fontsize)
        y -= line_height
    return y


def create_pdf_report(
    lang,
    client_name,
    report_date_str,
    verdict,
    executive_summary,
    input_summary,
    output_summary,
    note_lines,
    fig1,
    fig2,
    fig3,
):
    buffer = io.BytesIO()

    with PdfPages(buffer) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.patch.set_facecolor("white")
        fig.text(0.08, 0.88, lang["pdf_title"], fontsize=22, fontweight="bold")
        fig.text(0.08, 0.84, lang["pdf_subtitle"], fontsize=11)
        fig.text(0.08, 0.74, f"{lang['pdf_cover_for']}: {client_name}", fontsize=14)
        fig.text(0.08, 0.70, f"{lang['pdf_cover_date']}: {report_date_str}", fontsize=14)
        fig.text(0.08, 0.60, lang["pdf_conclusion"], fontsize=16, fontweight="bold")
        fig.text(0.08, 0.55, verdict, fontsize=20)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = plt.figure(figsize=(8.27, 11.69))
        fig.patch.set_facecolor("white")
        y = 0.94
        fig.text(0.08, y, lang["pdf_exec_summary"], fontsize=18, fontweight="bold")
        y -= 0.05
        y = wrap_and_draw(fig, 0.08, y, executive_summary, width=95, fontsize=11, line_height=0.022)
        y -= 0.04
        fig.text(0.08, y, lang["pdf_outputs"], fontsize=14, fontweight="bold")
        y -= 0.03
        for line in output_summary:
            y = wrap_and_draw(fig, 0.08, y, f"• {line}", width=90, fontsize=10, line_height=0.018)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = plt.figure(figsize=(8.27, 11.69))
        fig.patch.set_facecolor("white")
        y = 0.95
        fig.text(0.08, y, lang["pdf_inputs"], fontsize=14, fontweight="bold")
        y -= 0.03
        for line in input_summary:
            y = wrap_and_draw(fig, 0.08, y, f"• {line}", width=90, fontsize=10, line_height=0.018)
            if y < 0.20:
                break

        y -= 0.02
        fig.text(0.08, y, lang["pdf_notes"], fontsize=14, fontweight="bold")
        y -= 0.03
        for line in note_lines:
            y = wrap_and_draw(fig, 0.08, y, f"• {line}", width=90, fontsize=10, line_height=0.018)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        pdf.savefig(fig1, bbox_inches="tight")
        pdf.savefig(fig2, bbox_inches="tight")
        pdf.savefig(fig3, bbox_inches="tight")

    buffer.seek(0)
    return buffer.getvalue()


def build_executive_summary(lang, savings, per_order, annual_impact, verdict, buyer_shipping_saved):
    if lang is LANG["zh"]:
        return (
            f"基于当前输入假设，结论为：{verdict}。"
            f"在不假设任何 GMV 提升的前提下，FBT 预计可为卖家每月节省 {format_eur(savings)} 的运营成本，"
            f"相当于每单改善 {format_eur(per_order)}，按年化测算约为 {format_eur(annual_impact)}。"
            f"与此同时，买家侧包邮相关运费价值约为 {format_eur(buyer_shipping_saved)}。"
            f"因此，本报告中的利润提升仅来源于成本下降，而非收入增长。"
        )
    return (
        f"Based on the current assumptions, the conclusion is: {verdict}. "
        f"Without assuming any GMV uplift, FBT is estimated to reduce seller-side monthly operating cost by {format_eur(savings)}, "
        f"equivalent to {format_eur(per_order)} per order and {format_eur(annual_impact)} on an annualized basis. "
        f"In addition, the buyer-side shipping value saved is estimated at {format_eur(buyer_shipping_saved)}. "
        f"Therefore, the profit improvement in this report comes purely from cost savings rather than revenue uplift."
    )

# =========================================================
# 4. PAGE CONFIG
# =========================================================

st.set_page_config(page_title="FBT Simulator", layout="wide")

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

lang_choice = st.selectbox(
    "Language / 语言",
    options=["en", "zh"],
    format_func=lambda x: "English" if x == "en" else "中文",
    key=f"language_{st.session_state.reset_counter}",
)

lang = LANG[lang_choice]

st.title(lang["title"])
st.caption(lang["subtitle"])
st.info(f"**{lang['note_input']}**：{lang['note_input_text']}")

# =========================================================
# 5. CENTERED INPUTS
# =========================================================

st.markdown(f"### {lang['report_inputs']}")
r1, r2 = st.columns(2)
with r1:
    client_name = st.text_input(
        lang["client_name"],
        value=lang["default_client_name"],
        key=f"client_name_{st.session_state.reset_counter}",
    )
with r2:
    report_date_value = st.date_input(
        lang["report_date"],
        value=date.today(),
        key=f"report_date_{st.session_state.reset_counter}",
    )

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"### {lang['basic_inputs']}")
    warehouse = st.selectbox(lang["warehouse_country"], ["DE", "ES"], key=f"warehouse_{st.session_state.reset_counter}")
    monthly_orders = st.number_input(lang["monthly_orders"], min_value=0, value=3000, step=100, key=f"monthly_orders_{st.session_state.reset_counter}")
    avg_items_per_order = st.number_input(lang["avg_items_per_order"], min_value=0.0, value=1.0, step=0.1, format="%.2f", key=f"avg_items_per_order_{st.session_state.reset_counter}")
    avg_volume_m3_per_item = st.number_input(lang["avg_volume_m3_per_item"], min_value=0.0, value=0.01, step=0.001, format="%.4f", key=f"avg_volume_{st.session_state.reset_counter}")
    avg_storage_days = st.number_input(lang["avg_storage_days"], min_value=0, value=30, step=1, key=f"avg_storage_days_{st.session_state.reset_counter}")
    inventory_coverage_days = st.number_input(lang["inventory_coverage_days"], min_value=0, value=30, step=1, key=f"inventory_coverage_days_{st.session_state.reset_counter}")
    return_rate = st.number_input(lang["return_rate"], min_value=0.0, value=0.05, step=0.01, format="%.4f", key=f"return_rate_{st.session_state.reset_counter}")

with c2:
    st.markdown(f"### {lang['business_inputs']}")
    avg_order_value = st.number_input(lang["avg_order_value"], min_value=0.0, value=30.0, step=1.0, format="%.2f", key=f"aov_{st.session_state.reset_counter}")
    domestic_share = st.number_input(lang["domestic_share"], min_value=0.0, value=0.6, step=0.05, format="%.4f", key=f"domestic_share_{st.session_state.reset_counter}")
    intra_eu_share = st.number_input(lang["intra_eu_share"], min_value=0.0, value=0.4, step=0.05, format="%.4f", key=f"intra_eu_share_{st.session_state.reset_counter}")
    share_ge_20 = st.number_input(lang["share_ge_20"], min_value=0.0, value=0.6, step=0.05, format="%.4f", key=f"share_ge_20_{st.session_state.reset_counter}")
    share_lt_20 = st.number_input(lang["share_lt_20"], min_value=0.0, value=0.4, step=0.05, format="%.4f", key=f"share_lt_20_{st.session_state.reset_counter}")
    size_xs_share = st.number_input(lang["size_xs_share"], min_value=0.0, value=0.25, step=0.05, format="%.4f", key=f"size_xs_share_{st.session_state.reset_counter}")
    size_s_share = st.number_input(lang["size_s_share"], min_value=0.0, value=0.25, step=0.05, format="%.4f", key=f"size_s_share_{st.session_state.reset_counter}")
    size_m_share = st.number_input(lang["size_m_share"], min_value=0.0, value=0.25, step=0.05, format="%.4f", key=f"size_m_share_{st.session_state.reset_counter}")
    size_l_share = st.number_input(lang["size_l_share"], min_value=0.0, value=0.25, step=0.05, format="%.4f", key=f"size_l_share_{st.session_state.reset_counter}")

with c3:
    st.markdown(f"### {lang['fbt_inputs']}")
    st.number_input(
        lang["fbt_storage_cost"],
        value=float(RATE_CARD[warehouse]["storage_per_m3_per_day"]),
        disabled=True,
        key=f"fbt_storage_cost_display_{st.session_state.reset_counter}",
    )
    buyer_shipping_domestic = st.number_input(lang["buyer_shipping_domestic"], min_value=0.0, value=4.99, step=0.1, format="%.2f", key=f"buyer_shipping_domestic_{st.session_state.reset_counter}")
    buyer_shipping_intra = st.number_input(lang["buyer_shipping_intra"], min_value=0.0, value=4.99, step=0.1, format="%.2f", key=f"buyer_shipping_intra_{st.session_state.reset_counter}")

with c4:
    st.markdown(f"### {lang['current_inputs']}")
    current_storage_cost = st.number_input(lang["current_storage_cost"], min_value=0.0, value=1.10, step=0.1, format="%.2f", key=f"current_storage_cost_{st.session_state.reset_counter}")
    current_fulfillment_per_order = st.number_input(lang["current_fulfillment_per_order"], min_value=0.0, value=2.20, step=0.1, format="%.2f", key=f"current_fulfillment_per_order_{st.session_state.reset_counter}")
    current_return_processing = st.number_input(lang["current_return_processing"], min_value=0.0, value=2.20, step=0.1, format="%.2f", key=f"current_return_processing_{st.session_state.reset_counter}")
    current_inventory_handling_monthly = st.number_input(lang["current_inventory_handling_monthly"], min_value=0.0, value=700.0, step=50.0, format="%.2f", key=f"current_inventory_handling_monthly_{st.session_state.reset_counter}")
    current_stock_loss_monthly = st.number_input(lang["current_stock_loss_monthly"], min_value=0.0, value=300.0, step=50.0, format="%.2f", key=f"current_stock_loss_monthly_{st.session_state.reset_counter}")
    current_manpower_monthly = st.number_input(lang["current_manpower_monthly"], min_value=0.0, value=1500.0, step=100.0, format="%.2f", key=f"current_manpower_monthly_{st.session_state.reset_counter}")
    current_other_fixed_monthly = st.number_input(lang["current_other_fixed_monthly"], min_value=0.0, value=300.0, step=50.0, format="%.2f", key=f"current_other_fixed_monthly_{st.session_state.reset_counter}")

b1, b2, _ = st.columns([1, 1, 4])
with b1:
    calculate_clicked = st.button(lang["calculate"], use_container_width=True)
with b2:
    reset_clicked = st.button(lang["reset"], use_container_width=True)

if reset_clicked:
    st.session_state.reset_counter += 1
    st.rerun()

if not calculate_clicked:
    st.info(lang["placeholder"])

# =========================================================
# 6. CALCULATION
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
        lang_pack=lang,
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
        lang_pack=lang,
    )

    savings = current_total - fbt_total
    savings_rate = (savings / current_total * 100) if current_total > 0 else 0
    per_order = (savings / mo) if mo > 0 else 0

    revenue = mo * aov
    profit_fbt = revenue - fbt_total
    profit_current = revenue - current_total
    profit_uplift = savings
    annual_impact = savings * 12

    verdict = lang["recommend_fbt"] if savings > 0 else lang["not_recommend_fbt"]
    color = "green" if savings > 0 else "red"

    executive_summary = build_executive_summary(
        lang=lang,
        savings=savings,
        per_order=per_order,
        annual_impact=annual_impact,
        verdict=verdict,
        buyer_shipping_saved=fbt_extra["buyer_shipping_saved"],
    )

    st.markdown("---")
    st.subheader(lang["decision"])
    st.markdown(
        f"""
        <div style="
            padding: 16px 20px;
            border-radius: 12px;
            background-color: #f7f7f7;
            border-left: 8px solid {color};
            margin-bottom: 12px;">
            <span style="font-size: 28px; font-weight: 700; color: {color};">{verdict}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(lang["executive_summary"])
    st.info(executive_summary)

    st.subheader(lang["section_results"])
    k1, k2, k3, k4 = st.columns(4)
    k5, k6, k7, k8 = st.columns(4)

    k1.metric(lang["a_cost"], format_eur(fbt_total))
    k2.metric(lang["b_cost"], format_eur(current_total))
    k3.metric(lang["c_savings"], format_eur(savings))
    k4.metric(lang["savings_rate"], f"{savings_rate:.2f}%")
    k5.metric(lang["per_order_saving"], format_eur(per_order))
    k6.metric(lang["free_shipping_orders"], f"{fbt_extra['free_shipping_orders']:,.0f}")
    k7.metric(lang["buyer_shipping_saved"], format_eur(fbt_extra["buyer_shipping_saved"]))
    k8.metric(lang["monthly_revenue"], format_eur(revenue))

    st.subheader(lang["section_profit"])
    st.caption(lang["profit_note"])
    p1, p2, p3 = st.columns(3)
    p1.metric(lang["fbt_profit"], format_eur(profit_fbt))
    p2.metric(lang["current_profit"], format_eur(profit_current))
    p3.metric(lang["profit_uplift"], format_eur(profit_uplift))

    st.subheader(lang["section_breakdown"])
    bd1, bd2 = st.columns(2)

    with bd1:
        st.markdown(f"**{lang['fbt_breakdown']}**")
        for k, v in fbt_breakdown.items():
            st.write(f"- {k}: {format_eur(v)}")

    with bd2:
        st.markdown(f"**{lang['current_breakdown']}**")
        for k, v in current_breakdown.items():
            st.write(f"- {k}: {format_eur(v)}")

    st.subheader(lang["section_assumptions"])
    xs_n, s_n, m_n, l_n = fbt_extra["xs_s_m_l_norm"]
    norm_df = pd.DataFrame(
        {
            "Metric": [
                lang["domestic_norm"],
                lang["intra_norm"],
                lang["ge20_norm"],
                lang["lt20_norm"],
                lang["xs_norm"],
                lang["s_norm"],
                lang["m_norm"],
                lang["l_norm"],
            ],
            "Value": [
                f"{fbt_extra['domestic_share_norm']:.2%}",
                f"{fbt_extra['intra_share_norm']:.2%}",
                f"{fbt_extra['ge20_share_norm']:.2%}",
                f"{fbt_extra['lt20_share_norm']:.2%}",
                f"{xs_n:.2%}",
                f"{s_n:.2%}",
                f"{m_n:.2%}",
                f"{l_n:.2%}",
            ],
        }
    )
    st.dataframe(norm_df, use_container_width=True, hide_index=True)

    st.subheader(lang["sales_insight"])
    st.info(
        f"""
• {lang['c_savings']}: **{format_eur(savings)} / month**

• {lang['per_order_saving']}: **{format_eur(per_order)}**

• {lang['annual_impact']}: **{format_eur(annual_impact)}**

• {lang['buyer_shipping_saved']}: **{format_eur(fbt_extra['buyer_shipping_saved'])}**

👉 {lang['profit_note']}
        """
    )

    max_orders = max(100, int(mo * 2)) if mo > 0 else 1000
    start_orders = max(100, int(max(mo, 100) * 0.2))
    order_range = np.linspace(start_orders, max_orders, 25)

    fbt_curve, cur_curve, save_curve = [], [], []
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
            lang_pack=lang,
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
            lang_pack=lang,
        )
        fbt_curve.append(f_cost)
        cur_curve.append(c_cost)
        save_curve.append(c_cost - f_cost)

    breakeven_orders = None
    for i, v in enumerate(save_curve):
        if v > 0:
            breakeven_orders = int(order_range[i])
            break

    if breakeven_orders is not None:
        st.success(lang["breakeven_found"].format(orders=breakeven_orders))
    else:
        st.warning(lang["breakeven_not_found"])

    fig1 = make_cost_curve_figure(lang, order_range, fbt_curve, cur_curve, mo)
    st.pyplot(fig1)

    fig2 = make_total_comparison_figure(lang, fbt_total, current_total, savings)
    st.pyplot(fig2)

    fig3 = make_breakdown_figure(lang, fbt_breakdown, current_breakdown)
    st.pyplot(fig3)

    export_metrics = {
        lang["a_cost"]: round(fbt_total, 2),
        lang["b_cost"]: round(current_total, 2),
        lang["c_savings"]: round(savings, 2),
        lang["savings_rate"]: round(savings_rate, 2),
        lang["per_order_saving"]: round(per_order, 2),
        lang["free_shipping_orders"]: round(fbt_extra["free_shipping_orders"], 0),
        lang["buyer_shipping_saved"]: round(fbt_extra["buyer_shipping_saved"], 2),
        lang["monthly_revenue"]: round(revenue, 2),
        lang["fbt_profit"]: round(profit_fbt, 2),
        lang["current_profit"]: round(profit_current, 2),
        lang["profit_uplift"]: round(profit_uplift, 2),
        lang["annual_impact"]: round(annual_impact, 2),
    }

    export_df = build_results_dataframe(export_metrics)
    csv_bytes = df_to_csv_bytes(export_df)

    report_date_str = str(report_date_value)

    input_summary = [
        f"{lang['client_name']}: {client_name}",
        f"{lang['report_date']}: {report_date_str}",
        f"{lang['warehouse_country']}: {warehouse}",
        f"{lang['monthly_orders']}: {mo}",
        f"{lang['avg_items_per_order']}: {items}",
        f"{lang['avg_volume_m3_per_item']}: {vol}",
        f"{lang['avg_storage_days']}: {storage_days}",
        f"{lang['inventory_coverage_days']}: {coverage_days}",
        f"{lang['return_rate']}: {ret:.2%}",
        f"{lang['avg_order_value']}: {format_eur(aov)}",
        f"{lang['domestic_share']}: {domestic_share}",
        f"{lang['intra_eu_share']}: {intra_eu_share}",
        f"{lang['share_ge_20']}: {share_ge_20}",
        f"{lang['share_lt_20']}: {share_lt_20}",
        f"{lang['size_xs_share']}: {size_xs_share}",
        f"{lang['size_s_share']}: {size_s_share}",
        f"{lang['size_m_share']}: {size_m_share}",
        f"{lang['size_l_share']}: {size_l_share}",
        f"{lang['buyer_shipping_domestic']}: {format_eur(buyer_shipping_domestic)}",
        f"{lang['buyer_shipping_intra']}: {format_eur(buyer_shipping_intra)}",
        f"{lang['current_storage_cost']}: {format_eur(current_storage_cost)}",
        f"{lang['current_fulfillment_per_order']}: {format_eur(current_fulfillment_per_order)}",
        f"{lang['current_return_processing']}: {format_eur(current_return_processing)}",
    ]

    output_summary = [
        f"{lang['a_cost']}: {format_eur(fbt_total)}",
        f"{lang['b_cost']}: {format_eur(current_total)}",
        f"{lang['c_savings']}: {format_eur(savings)}",
        f"{lang['savings_rate']}: {savings_rate:.2f}%",
        f"{lang['per_order_saving']}: {format_eur(per_order)}",
        f"{lang['monthly_revenue']}: {format_eur(revenue)}",
        f"{lang['fbt_profit']}: {format_eur(profit_fbt)}",
        f"{lang['current_profit']}: {format_eur(profit_current)}",
        f"{lang['profit_uplift']}: {format_eur(profit_uplift)}",
        f"{lang['annual_impact']}: {format_eur(annual_impact)}",
    ]

    note_lines = [
        lang["profit_note"],
        f"{lang['domestic_norm']}: {fbt_extra['domestic_share_norm']:.2%}",
        f"{lang['intra_norm']}: {fbt_extra['intra_share_norm']:.2%}",
        f"{lang['ge20_norm']}: {fbt_extra['ge20_share_norm']:.2%}",
        f"{lang['lt20_norm']}: {fbt_extra['lt20_share_norm']:.2%}",
    ]

    pdf_bytes = create_pdf_report(
        lang=lang,
        client_name=client_name,
        report_date_str=report_date_str,
        verdict=verdict,
        executive_summary=executive_summary,
        input_summary=input_summary,
        output_summary=output_summary,
        note_lines=note_lines,
        fig1=fig1,
        fig2=fig2,
        fig3=fig3,
    )

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            label=lang["download_csv"],
            data=csv_bytes,
            file_name="fbt_simulation_results.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            label=lang["download_pdf"],
            data=pdf_bytes,
            file_name="fbt_simulation_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    plt.close(fig1)
    plt.close(fig2)
    plt.close(fig3)
