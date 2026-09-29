from comum import *

st.markdown("""<div class="hero"><span class="tag">Sobre nós</span>
<h1>Controle financeiro simples para quem trabalha por conta própria</h1>
<p>O SalesTrack existe para responder, em poucos toques, uma pergunta que muita gente não sabe responder:
quanto eu realmente ganhei?</p></div>""", unsafe_allow_html=True)

st.subheader("Por que criamos o SalesTrack")
st.write("Vendedores, ambulantes, freelancers e prestadores de serviço vendem todos os dias, mas quase sempre "
         "misturam o dinheiro do trabalho com o dinheiro pessoal e não sabem quanto sobra no fim do mês. "
         "Os sistemas que existem costumam ser cheios de termos difíceis. Nós fizemos o contrário: "
         "um sistema que qualquer pessoa entende, mesmo sem saber nada de finanças.")

st.subheader("Nossos diferenciais")
cards([("⚡", "Registro rápido", "Registre uma venda em poucos segundos: produto, valor, custo e forma de pagamento."),
       ("💰", "Lucro automático", "O sistema calcula o lucro de cada venda e do mês inteiro. Sem fórmulas, sem planilhas."),
       ("📊", "Dashboard simples", "O lucro aparece logo na tela inicial, com vendas e gastos ao lado.")])
cards([("🎯", "Foco em autônomos", "Pensado para quem trabalha por conta própria, não para grandes empresas."),
       ("💬", "Linguagem simples", "Sem DRE, competência ou centro de custo. Perguntas do dia a dia, como \"O que você gastou?\"."),
       ("🔔", "Análise de desempenho", "Avisos como \"seus gastos aumentaram 25%\" ou \"você vendeu 18% mais que no mês passado\".")])

st.subheader("Vantagens de usar o SalesTrack")
cards([("✅", "Saiba seu lucro real", "Descubra quanto sobra de verdade depois de descontar custos e gastos."),
       ("🧭", "Decida com mais segurança", "Veja o que dá mais lucro e quando os gastos estão saindo do controle."),
       ("⏱️", "Ganhe tempo", "Tudo em um só lugar, sem caderninho, sem conta de cabeça e sem planilha complicada.")])

st.subheader("Como funciona")
passos = [("1", "Registre suas vendas", "Diga o que vendeu, por quanto e quanto pagou nisso."),
          ("2", "Anote seus gastos", "Gasolina, embalagem, internet... tudo que saiu do seu bolso."),
          ("3", "Veja seu lucro", "O painel mostra o lucro do mês e avisos para você agir.")]
for col, (n, t, d) in zip(st.columns(3), passos):
    col.markdown(f'<div class="feat"><span class="passo">{n}</span><h4>{t}</h4><p>{d}</p></div>',
                 unsafe_allow_html=True)

st.subheader("Sistemas complicados x SalesTrack")
st.markdown("""
| Em sistemas complicados | No SalesTrack |
|---|---|
| "Lançamento de despesa" | "O que você gastou?" |
| "Receita operacional" | "Quanto você recebeu?" |
| DRE, competência, centro de custo | Só vendas, gastos e lucro |
| Telas cheias de menus | Lucro logo na tela inicial |
""")

st.subheader("Para quem é")
st.write("Vendedores de roupas, alimentos e cosméticos · ambulantes · freelancers · fotógrafos · designers · "
         "eletricistas · barbeiros · manicures · prestadores de serviço · MEIs e pequenos comerciantes.")

st.markdown('<div class="cta">Pronto para descobrir quanto você realmente ganha?</div>', unsafe_allow_html=True)
if st.button("Registrar minha primeira venda"):
    st.switch_page("pags/venda.py")