"""Riverside Food Bank — Pulse
A tiny Databricks App (Streamlit) over the bootcamp dataset.
Shows headline numbers, meals over time, and donations by category,
with a site filter. Read-only.
"""
import os

import pandas as pd
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config

st.set_page_config(page_title="Riverside Food Bank — Pulse", page_icon="🥫", layout="wide")

cfg = Config()  # picks up the app's OAuth credentials automatically
WAREHOUSE_ID = os.getenv("DATABRICKS_WAREHOUSE_ID")
HTTP_PATH = f"/sql/1.0/warehouses/{WAREHOUSE_ID}"
CATALOG, SCHEMA = "workspace", "foodbank"


@st.cache_resource
def _connection():
    return sql.connect(
        server_hostname=cfg.host,
        http_path=HTTP_PATH,
        credentials_provider=lambda: cfg.authenticate,
    )


@st.cache_data(ttl=300)
def q(query: str) -> pd.DataFrame:
    with _connection().cursor() as cur:
        cur.execute(query)
        cols = [c[0] for c in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=cols)


st.title("🥫 Riverside Food Bank — Pulse")
st.caption("Live view of donations and distributions. Built at the Philanthrobricks bootcamp.")

# --- Site filter ---
sites = q(f"SELECT DISTINCT site FROM {CATALOG}.{SCHEMA}.distributions ORDER BY site")["site"].tolist()
choice = st.selectbox("Site", ["All sites"] + sites)
where = "" if choice == "All sites" else f"WHERE site = '{choice}'"

# --- Headline numbers ---
kpis = q(f"""
    SELECT sum(meals_served) AS meals, sum(households_served) AS households, count(*) AS sessions
    FROM {CATALOG}.{SCHEMA}.distributions {where}
""").iloc[0]
c1, c2, c3 = st.columns(3)
c1.metric("Meals served", f"{int(kpis.meals):,}")
c2.metric("Households reached", f"{int(kpis.households):,}")
c3.metric("Distribution sessions", f"{int(kpis.sessions):,}")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Meals served per month")
    meals = q(f"""
        SELECT date_trunc('month', distribution_date) AS month, sum(meals_served) AS meals
        FROM {CATALOG}.{SCHEMA}.distributions {where}
        GROUP BY month ORDER BY month
    """)
    st.line_chart(meals, x="month", y="meals")

with right:
    st.subheader("Donations by category (kg)")
    cats = q(f"""
        SELECT food_category, round(sum(weight_kg)) AS total_kg
        FROM {CATALOG}.{SCHEMA}.donations
        GROUP BY food_category ORDER BY total_kg DESC
    """)
    st.bar_chart(cats, x="food_category", y="total_kg")
