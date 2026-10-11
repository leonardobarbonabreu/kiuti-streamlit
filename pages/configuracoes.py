"""Taxas da Shopee, margem de lucro e outras variáveis de configuração da Loja"""
import streamlit as st
import api

st.set_page_config(page_title="Configurações · Kiuti", layout="wide")
st.title("Configurações")
api.exigir_login()
api.mostrar_aviso()

CAMPOS = {  # chave do JSON: rótulo na tela
    "perc_taxa_shopee": "Taxa da Shopee (%)",
    "taxa_fixa_shopee": "Taxa fixa por venda (R$)",
    "embalagem_padrao": "Embalagem padrão (R$)",
    "brinde_padrao": "Brinde padrão (R$)",
    "envio_padrao": "Envio padrão (R$)",
    "despesas_variaveis_padrao": "Despesas variáveis padrão (R$)",
    "perc_lucro_padrao": "Margem padrão sobre o custo (%)",
}

try:
    config = api.get("/configuracoes")
except api.ErroApi as erro:
    st.error(erro.detail)
    st.stop()

with st.form("configuracoes"):
    novos = {}
    colunas = st.columns(2)
    for posicao, (chave, rotulo) in enumerate(CAMPOS.items()):
        novos[chave] = colunas[posicao % 2].number_input(
            rotulo, min_value=0.0, value=float(config[chave]), step=0.5, format="%.2f"
        )
    salvar = st.form_submit_button("Salvar", type="primary")

if salvar:
    mudancas = {chave: valor for chave, valor in novos.items() if valor != config[chave]}
    if not mudancas:
        st.info("Nada mudou.")
    else:
        try:
            api.put("/configuracoes", mudancas)
            api.avisar_depois("Configurações salvas.")
            st.rerun()
        except api.ErroApi as erro:
            campo = erro.dados.get("campo")
            st.error(f"{CAMPOS.get(campo, campo)}: {erro.detail}" if campo else erro.detail)