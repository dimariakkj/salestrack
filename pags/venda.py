from comum import *

st.header("Registrar venda")
st.caption("Leva poucos segundos.")
mostrar_aviso()
st.text_input("O que você vendeu?", key="v_produto", placeholder="Ex.: Camisa")
c1, c2 = st.columns(2)
c1.number_input("Por quanto você vendeu? (R$)", min_value=0.0, step=1.0, key="v_valor")
c2.number_input("Quanto você pagou nisso? (R$)", min_value=0.0, step=1.0, key="v_custo",
                help="O que você gastou para comprar ou fazer o produto.")
c3, c4 = st.columns(2)
c3.number_input("Quantas unidades?", min_value=1, step=1, key="v_qtd", value=1)
c4.selectbox("Como o cliente pagou?", PAGAMENTOS, key="v_pag")
st.date_input("Quando foi?", value=date.today(), key="v_data", format="DD/MM/YYYY")

s = st.session_state
lucro = (s.get("v_valor", 0) - s.get("v_custo", 0)) * s.get("v_qtd", 1)
if s.get("v_valor", 0) > 0:
    (st.success if lucro >= 0 else st.error)(f"→ Lucro desta venda: **{brl(lucro)}**")
st.button("Salvar venda", on_click=salvar_venda)