import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(
    page_title="Manufacturing Dashboard",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Manufacturing Analytics Dashboard")
st.markdown("Analyse des données de production industrielle.")
st.divider()

@st.cache_data
def load_data():
    df = pd.read_csv("data/manufacturing.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

with st.sidebar:
    st.header("🔧 Filtres")
    
    produits = st.multiselect(
        "Produits",
        options=df["product"].unique(),
        default=df["product"].unique()
    )
    
    df_filtered = df[df["product"].isin(produits)]

st.subheader("📊 KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Production totale", f"{df_filtered['production_volume'].sum():,.0f}")
col2.metric("Taux de défaut moyen", f"{df_filtered['defect_rate'].mean():.2%}")
col3.metric("Nombre de défauts", f"{df_filtered['defect_count'].sum():,.0f}")
col4.metric("Température moyenne", f"{df_filtered['temperature'].mean():.1f}°C")


st.divider()
st.subheader("📈 Graphiques")

col_left, col_right = st.columns(2)

with col_left:
    prod_by_product = df_filtered.groupby("product")["production_volume"].sum().reset_index()
    fig1 = px.bar(
        prod_by_product,
        x="product",
        y="production_volume",
        title="Production par produit",
        color="product"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    defect_by_line = df_filtered.groupby("production_line")["defect_rate"].mean().reset_index()
    fig2 = px.bar(
        defect_by_line,
        x="production_line",
        y="defect_rate",
        title="Taux de défaut par ligne",
        color="production_line"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    col_left2, col_right2 = st.columns(2)

with col_left2:
    prod_by_date = df_filtered.groupby("date")["production_volume"].sum().reset_index()
    fig3 = px.line(
        prod_by_date,
        x="date",
        y="production_volume",
        title="Production dans le temps"
    )
    st.plotly_chart(fig3, use_container_width=True)
    
with col_right2:
    defect_types = df_filtered.groupby("defect_type")["defect_count"].sum().reset_index()
    fig4 = px.pie(
        defect_types,
        values="defect_count",
        names="defect_type",
        title="Types de défauts"
    )
    st.plotly_chart(fig4, use_container_width=True)    
