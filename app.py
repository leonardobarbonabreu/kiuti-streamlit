"""Página inicial: login."""
import streamlit as st

import api

st.set_page_config(page_title="Kiuti", layout="wide")
st.image("C:\\SISTEMAS\\VS_CODE\\PROJETO_KIUTI\\STREAM_LIT\\imagens\\Logo_kiuti.png", width=144)
st.caption("Custos, preços e reajustes da loja.")

if "token" in st.session_state:
    st.success("Login feito. Escolha uma página no menu ao lado.")
    if st.button("Sair"):
        st.session_state.pop("token")
        st.rerun()
    st.stop()

with st.form("login", width=300):
    login = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    entrar = st.form_submit_button("Entrar", type="primary")

if entrar:
    try:
        api.entrar(login, senha)
        st.rerun()
    except api.ErroApi as erro:
        st.error(erro.detail)
