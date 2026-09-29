import calendar
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

BASE = Path(__file__).parent
DB = BASE / "salestrack.db"
LOGO = BASE / "logo.png"
NAVY, GREEN, GREEN_DARK = "#0B1B2E", "#12A34B", "#0B7A38"
AZUL = "#3B82F6"
PAGAMENTOS = ["Pix", "Dinheiro", "Cartão de débito", "Cartão de crédito", "Fiado"]


def escuro():
    return bool(st.session_state.get("escuro", False))


def estilo():
    dk = escuro()
    bg, sec, txt, mut, borda = (("#0A0F14", "#121C26", "#EAF2EC", "#9FB3A8", "#26364A") if dk
                                else ("#FFFFFF", "#F0F6F2", NAVY, "#4B5B6B", "#D6E4DA"))
    feat = "#101A24" if dk else "#FFFFFF"
    modo_escuro = f"""
.stApp, [data-testid="stHeader"] {{ background:{bg}; }}
[data-testid="stSidebar"] {{ background:{sec}; }}
[data-testid="stHeader"] * {{ color:{txt} !important; }}
.stApp, .stApp * {{ color:{txt}; }}
[data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="menu"], [data-baseweb="calendar"]
    {{ background:{sec} !important; }}
[data-baseweb="popover"] * {{ color:{txt}; }}
[data-baseweb="menu"] li:hover {{ background:{borda} !important; }}
.stApp td, .stApp th {{ color:{txt}; border-color:{borda} !important; }}
.stApp [data-testid="stMarkdownContainer"] *, .stApp [data-testid="stWidgetLabel"] *,
.stApp [data-testid="stExpander"] summary *, .stApp [data-baseweb="tab"] *,
.stApp [data-testid="stCaptionContainer"] *, [data-testid="stSidebar"] * {{ color:{txt}; }}
input::placeholder, textarea::placeholder {{ color:{mut} !important; opacity:1; }}
[data-testid="stNumberInputContainer"] button {{ background:{sec} !important; color:{txt} !important; }}
[data-baseweb="popover"] > div, [data-baseweb="menu"], [data-baseweb="calendar"] {{ background:{sec} !important; }}
[data-baseweb="popover"] *, [data-baseweb="menu"] *, [data-baseweb="calendar"] * {{ color:{txt} !important; }}
[data-baseweb="calendar"] [aria-selected="true"] {{ background:{GREEN} !important; color:#fff !important; }}
[data-testid="stAlert"] * {{ color:{txt} !important; }}
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"] details {{ border-color:{borda} !important; }}
input, textarea, [data-baseweb="select"] > div, [data-baseweb="input"] > div
    {{ background:{sec} !important; color:{txt} !important; }}
""" if dk else ""
    st.markdown(f"""<style>
{modo_escuro}
[data-testid="stMainBlockContainer"] {{ max-width:1000px !important; }}
h1, h2, h3 {{ color:{txt}; font-weight:800; }}
.card {{ background:{sec}; border-left:6px solid {GREEN}; border-radius:12px; padding:14px 18px; margin-bottom:10px; }}
.card small {{ color:{mut}; font-size:.9rem; }}
.card b {{ display:block; font-size:1.5rem; color:{txt}; }}
.lucro {{ background:linear-gradient(135deg,{GREEN},{GREEN_DARK}); color:#fff; border-radius:16px;
         padding:22px; margin-bottom:14px; }}
.lucro small {{ opacity:.9; font-size:1rem; }}
.lucro b {{ display:block; font-size:2.6rem; }}
.alerta {{ background:{feat}; border:1px solid {borda}; border-radius:10px; padding:10px 14px;
          margin-bottom:8px; color:{txt}; }}
div.stButton > button {{ background:{GREEN}; color:#fff; border:0; font-weight:700; border-radius:10px;
                        padding:.6rem 1.2rem; }}
div.stButton > button:hover {{ background:{GREEN_DARK}; color:#fff; }}
div.stButton > button p {{ color:#fff !important; }}
.hero {{ background:linear-gradient(135deg,{NAVY} 0%,#123A3A 55%,{GREEN_DARK} 100%);
        border-radius:20px; padding:34px 30px; margin-bottom:24px; }}
.hero h1 {{ color:#fff !important; font-size:2rem; line-height:1.15; margin:0 0 10px; padding:0; }}
.hero p {{ color:#DCEFE3 !important; font-size:1.05rem; margin:0; }}
.hero .tag {{ display:inline-block; background:rgba(255,255,255,.15); color:#fff;
             border-radius:999px; padding:4px 14px; font-size:.8rem; margin-bottom:14px; }}
.feat {{ background:{feat}; border:1px solid {borda}; border-top:5px solid {GREEN}; border-radius:14px;
        padding:18px; min-height:190px; margin-bottom:12px; box-shadow:0 3px 10px rgba(0,0,0,.10);
        transition:transform .15s; }}
.feat:hover {{ transform:translateY(-4px); }}
.feat .ic {{ font-size:1.9rem; }}
.feat h4 {{ margin:6px 0 6px; color:{txt}; }}
.feat p {{ margin:0; color:{mut}; font-size:.93rem; }}
.passo {{ background:{GREEN_DARK}; color:#fff; border-radius:50%; width:34px; height:34px; display:inline-block;
         text-align:center; line-height:34px; font-weight:800; margin-bottom:6px; }}
.cta {{ background:linear-gradient(135deg,{GREEN},{GREEN_DARK}); color:#fff; border-radius:16px;
       padding:24px; text-align:center; margin:20px 0 10px; font-size:1.2rem; font-weight:700; }}
.tbw {{ overflow-x:auto; margin-bottom:1rem; }}
.tb {{ border-collapse:collapse; width:100%; font-size:.92rem; color:{txt}; }}
.tb th {{ background:{GREEN_DARK}; color:#fff; text-align:left; padding:8px 10px; white-space:nowrap; }}
.tb td {{ padding:7px 10px; border-bottom:1px solid {borda}; white-space:nowrap; }}
[data-testid="stButtonGroup"] {{ gap:.5rem; flex-wrap:wrap; }}
[data-testid^="stBaseButton-pills"] {{ background:{feat}; border:1.5px solid {borda}; border-radius:999px;
    padding:.35rem 1.1rem; min-height:2.5rem; transition:all .15s; }}
[data-testid^="stBaseButton-pills"], [data-testid^="stBaseButton-pills"] * {{ color:{txt} !important; font-weight:600; }}
[data-testid^="stBaseButton-pills"]:hover {{ border-color:{GREEN}; }}
[data-testid="stBaseButton-pillsActive"] {{ background:{GREEN} !important; border-color:{GREEN} !important; }}
[data-testid="stBaseButton-pillsActive"], [data-testid="stBaseButton-pillsActive"] * {{ color:#fff !important; }}
@media (max-width:640px) {{
  [data-testid="stMainBlockContainer"] {{ padding:2.5rem 1rem 3rem !important; }}
  .hero {{ padding:22px 18px; }}
  .hero h1 {{ font-size:1.5rem; }}
  .lucro b {{ font-size:2.1rem; }}
  .feat {{ min-height:0; }}
  .cta {{ font-size:1rem; padding:18px; }}
}}
</style>""", unsafe_allow_html=True)


