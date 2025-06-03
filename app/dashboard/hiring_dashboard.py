import streamlit as st
import pandas as pd

from app.reports.hiring_quarterly_report import get_hiring_quarterly_report
from app.reports.hiring_above_average import generate_hiring_above_average_report

st.set_page_config(page_title="Hiring Dashboard", layout="wide")

st.markdown("<h1 style='text-align: center;'>📊 Hiring Dashboard (2021)</h1>", unsafe_allow_html=True)

# Report 1
st.header("📌 Hires by Department and Job per Quarter")
df_quarterly = get_hiring_quarterly_report().toPandas()
st.dataframe(df_quarterly)

# Report 2
st.header("🚀 Departments with Above Average Hiring")
df_above_avg = generate_hiring_above_average_report().toPandas()
st.dataframe(df_above_avg)
st.bar_chart(df_above_avg.set_index("department")["hired"])
