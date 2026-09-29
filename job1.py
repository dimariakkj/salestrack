import streamlit as st

from comum import LOGO, estilo, init

st.set_page_config(page_title="SalesTrack", page_icon=str(LOGO) if LOGO.exists() else "📈")
init()
estilo()

if LOGO.exists():
    try:
        st.logo(str(LOGO), size="large")
    except TypeError:
        st.logo(str(LOGO))

pagina = st.navigation([
    st.Page("pags/sobre.py", title="Sobre nós", icon="ℹ️", default=True),
    st.Page("pags/painel.py", title="Meu painel", icon="📈"),
    st.Page("pags/venda.py", title="Registrar venda", icon="🛒"),
    st.Page("pags/gasto.py", title="Registrar gasto", icon="💸"),
    st.Page("pags/dividas.py", title="Dívidas de clientes", icon="💳"),
    st.Page("pags/historico.py", title="Meu histórico", icon="📋"),
])
st.sidebar.caption("Você sabe quanto vendeu. Mas sabe quanto realmente ganhou?")
st.sidebar.toggle("🌙 Modo escuro", key="escuro")
pagina.run()