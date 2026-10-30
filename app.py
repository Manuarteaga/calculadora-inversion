import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Capacidad de Inversión",
    page_icon="📈",
    layout="centered",
)

st.title("📈 Calculadora de Capacidad de Inversión")
st.markdown(
    "Calcula fácilmente cuánto dinero disponible te queda al mes para destinar a "
    "**fondos indexados, ETFs** u otros instrumentos de inversión."
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

    # Cálculo del neto anual y prorrateo a 12 meses para el presupuesto mensual
    bruto_mensual = sueldo_bruto_anual / num_pagas
    neto_por_paga = bruto_mensual * (1 - (irpf_pct / 100))
    ingreso_neto_mensual = (neto_por_paga * num_pagas) / 12

    st.caption(
        f"💡 Tu ingreso neto mensual estimado (promedio a 12 meses) es: **{ingreso_neto_mensual:,.2f} €**"
    )

st.markdown("---")

# 2. SECCIÓN DE GASTOS FIJOS Y VARIABLES
st.header("2. Gastos Mensuales")

with st.expander("🏠 Vivienda y Suministros", expanded=True):
    col_alquiler, col_luz, col_agua = st.columns(3)
    with col_alquiler:
        g_vivienda = st.number_input(
            "Hipoteca / Alquiler (€):", min_value=0.0, value=700.0, step=10.0
        )
    with col_luz:
        g_luz = st.number_input(
            "Factura de Luz (€):", min_value=0.0, value=60.0, step=5.0
        )
    with col_agua:
        g_agua_gas = st.number_input(
            "Agua / Gas (€):", min_value=0.0, value=40.0, step=5.0
        )

with st.expander("📱 Telecomunicaciones y Suscripciones", expanded=True):
    col_tel, col_stream = st.columns(2)
    with col_tel:
        g_internet_tel = st.number_input(
            "Internet / Teléfono (€):", min_value=0.0, value=45.0, step=5.0
        )
    with col_stream:
        g_streaming = st.number_input(
            "Streaming (Netflix, Prime... €):",
            min_value=0.0,
            value=25.0,
            step=5.0,
        )

with st.expander("🛒 Vida Diaria y Otros Gastos", expanded=False):
    col_comida, col_otros = st.columns(2)
    with col_comida:
        g_comida = st.number_input(
            "Alimentación y Compra (€):", min_value=0.0, value=300.0, step=10.0
        )
    with col_otros:
        g_otros = st.number_input(
            "Otros gastos variados (€):", min_value=0.0, value=150.0, step=10.0
        )

gastos_totales = (
    g_vivienda + g_luz + g_agua_gas + g_internet_tel + g_streaming + g_comida + g_otros
)

st.markdown("---")

# 3. RESULTADOS
st.header("3. Resumen y Capacidad de Inversión")

disponible_inversion = ingreso_neto_mensual - gastos_totales
tasa_ahorro = (
    (disponible_inversion / ingreso_neto_mensual * 100)
    if ingreso_neto_mensual > 0
    else 0.0
)

col_res1, col_res2, col_res3 = st.columns(3)

col_res1.metric(
    label="Ingreso Neto Mensual", value=f"{ingreso_neto_mensual:,.2f} €"
)
col_res2.metric(
    label="Gastos Totales",
    value=f"{gastos_totales:,.2f} €",
    delta=f"-{gastos_totales:,.2f} €",
    delta_color="inverse",
)
col_res3.metric(
    label="Disponible para Invertir",
    value=f"{disponible_inversion:,.2f} €",
    delta=f"{tasa_ahorro:.1f}% de tu sueldo",
    delta_color="normal" if disponible_inversion >= 0 else "inverse",
)

if disponible_inversion > 0:
    st.success(
        f"🎯 ¡Tienes **{disponible_inversion:,.2f} €** disponibles cada mes! "
        "Es un excelente capital para hacer aportaciones periódicas (DCA) en tus fondos indexados (MSCI World, S&P 500) o ETFs."
    )
elif disponible_inversion == 0:
    st.warning(
        "⚖️ Estás ingresando exactamente lo mismo que gastas. Revisa tus suscripciones o gastos secundarios para liberar margen de inversión."
    )
else:
    st.error(
        f"⚠️ Tus gastos superan a tus ingresos por **{abs(disponible_inversion):,.2f} €**. "
        "Necesitas ajustar tu presupuesto antes de empezar a invertir."
    )