def db():
    return sqlite3.connect(DB)


def init():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS vendas(id INTEGER PRIMARY KEY AUTOINCREMENT,
                     data TEXT, produto TEXT, valor REAL, custo REAL, qtd INTEGER, pagamento TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS gastos(id INTEGER PRIMARY KEY AUTOINCREMENT,
                     data TEXT, descricao TEXT, valor REAL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS dividas(id INTEGER PRIMARY KEY AUTOINCREMENT,
                     data TEXT, cliente TEXT, descricao TEXT, valor REAL, vencimento TEXT,
                     pago INTEGER DEFAULT 0, data_pago TEXT)""")


def brl(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def resumo(ym):
    with db() as c:
        vendas, custos, lucro_v, n = c.execute(
            """SELECT COALESCE(SUM(valor*qtd),0), COALESCE(SUM(custo*qtd),0),
                      COALESCE(SUM((valor-custo)*qtd),0), COUNT(*)
               FROM vendas WHERE substr(data,1,7)=?""", (ym,)).fetchone()
        outros = c.execute("SELECT COALESCE(SUM(valor),0) FROM gastos WHERE substr(data,1,7)=?",
                           (ym,)).fetchone()[0]
    gastos = custos + outros
    return dict(vendas=vendas, gastos=gastos, lucro=vendas - gastos, n=n,
                lucro_medio=(lucro_v / n if n else 0))


def mes_anterior(ym, k=1):
    """Volta k meses (k negativo avança)."""
    a, m = map(int, ym.split("-"))
    t = a * 12 + (m - 1) - k
    return f"{t // 12}-{t % 12 + 1:02d}"


def salvar_venda():
    s = st.session_state
    if not s.v_produto.strip() or s.v_valor <= 0:
        s.aviso = ("erro", "Diga o que vendeu e por quanto.")
        return
    with db() as c:
        c.execute("INSERT INTO vendas(data,produto,valor,custo,qtd,pagamento) VALUES(?,?,?,?,?,?)",
                  (s.v_data.isoformat(), s.v_produto.strip(), s.v_valor, s.v_custo, s.v_qtd, s.v_pag))
    lucro = (s.v_valor - s.v_custo) * s.v_qtd
    s.aviso = ("ok", f"Venda registrada! Lucro: {brl(lucro)}")
    s.v_produto, s.v_valor, s.v_custo, s.v_qtd = "", 0.0, 0.0, 1


def salvar_gasto():
    s = st.session_state
    if not s.g_desc.strip() or s.g_valor <= 0:
        s.aviso = ("erro", "Diga o que gastou e quanto.")
        return
    with db() as c:
        c.execute("INSERT INTO gastos(data,descricao,valor) VALUES(?,?,?)",
                  (s.g_data.isoformat(), s.g_desc.strip(), s.g_valor))
    s.aviso = ("ok", "Gasto registrado!")
    s.g_desc, s.g_valor = "", 0.0


def mostrar_aviso():
    aviso = st.session_state.pop("aviso", None)
    if aviso:
        (st.success if aviso[0] == "ok" else st.warning)(aviso[1])


def cards(itens):
    for col, (ic, t, d) in zip(st.columns(len(itens)), itens):
        col.markdown(f'<div class="feat"><div class="ic">{ic}</div><h4>{t}</h4><p>{d}</p></div>',
                     unsafe_allow_html=True)


def projecao_lucro():
    """Estima o fechamento do mês e a tendência dos próximos 3 meses."""
    hoje = date.today()
    ym = hoje.strftime("%Y-%m")
    meses = [mes_anterior(ym, k) for k in range(5, -1, -1)]
    rs = [resumo(m) for m in meses]
    ativos = [i for i, r in enumerate(rs) if r["vendas"] or r["gastos"]]
    if not ativos:
        return None
    dias_mes = calendar.monthrange(hoje.year, hoje.month)[1]
    fechamento = rs[-1]["lucro"] / hoje.day * dias_mes
    ini = ativos[0]
    nomes, real = meses[ini:], [r["lucro"] for r in rs[ini:]]
    y = real[:-1] + [fechamento]
    if len(y) < 3:
        return dict(fechamento=fechamento, grafico=None)
    a, b = np.polyfit(range(len(y)), y, 1)
    futuro = [mes_anterior(ym, -k) for k in (1, 2, 3)]
    prev = [float(b + a * (len(y) - 1 + k)) for k in (1, 2, 3)]
    df = pd.DataFrame({"Lucro real": real + [np.nan] * 3,
                       "Projeção": [np.nan] * (len(nomes) - 1) + [fechamento] + prev},
                      index=nomes + futuro)
    return dict(fechamento=fechamento, grafico=df)


def a_receber():
    with db() as c:
        return c.execute("SELECT COALESCE(SUM(valor),0), COUNT(*) FROM dividas WHERE pago=0").fetchone()


def salvar_divida():
    s = st.session_state
    if not s.d_cliente.strip() or s.d_valor <= 0:
        s.aviso = ("erro", "Diga o nome do cliente e quanto ele deve.")
        return
    venc = s.d_venc.isoformat() if s.d_venc else None
    with db() as c:
        c.execute("INSERT INTO dividas(data,cliente,descricao,valor,vencimento) VALUES(?,?,?,?,?)",
                  (date.today().isoformat(), s.d_cliente.strip(), s.d_desc.strip(), s.d_valor, venc))
    s.aviso = ("ok", f"Dívida de {s.d_cliente.strip()} anotada!")
    s.d_cliente, s.d_desc, s.d_valor, s.d_venc = "", "", 0.0, None


def tabela(df):
    """Tabela em HTML: acompanha o modo escuro e rola de lado no celular."""
    df = df.copy()
    for col in ("Valor", "Custo", "Lucro"):
        if col in df.columns:
            df[col] = df[col].map(brl)
    st.markdown('<div class="tbw">' + df.to_html(index=False, classes="tb", border=0, na_rep="") + "</div>",
                unsafe_allow_html=True)


def grafico(df, tipo="bar", cores=None):
    """Gráfico que acompanha o modo escuro. O índice do df vira o eixo X."""
    import altair as alt
    txt, grade = ("#EAF2EC", "#26364A") if escuro() else (NAVY, "#D6E4DA")
    long = df.rename_axis("mes").reset_index().melt("mes", var_name="serie", value_name="valor").dropna()
    cor = alt.Color("serie:N", scale=alt.Scale(domain=list(df.columns), range=cores or [GREEN]),
                    legend=alt.Legend(title=None) if len(df.columns) > 1 else None)
    base = alt.Chart(long, height=260).encode(
        x=alt.X("mes:N", sort=None, title=None, axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("valor:Q", title=None), color=cor, tooltip=["mes", "serie", "valor"])
    graf = base.mark_bar() if tipo == "bar" else base.mark_line(point=True, strokeWidth=3)
    graf = (graf.configure(background="transparent")
            .configure_axis(labelColor=txt, gridColor=grade, domainColor=grade, tickColor=grade)
            .configure_legend(labelColor=txt, orient="bottom").configure_view(stroke=None))
    st.altair_chart(graf, theme=None, width="stretch")


def lucro_semanal(n=8):
    """Lucro (vendas - custos - gastos) das últimas n semanas, de segunda a domingo."""
    hoje = date.today()
    inicio = hoje - timedelta(days=hoje.weekday()) - timedelta(weeks=n - 1)
    with db() as c:
        v = pd.read_sql_query("SELECT data, (valor-custo)*qtd AS lucro FROM vendas WHERE data>=?",
                              c, params=(inicio.isoformat(),))
        g = pd.read_sql_query("SELECT data, -valor AS lucro FROM gastos WHERE data>=?",
                              c, params=(inicio.isoformat(),))
    df = pd.concat([v, g])
    if df.empty:
        return None
    dias = pd.to_datetime(df["data"]).dt.date
    tot = df["lucro"].groupby(dias.map(lambda d: d - timedelta(days=d.weekday()))).sum()
    semanas = [inicio + timedelta(weeks=i) for i in range(n)]
    return pd.DataFrame({"Lucro da semana": [float(tot.get(s, 0.0)) for s in semanas]},
                        index=[s.strftime("%d/%m") for s in semanas])


def lucro_diario(n=14):
    """Lucro (vendas - custos - gastos) dos últimos n dias."""
    hoje = date.today()
    inicio = hoje - timedelta(days=n - 1)
    with db() as c:
        v = pd.read_sql_query("SELECT data, (valor-custo)*qtd AS lucro FROM vendas WHERE data>=?",
                              c, params=(inicio.isoformat(),))
        g = pd.read_sql_query("SELECT data, -valor AS lucro FROM gastos WHERE data>=?",
                              c, params=(inicio.isoformat(),))
    df = pd.concat([v, g])
    if df.empty:
        return None
    tot = df["lucro"].groupby(pd.to_datetime(df["data"]).dt.date).sum()
    dias = [inicio + timedelta(days=i) for i in range(n)]
    return pd.DataFrame({"Lucro do dia": [float(tot.get(d, 0.0)) for d in dias]},
                        index=[d.strftime("%d/%m") for d in dias])