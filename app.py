import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página (Estilo Oscuro Dashboard)
st.set_page_config(page_title="Dashboard Comercial Pro", page_icon="📊", layout="wide")

# Estilos CSS personalizados para simular la estética de la imagen de referencia (Dark Theme)
st.markdown("""
    <style>
    .main {
        background-color: #0F111A;
    }
    .kpi-card {
        background-color: #1A1D2E;
        border: 1px solid #2D3748;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .kpi-title {
        color: #9CA3AF;
        font-size: 14px;
        font-weight: 600;
    }
    .kpi-value {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: bold;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar los datos (Asegúrate de que tu archivo se llame Ventas.xlsx o usa la versión CSV)
@st.cache_data
def load_data():
    # Intenta leer el archivo Excel; si tienes el CSV, puedes cambiarlo aquí
    df = pd.read_excel("Ventas.xlsx")
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['AÑO'] = df['Fecha'].dt.year
    df['MES'] = df['Fecha'].dt.strftime('%Y-%m')
    df['UTILIDAD'] = df['TOTAL'] - df['Total de Costo']
    df['MARGEN_%'] = df['UTILIDAD'] / df['TOTAL']
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"No se encontró el archivo 'Ventas.xlsx' en la carpeta. Colócalo junto a este script. Detalle: {e}")
    st.stop()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("🎯 Filtros Interactivos")
anos = sorted(df['AÑO'].unique())
selected_ano = st.sidebar.selectbox("Filtrar por Año", options=["Todos"] + list(anos))

if selected_ano != "Todos":
    df_filtered = df[df['AÑO'] == selected_ano]
else:
    df_filtered = df

categorias = sorted(df_filtered['CATEGORIA'].unique())
selected_cat = st.sidebar.selectbox("Filtrar por Categoría", options=["Todas"] + list(categorias))

if selected_cat != "Todas":
    df_filtered = df_filtered[df_filtered['CATEGORIA'] == selected_cat]

# --- TÍTULO PRINCIPAL ---
st.title("📊 Dashboard Comercial — Panel de Control")
st.markdown("---")

# --- CÁLCULOS DE KPIs ---
total_ventas = df_filtered['TOTAL'].sum()
total_utilidad = df_filtered['UTILIDAD'].sum()
margen_promedio = (total_utilidad / total_ventas) if total_ventas > 0 else 0
total_unidades = df_filtered['CANTIDAD'].sum()
total_operaciones = len(df_filtered)
venta_promedio = (total_ventas / total_operaciones) if total_operaciones > 0 else 0

# --- MOSTRAR TARJETAS KPI (Estilo Fila Superior) ---
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">VENTAS TOTALES</div><div class="kpi-value">${total_ventas:,.2f}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">UTILIDAD BRUTA</div><div class="kpi-value">${total_utilidad:,.2f}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">MARGEN BRUTO</div><div class="kpi-value">{margen_promedio:.1%}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">UNIDADES</div><div class="kpi-value">{total_unidades:,}</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">OPERACIONES</div><div class="kpi-value">{total_operaciones:,}</div></div>', unsafe_allow_html=True)
with col6:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">TICKET PROMEDIO</div><div class="kpi-value">${venta_promedio:,.2f}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- GRÁFICOS INTERACTIVOS (Plotly Dark Theme) ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📈 Evolución de Ventas por Mes")
    df_mensual = df_filtered.groupby('MES', as_index=False)['TOTAL'].sum()
    fig_line = px.line(df_mensual, x='MES', y='TOTAL', markers=True, template="plotly_dark", color_discrete_sequence=["#3B82F6"])
    fig_line.update_layout(plot_bgcolor="#1A1D2E", paper_bgcolor="#0F111A")
    st.plotly_chart(fig_line, use_container_width=True)

with col_g2:
    st.subheader("📊 Ventas por Categoría")
    df_cat = df_filtered.groupby('CATEGORIA', as_index=False)['TOTAL'].sum()
    fig_bar = px.bar(df_cat, x='CATEGORIA', y='TOTAL', template="plotly_dark", color_discrete_sequence=["#9333EA"])
    fig_bar.update_layout(plot_bgcolor="#1A1D2E", paper_bgcolor="#0F111A")
    st.plotly_chart(fig_bar, use_container_width=True)

col_g3, col_g4 = st.columns(2)

with col_g3:
    st.subheader("🏆 Top 5 Productos por Facturación")
    df_prod = df_filtered.groupby('PRODUCTO', as_index=False)['TOTAL'].sum().sort_values(by='TOTAL', ascending=True).tail(5)
    fig_prod = px.bar(df_prod, x='TOTAL', y='PRODUCTO', orientation='h', template="plotly_dark", color_discrete_sequence=["#EC4899"])
    fig_prod.update_layout(plot_bgcolor="#1A1D2E", paper_bgcolor="#0F111A")
    st.plotly_chart(fig_prod, use_container_width=True)

with col_g4:
    st.subheader("🏢 Ventas por Marca")
    df_brand = df_filtered.groupby('MARCA', as_index=False)['TOTAL'].sum().sort_values(by='TOTAL', ascending=False)
    fig_brand = px.bar(df_brand, x='MARCA', y='TOTAL', template="plotly_dark", color_discrete_sequence=["#3B82F6"])
    fig_brand.update_layout(plot_bgcolor="#1A1D2E", paper_bgcolor="#0F111A")
    st.plotly_chart(fig_brand, use_container_width=True)

# --- TABLA DE DETALLE ---
st.markdown("---")
st.subheader("📋 Detalle de Operaciones y Ranking")
st.dataframe(df_filtered[['Fecha', 'CATEGORIA', 'PRODUCTO', 'MARCA', 'CANTIDAD', 'TOTAL', 'UTILIDAD']], use_container_width=True)