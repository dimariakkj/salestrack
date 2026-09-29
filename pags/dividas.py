from comum import *

st.header("Dívidas de clientes")
st.caption("Anote quem ficou de pagar depois (fiado) e marque quando pagarem.")
mostrar_aviso()

total, n = a_receber()
st.markdown(f"""<div class="lucro"><small>💳 Total a receber</small><b>{brl(total)}</b>
<small>{n} dívida(s) em aberto</small></div>""", unsafe_allow_html=True)

with st.expander("➕ Anotar nova dívida", expanded=(n == 0)):
    st.text_input("Nome do cliente", key="d_cliente", placeholder="Ex.: Maria")
    st.text_input("O que ele levou?", key="d_desc", placeholder="Ex.: 2 camisas")
    c1, c2 = st.columns(2)
    c1.number_input("Quanto ele deve? (R$)", min_value=0.0, step=1.0, key="d_valor")
    c2.date_input("Vai pagar até quando? (opcional)", value=None, key="d_venc", format="DD/MM/YYYY")
    st.button("Salvar dívida", on_click=salvar_divida)

st.subheader("Quem está devendo")
with db() as c:
    abertas = pd.read_sql_query(
        "SELECT * FROM dividas WHERE pago=0 ORDER BY vencimento IS NULL, vencimento, id", c)
    pagas = pd.read_sql_query("SELECT * FROM dividas WHERE pago=1 ORDER BY data_pago DESC, id DESC", c)

if abertas.empty:
    st.info("Ninguém está devendo. 🎉")
hoje_iso = date.today().isoformat()
for r in abertas.itertuples():
    venc = r.vencimento if isinstance(r.vencimento, str) and r.vencimento else None
    detalhe = (r.descricao or "Sem descrição") + " · anotado em " + date.fromisoformat(r.data).strftime("%d/%m/%Y")
    if venc:
        detalhe += " · paga até " + date.fromisoformat(venc).strftime("%d/%m/%Y")
    with st.container(border=True):
        col1, col2, col3 = st.columns([4, 1.4, 1])
        atraso = "  ⚠️ **atrasada**" if venc and venc < hoje_iso else ""
        col1.markdown(f"**{r.cliente}** · {brl(r.valor)}{atraso}")
        col1.caption(detalhe)
        if col2.button("Já pagou", key=f"pago_{int(r.id)}"):
            with db() as c:
                c.execute("UPDATE dividas SET pago=1, data_pago=? WHERE id=?", (hoje_iso, int(r.id)))
            st.rerun()
        if col3.button("🗑️", key=f"del_{int(r.id)}", help="Apagar esta dívida"):
            with db() as c:
                c.execute("DELETE FROM dividas WHERE id=?", (int(r.id),))
            st.rerun()

if not pagas.empty:
    with st.expander(f"✅ Já pagas ({len(pagas)})"):
        tabela(pagas.rename(columns={"cliente": "Cliente", "descricao": "O que levou", "valor": "Valor",
                                           "data_pago": "Pago em"})[["Cliente", "O que levou", "Valor", "Pago em"]])