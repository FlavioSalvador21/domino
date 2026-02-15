import streamlit as st
import pandas as pd
import json, os

st.set_page_config(page_title="Dominó", layout="centered")

ARQ = "domino_state.json"

# =========================
# Persistência
# =========================

def salvar():
    with open(ARQ,"w") as f:
        json.dump({
            "historico": st.session_state.historico
        },f)

def carregar():
    if os.path.exists(ARQ):
        with open(ARQ) as f:
            d=json.load(f)
            st.session_state.historico=d.get("historico",[])

# =========================
# Estado inicial
# =========================

if "init" not in st.session_state:
    st.session_state.init=True
    st.session_state.historico=[]
    carregar()

# =========================
# Funções
# =========================

def registrar():

    time = st.session_state.time
    pontos = st.session_state.pontos

    if pontos <= 0:
        return

    linha = {"Turno": len(st.session_state.historico)+1,
             "NÓS": 0,
             "ELES": 0}

    if time == "NÓS":
        linha["NÓS"] = pontos
    else:
        linha["ELES"] = pontos

    st.session_state.historico.append(linha)
    st.session_state.pontos = 0
    salvar()

def recalcular(df_editado):
    st.session_state.historico = df_editado.to_dict("records")
    salvar()

def novo_jogo():
    st.session_state.historico=[]
    salvar()

# =========================
# UI
# =========================

st.title("🁫 DOMINÓ")

# calcula placar sempre a partir do histórico
nos_total = sum(linha["NÓS"] for linha in st.session_state.historico)
eles_total = sum(linha["ELES"] for linha in st.session_state.historico)

c1,c2 = st.columns(2)
c1.metric("NÓS", nos_total)
c2.metric("ELES", eles_total)

st.divider()

st.subheader("Registrar novo turno")

st.radio("Quem pontuou?", ["NÓS","ELES"], horizontal=True, key="time")
st.number_input("Pontos do turno", min_value=0, step=1, key="pontos")

st.button("Registrar Turno", on_click=registrar)

st.divider()

# vencedor automático
if nos_total >= 100:
    st.success("🏆 NÓS venceram!")
elif eles_total >= 100:
    st.success("🏆 ELES venceram!")

# =========================
# Histórico editável
# =========================

if st.session_state.historico:

    df = pd.DataFrame(st.session_state.historico)

    st.subheader("Histórico (editável)")
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        key="editor"
    )

    recalcular(df_editado)

st.divider()

st.button("Novo Jogo", on_click=novo_jogo)
