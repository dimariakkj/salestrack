from comum import *

st.header("Registrar gasto")
mostrar_aviso()
st.text_input("O que você gastou?", key="g_desc", placeholder="Ex.: Gasolina, embalagem, internet")
st.number_input("Quanto foi? (R$)", min_value=0.0, step=1.0, key="g_valor")
st.date_input("Quando foi?", value=date.today(), key="g_data", format="DD/MM/YYYY")
st.button("Salvar gasto", on_click=salvar_gasto)