import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Capacidad de Inversión y Cartera",
    page_icon="📈",
    layout="centered",
)

st.title("📈 Calculadora de Capacidad de Inversión y Propuesta de Cartera")
st.markdown(
    "Calcula cuánto dinero disponible te queda al mes y obtén una propuesta de distribución "
    "de tu ahorro adaptada a diferentes clases de activos (incluyendo letras/bonos) y cuentas remuneradas."
)

st.markdown("---")

# 1. SECCIÓN DE INGRESOS
st.header("1. Ingresos Mensuales")

tipo_ingreso = st.radio(
    "¿Cómo quieres introducir tu sueldo?",
    options=["Neto (lo que te llega al banco)", "Bruto anual"],
    horizontal=True,
)

ingreso_neto_mensual = 0.0

if tipo_ingreso == "Neto (lo que te llega al banco)":
    ingreso_neto_mensual = st.number_input(
        "Sueldo neto mensual (€):",
        min_value=0.0,
        value=2000.0,
        step=50.0,
        format="%.2f",
    )
else:
    col_bruto, col_irpf, col_pagas = st.columns(3)
    with col_bruto:
        sueldo_bruto_anual = st.number_input(
            "Sueldo bruto anual (€):",
            min_value=0.0,
            value=30000.0,
            step=500.0,
            format="%.2f",
        )
    with col_irpf:
        irpf_pct = st.number_input(
            "Retención IRPF + Seg. Soc. (%):",
            min_value=0.0,
            max_value=50.0,
            value=19.0,
            step=0.5,
            format="%.1f",
        )
    with col_pagas:
        num_pagas = st.selectbox(
            "Número de pagas:", options=[12, 14], index=0
        )

    bruto_mensual = sueldo_bruto_anual / num_pagas
    neto_por_paga
