from comum import *

st.header("Meu histórico")
aba_v, aba_g = st.tabs(["Vendas", "Gastos"])
with db() as c:
    v = pd.read_sql_query("SELECT * FROM vendas ORDER BY data DESC, id DESC", c)
    g = pd.read_sql_query("SELECT * FROM gastos ORDER BY data DESC, id DESC", c)
with aba_v:
    if v.empty:
        st.info("Nenhuma venda registrada ainda.")
    else:
        v["lucro"] = (v.valor - v.custo) * v.qtd
        tabela(v.rename(columns={"data": "Data", "produto": "Produto", "valor": "Valor",
                                       "custo": "Custo", "qtd": "Qtd", "pagamento": "Pagamento",
                                       "lucro": "Lucro"}).drop(columns="id"))
        rot = {int(r.id): f"{r.data} · {r.produto} · {brl(r.valor * r.qtd)}" for r in v.itertuples()}
        sel = st.selectbox("Apagar uma venda", [None] + list(rot), format_func=lambda i: "Escolha…" if i is None else rot[i])
        if sel and st.button("Apagar venda"):
            with db() as c:
                c.execute("DELETE FROM vendas WHERE id=?", (sel,))
            st.rerun()
with aba_g:
    if g.empty:
        st.info("Nenhum gasto registrado ainda.")
    else:
        tabela(g.rename(columns={"data": "Data", "descricao": "Gasto", "valor": "Valor"}).drop(columns="id"))
        rot = {int(r.id): f"{r.data} · {r.descricao} · {brl(r.valor)}" for r in g.itertuples()}
        sel = st.selectbox("Apagar um gasto", [None] + list(rot), format_func=lambda i: "Escolha…" if i is None else rot[i])
        if sel and st.button("Apagar gasto"):
            with db() as c:
                c.execute("DELETE FROM gastos WHERE id=?", (sel,))
            st.rerun()