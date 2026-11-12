import streamlit as st
import duckdb

st.set_page_config(page_title="Balkan Power & Weather", layout="wide")
st.title("Power & Weather ELT Pipeline")

@st.cache_data
def load_data():
    con = duckdb.connect("warehouse.duckdb")
    df = con.sql("SELECT * FROM main.fct_power_weather ORDER BY time_hour DESC").df()
    con.close()
    return df

df = load_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Combined data (dbt fact table)")
    st.dataframe(df.head(24))

with col2:
    st.subheader("Price trend (EUR/MWh)")
    if not df.empty:
        st.line_chart(data=df, x="time_hour", y="price_eur_mwh")