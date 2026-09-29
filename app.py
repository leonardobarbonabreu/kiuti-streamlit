"""Página inicial: login."""
import streamlit as st

import api

st.set_page_config(page_title="Kiuti", layout="wide")
st.title("Kiuti")
st.caption("Custos, preços e reajustes da loja.")

if "token" in st.session_state:
    st.success("Login feito. Escolha uma página no menu ao lado.")
    if st.button("Sair"):
        st.session_state.pop("token")
        st.rerun()
    st.stop()

with st.form("login"):
    login = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    entrar = st.form_submit_button("Entrar", type="primary")

if entrar:
    try:
        api.entrar(login, senha)
        st.rerun()
    except api.ErroApi as erro:
        st.error(erro.detail)
