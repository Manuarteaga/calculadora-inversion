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
    "de tu ahorro adaptada a diferentes clases de activos y cuentas remuneradas."
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
            "Otros gastos variados (€):", min_value=0.0, value=150.0, step=5.0
        )

gastos_totales = (
    g_vivienda + g_luz + g_agua_gas + g_internet_tel + g_streaming + g_comida + g_otros
)

st.markdown("---")

# 3. RESULTADOS DE CAPACIDAD DE INVERSIÓN
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

st.markdown("---")

# 4. PROPUESTA DE DISTRIBUCIÓN DE CARTERA Y CUENTA REMUNERADA
st.header("4. Propuesta de Distribución y Remuneración del Ahorro")

if disponible_inversion <= 0:
    st.warning(
        "⚠️ No tienes capital disponible para invertir según tus ingresos y gastos actuales. "
        "Aun así, puedes ajustar los porcentajes de abajo de manera simulada."
    )

st.subheader("Configuración de Cuenta Remunerada")
tiene_cuenta_rem = st.radio(
    "¿Tienes cuenta remunerada?", options=["No", "Sí"], horizontal=True
)

tae_seleccionada = 0.0
plataforma_elegida = "Ninguna"

if tiene_cuenta_rem == "Sí":
    plataformas_taes = {
        "Trade Republic": 2.25,
        "N26": 2.26,
        "Revolut (Flex)": 2.50,
        "BFF (Cuenta Facto)": 3.00,
        "EBN Banco": 3.00,
        "MyInvestor": 2.50,
        "Otra / Personalizada": 2.00,
    }
    
    col_plt, col_tae_custom = st.columns(2)
    with col_plt:
        plataforma_elegida = st.selectbox(
            "Selecciona tu plataforma:", options=list(plataformas_taes.keys())
        )
    
    if plataforma_elegida == "Otra / Personalizada":
        with col_tae_custom:
            tae_seleccionada = st.number_input(
                "Introduce la TAE (%):", min_value=0.0, max_value=10.0, value=2.0, step=0.1
            )
    else:
        tae_seleccionada = plataformas_taes[plataforma_elegida]
        with col_tae_custom:
            st.metric(label="TAE Aplicada automáticamente", value=f"{tae_seleccionada:.2f}%")

st.markdown("### Reparto porcentual de tu capital mensual")
st.markdown("Personaliza los porcentajes para que sumen el **100%**:")

col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)

with col_p1:
    p_fondos_ind = st.slider("Fondos Indexados (%)", 0, 100, 50, step=5)
with col_p2:
    p_etfs = st.slider("ETFs (%)", 0, 100, 20, step=5)
with col_p3:
    p_monetarios = st.slider("Fondos Monetarios (%)", 0, 100, 10, step=5)
with col_p4:
    p_acciones = st.slider("Acciones (%)", 0, 100, 10, step=5)
with col_p5:
    p_remunerada = st.slider("Cuenta Remunerada (%)", 0, 100, 10, step=5)

suma_porcentajes = p_fondos_ind + p_etfs + p_monetarios + p_acciones + p_remunerada

if suma_porcentajes != 100:
    st.error(f"❌ Los porcentajes suman **{suma_porcentajes}%**. Deben sumar exactamente **100%** para ver los cálculos detallados.")
else:
    st.success("✅ Los porcentajes suman 100 correctamente.")
    
    # Importes mensuales destinados a cada activo
    imp_fondos = disponible_inversion * (p_fondos_ind / 100)
    imp_etfs = disponible_inversion * (p_etfs / 100)
    imp_monetarios = disponible_inversion * (p_monetarios / 100)
    imp_acciones = disponible_inversion * (p_acciones / 100)
    imp_remunerada = disponible_inversion * (p_remunerada / 100)

    st.markdown("---")
    st.subheader("📊 Desglose de Inversión Mensual")
    
    col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns(5)
    col_d1.metric("Fondos Indexados", f"{imp_fondos:,.2f} €", f"{p_fondos_ind}%")
    col_d2.metric("ETFs", f"{imp_etfs:,.2f} €", f"{p_etfs}%")
    col_d3.metric("Monetarios", f"{imp_monetarios:,.2f} €", f"{p_monetarios}%")
    col_d4.metric("Acciones", f"{imp_acciones:,.2f} €", f"{p_acciones}%")
    col_d5.metric("Cta. Remunerada", f"{imp_remunerada:,.2f} €", f"{p_remunerada}%")

    # Proyección de la cuenta remunerada
    if p_remunerada > 0 and tiene_cuenta_rem == "Sí" and disponible_inversion > 0:
        st.markdown("---")
        st.subheader(f"💰 Proyección de Rendimiento: Cuenta Remunerada ({plataforma_elegida} - {tae_seleccionada}% TAE)")
        
        temporalidad = st.selectbox(
            "Selecciona la temporalidad para calcular los intereses generados por la parte de la cuenta remunerada:",
            options=["1 Año", "3 Años", "5 Años"],
            index=0
        )
        
        años = 1 if temporalidad == "1 Año" else (3 if temporalidad == "3 Años" else 5)
        
        # Interés compuesto simple aproximado aportando mes a mes
        # Fórmula aproximada de capitalización con aportaciones mensuales regulares
        tae_decimal = tae_seleccionada / 100
        interes_acumulado = 0.0
        capital_total_remunerado = 0.0
        
        for mes in range(1, (años * 12) + 1):
            capital_total_remunerado += imp_remunerada
            # Interés mensual aplicado al capital acumulado hasta el momento
            interes_mes = capital_total_remunerado * (tae_decimal / 12)
            interes_acumulado += interes_mes
            capital_total_remunerado += interes_mes

        col_pr1, col_pr2, col_pr3 = st.columns(3)
        col_pr1.metric("Aportación Total Acumulada", f"{(imp_remunerada * 12 * años):,.2f} €")
        col_pr2.metric(f"Intereses Brutos Generados ({temporalidad})", f"{interes_acumulado:,.2f} €")
        col_pr3.metric("Capital Final en Cta. Remunerada", f"{capital_total_remunerado:,.2f} €")
        
        st.info(
            f"💡 Gracias a destinar un **{p_remunerada}%** mensual ({imp_remunerada:,.2f} €/mes) a tu cuenta remunerada en **{plataforma_elegida}** al **{tae_seleccionada}% TAE**, "
            f"conseguirás un rendimiento bruto aproximado de **{interes_acumulado:,.2f} €** en un plazo de **{temporalidad}**."
        )
