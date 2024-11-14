import streamlit as st       # BIBLIOTECA PARA DASHBOARDS
import pandas as pd          # BIBLIOTECA PARA DADOS
import plotly.express as px  # bIBLIOTECA PARA GRÁFICOS

st.set_page_config(layout="wide")

st.title("Dashboard de Faturamento do Supermercado")
st.markdown("Este dashboard apresenta uma visão detalhada das vendas e do desempenho do supermercado, permitindo análises por mês, filial e tipo de pagamento.")

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

df["Month"] = df["Date"].apply(lambda x: f"{x.year}-{x.month}")
month = st.sidebar.selectbox("Mês", df["Month"].unique())
city = st.sidebar.selectbox("Cidade", df["City"].unique())
product_line = st.sidebar.multiselect("Tipo de Produto", df["Product line"].unique())

df_filtered = df[(df["Month"] == month) & (df["City"] == city) & (df["Product line"].isin(product_line))]

# Colunas para gráficos
col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

# Gráficos
custom_colors = ["#FF204E", "#A0153E", "#5D0E41", "#AB63FA", "#FFA15A", "#19D3F3", "#FF6692"]

# Gráfico Faturamento por Dia
col1.header("Faturamento por Dia")
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por Dia", color_discrete_sequence=custom_colors)
col1.plotly_chart(fig_date, use_container_width=True)

# Gráfico Faturamento por Tipo de Produto
col2.header("Faturamento por Tipo de Produto")
fig_prod = px.bar(df_filtered, x="Date", y="Product line", color="City", title="Faturamento por Tipo de Produto", orientation="h", color_discrete_sequence=custom_colors)
col2.plotly_chart(fig_prod, use_container_width=True)

# Gráfico Faturamento por Filial
col3.header("Faturamento por Filial")
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", color="City", title="Faturamento por Filial", color_discrete_sequence=custom_colors)
col3.plotly_chart(fig_city, use_container_width=True)

# Gráfico Faturamento por Tipo de Pagamento
col4.header("Faturamento por Tipo de Pagamento")
fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por Tipo de Pagamento", color_discrete_sequence=custom_colors)
col4.plotly_chart(fig_kind, use_container_width=True)

# Gráfico Avaliação
col5.header("Avaliação por Cidade")
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(city_rating, x="City", y="Rating", color="City", title="Avaliação", color_discrete_sequence=custom_colors)
col5.plotly_chart(fig_rating, use_container_width=True)

# Botão para baixar dados
if st.button("Baixar Dados Filtrados"):
    df_filtered.to_csv("dados_filtrados.csv", index=False)
    st.success("Arquivo baixado com sucesso!")

# python -m streamlit run dashboard.py