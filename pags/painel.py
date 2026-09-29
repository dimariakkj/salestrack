from comum import *

hoje = date.today().strftime("%Y-%m")
r, ant = resumo(hoje), resumo(mes_anterior(hoje))
st.markdown("""<div class="hero"><span class="tag">📈 Painel do mês</span>
<h1>Você sabe quanto vendeu. Mas sabe quanto realmente ganhou?</h1>
<p>Registre suas vendas e gastos e veja seu lucro de verdade.</p></div>""", unsafe_allow_html=True)
st.markdown(f"""<div class="lucro"><small>💰 Lucro este mês</small><b>{brl(r['lucro'])}</b></div>""",
            unsafe_allow_html=True)
c1, c2 = st.columns(2)
c1.markdown(f"""<div class="card"><small>📈 Vendas</small><b>{brl(r['vendas'])}</b></div>""",
            unsafe_allow_html=True)
c2.markdown(f"""<div class="card"><small>💸 Gastos</small><b>{brl(r['gastos'])}</b></div>""",
            unsafe_allow_html=True)

total_receber, n_receber = a_receber()
if n_receber:
    st.markdown(f"""<div class="card"><small>💳 Clientes devendo ({n_receber})</small>
    <b>{brl(total_receber)}</b></div>""", unsafe_allow_html=True)

st.subheader("Avisos para você")
avisos = []
if ant["gastos"] > 0:
    d = (r["gastos"] / ant["gastos"] - 1) * 100
    if d >= 5:
        avisos.append(f"⚠️ Seus gastos aumentaram {d:.0f}% neste mês.")
    elif d <= -5:
        avisos.append(f"✅ Seus gastos caíram {abs(d):.0f}% neste mês.")
if ant["vendas"] > 0:
    d = (r["vendas"] / ant["vendas"] - 1) * 100
    if d >= 5:
        avisos.append(f"📈 Você vendeu {d:.0f}% mais que no mês passado.")
    elif d <= -5:
        avisos.append(f"📉 Você vendeu {abs(d):.0f}% menos que no mês passado.")
if r["n"]:
    avisos.append(f"💰 Seu lucro médio por venda é {brl(r['lucro_medio'])}.")
if r["lucro"] < 0:
    avisos.append("🔴 Neste mês você gastou mais do que vendeu.")
for a in avisos or ["Registre sua primeira venda para ver os avisos aqui."]:
    st.markdown(f'<div class="alerta">{a}</div>', unsafe_allow_html=True)

st.subheader("Gráficos de lucro")
opcoes = ["Diário", "Semanal", "Mensal", "Projeção"]
icones = {"Diário": "☀️ Diário", "Semanal": "🗓️ Semanal", "Mensal": "📅 Mensal", "Projeção": "🔮 Projeção"}
ver = st.pills("Toque para mostrar ou esconder cada gráfico:", opcoes, selection_mode="multi",
               default=opcoes, format_func=lambda o: icones[o])
if not ver:
    st.info("Escolha pelo menos uma opção acima para ver os gráficos.")

if "Diário" in ver:
    st.subheader("Lucro por dia")
    diario = lucro_diario()
    if diario is None:
        st.info("Registre suas vendas para ver o lucro de cada dia.")
    else:
        st.markdown(f"""<div class="card"><small>☀️ Lucro de hoje</small>
        <b>{brl(diario.iloc[-1, 0])}</b></div>""", unsafe_allow_html=True)
        grafico(diario, "bar", [GREEN])
        st.caption("Últimos 14 dias.")

if "Semanal" in ver:
    st.subheader("Lucro por semana")
    semanal = lucro_semanal()
    if semanal is None:
        st.info("Registre suas vendas para ver o lucro de cada semana.")
    else:
        st.markdown(f"""<div class="card"><small>🗓️ Lucro desta semana (desde segunda-feira)</small>
        <b>{brl(semanal.iloc[-1, 0])}</b></div>""", unsafe_allow_html=True)
        grafico(semanal, "bar", [GREEN])
        st.caption("Cada barra é uma semana, de segunda a domingo. A data embaixo é o dia em que a semana começou.")

if "Mensal" in ver:
    st.subheader("Lucro por mês")
    meses = [mes_anterior(hoje, k) for k in range(5, -1, -1)]
    df = pd.DataFrame({"Mês": meses, "Lucro (R$)": [resumo(m)["lucro"] for m in meses]}).set_index("Mês")
    grafico(df, "bar", [GREEN])
    st.caption("Últimos 6 meses.")

if "Projeção" in ver:
    st.subheader("Projeção de lucro")
    proj = projecao_lucro()
    if not proj:
        st.info("Registre suas vendas para ver a projeção do seu lucro.")
    else:
        st.markdown(f"""<div class="card"><small>📅 Neste ritmo, você fecha este mês com</small>
        <b>{brl(proj['fechamento'])}</b></div>""", unsafe_allow_html=True)
        if proj["grafico"] is None:
            st.info("Com 3 meses de vendas registradas, mostramos também a tendência dos próximos meses.")
        else:
            grafico(proj["grafico"], "line", [GREEN, AZUL])
            st.caption("Verde: lucro real. Azul: projeção dos próximos 3 meses, calculada pela tendência dos seus "
                       "últimos meses. É uma estimativa e pode mudar conforme você vende.")