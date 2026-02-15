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
            "turno": st.session_state.turno,
            "nos": st.session_state.nos,
            "eles": st.session_state.eles,
            "historico": st.session_state.historico
        },f)

def carregar():
    if os.path.exists(ARQ):
        with open(ARQ) as f:
            d=json.load(f)
            st.session_state.turno=d["turno"]
            st.session_state.nos=d["nos"]
            st.session_state.eles=d["eles"]
            st.session_state.historico=d["historico"]

# =========================
# Estado inicial
# =========================

if "init" not in st.session_state:
    st.session_state.init=True
    st.session_state.turno=1
    st.session_state.nos=0
    st.session_state.eles=0
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

    linha = {"Turno": st.session_state.turno, "NÓS":0, "ELES":0}

    if time == "NÓS":
        st.session_state.nos += pontos
        linha["NÓS"] = pontos
    else:
        st.session_state.eles += pontos
        linha["ELES"] = pontos

    st.session_state.historico.append(linha)
    st.session_state.turno += 1
    st.session_state.pontos = 0
    salvar()

def novo_jogo():
    st.session_state.turno=1
    st.session_state.nos=0
    st.session_state.eles=0
    st.session_state.historico=[]
    salvar()

# =========================
# UI
# =========================

st.title("🁫 DOMINÓ")

c1,c2 = st.columns(2)

c1.metric("NÓS", st.session_state.nos)
c2.metric("ELES", st.session_state.eles)

st.divider()

st.subheader(f"Turno {st.session_state.turno}")

st.radio("Quem pontuou?", ["NÓS","ELES"], horizontal=True, key="time")

st.number_input("Pontos do turno", min_value=0, step=1, key="pontos")

st.button("Registrar Turno", on_click=registrar)

st.divider()

# vencedor
if st.session_state.nos >= 100:
    st.success("🏆 NÓS venceram!")
elif st.session_state.eles >= 100:
    st.success("🏆 ELES venceram!")

# =========================
# Histórico
# =========================

if st.session_state.historico:

    df = pd.DataFrame(st.session_state.historico).set_index("Turno")
    st.subheader("Histórico de Turnos")
    st.dataframe(df, use_container_width=True)

st.divider()

st.button("Novo Jogo", on_click=novo_jogo)
