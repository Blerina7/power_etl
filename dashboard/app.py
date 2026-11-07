import streamlit as st
import duckdb
import pandas as pd

# Konfigurimi i faqes
st.set_page_config(page_title="Balkan Power & Weather", layout="wide")
st.title(" Pipeline ELT: Çmimet e Energjisë & Moti")

# Funksioni për të tërhequr të dhënat nga dbt (Marts)
@st.cache_data
def load_data():
    con = duckdb.connect('warehouse.duckdb')
    # Lexojmë tabelën përfundimtare nga dbt
    df = con.sql("SELECT * FROM main.fct_power_weather ORDER BY time_hour DESC").df()
    con.close()
    return df

df = load_data()

# Shfaqja e të dhënave
col1, col2 = st.columns(2)

with col1:
    st.subheader("Të dhënat e bashkuara (dbt Fact Table)")
    st.dataframe(df.head(24)) # Tregojmë 24 orët e fundit

with col2:
    st.subheader("Trendi i Çmimeve (EUR/MWh)")
    if not df.empty:
        # Grafiku i thjeshtë për çmimet
        st.line_chart(data=df, x='time_hour', y='price_eur_mwh')