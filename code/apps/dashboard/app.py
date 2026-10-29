import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Хостинг-провайдер — Аналитика серверов",
    page_icon="🖥️",
    layout="wide",
)

st.title("🖥️ Облачная инфраструктура — Панель управления")

# Боковая панель
st.sidebar.header("⚙️ Фильтры")
days = st.sidebar.selectbox("Период анализа", [7, 14, 30, 90, 365], index=2, format_func=lambda x: f"{x} дней")

if st.sidebar.button("🔄 Обновить метрики"):
    st.cache_data.clear()
    st.rerun()

# Функции загрузки
@st.cache_data(ttl=60)
def load_kpi(days):
    return requests.get(f"{API_URL}/api/reports/kpi/", params={"days": days}).json()

@st.cache_data(ttl=60)
def load_revenue(days):
    return pd.DataFrame(requests.get(f"{API_URL}/api/reports/revenue/", params={"days": days}).json())

@st.cache_data(ttl=60)
def load_top():
    return pd.DataFrame(requests.get(f"{API_URL}/api/reports/top-models/").json())

@st.cache_data(ttl=60)
def load_managers(days):
    return pd.DataFrame(requests.get(f"{API_URL}/api/reports/manager-load/", params={"days": days}).json())

@st.cache_data(ttl=60)
def load_stock():
    return pd.DataFrame(requests.get(f"{API_URL}/api/reports/stock/").json())

# Метрики
kpi = load_kpi(days)
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Выручка от аренды", f"{kpi.get('revenue', 0):,.0f} ₽")
c2.metric("📋 Активных аренд", kpi.get("sales_count", 0))
c3.metric("📊 Средний чек", f"{kpi.get('avg_check', 0):,.0f} ₽")
c4.metric("🟢 Свободных нод", kpi.get("in_stock", 0))

# График выручки
st.header("📈 Динамика выручки от аренды")
rev_df = load_revenue(days)
if not rev_df.empty:
    fig = px.line(rev_df, x="date", y="total", markers=True, labels={"date": "Дата", "total": "Выручка (₽)"})
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.header("🏆 Популярные тарифы")
    top_df = load_top()
    if not top_df.empty:
        fig = px.bar(top_df, x="count", y="model", color="brand", orientation="h", labels={"count": "Аренд", "model": "Тариф / Сервер"})
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("👔 Загрузка менеджеров")
    mgr_df = load_managers(days)
    if not mgr_df.empty:
        fig = px.pie(mgr_df, values="orders", names="manager")
        st.plotly_chart(fig, use_container_width=True)

# Состояние серверов
st.header("🏢 Статус серверного парка")
stk_df = load_stock()
if not stk_df.empty:
    fig = px.pie(
        stk_df,
        values="count",
        names="status",
        color="status",
        color_discrete_map={
            "available": "#4CAF50",
            "reserved": "#FF9800",
            "rented": "#2196F3",
            "maintenance": "#F44336",
        },
    )
    st.plotly_chart(fig, use_container_width=True)