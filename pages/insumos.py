"""CRUD de insumos."""
import pandas as pd
import streamlit as st

import api
from formatos import numero, reais

UNIDADES = ["g", "kg", "m", "cm", "ml", "l", "un", "pct"]

st.set_page_config(page_title="Insumos · Kiuti", layout="wide")
st.title("Insumos")
api.exigir_login()
api.mostrar_aviso()

try:
    insumos = api.get("/insumos")
except api.ErroApi as erro:
    st.error(erro.detail)
    st.stop()

# --- Tabela ---
if insumos:
    tabela = pd.DataFrame(insumos)
    tabela["compra"] = [f"{numero(i['qtde_compra'])} {i['unidade_compra']} por {reais(i['custo'])}" for i in insumos]
    st.dataframe(
        tabela[["nome", "compra", "custo_unitario", "unidade_compra", "qtd_produtos"]],
        column_config={
            "nome": "Insumo",
            "compra": "Compra",
            "custo_unitario": st.column_config.NumberColumn("Custo por unidade", format="R$ %.3f"),
            "unidade_compra": "Unidade",
            "qtd_produtos": "Usado em (produtos)",
        },
        hide_index=True,
        use_container_width=True,
    )
else:
    st.info("Nenhum insumo cadastrado ainda.")

# --- Cadastrar ou editar ---
st.subheader("Cadastrar ou editar")
# As opções são os ids (e não os dicionários): assim a escolha continua a mesma depois de um st.rerun().
por_id = {i["id_insumo"]: i for i in insumos}
id_escolhido = st.selectbox(
    "Insumo",
    [None, *por_id],
    format_func=lambda id_insumo: "— Novo insumo —" if id_insumo is None else por_id[id_insumo]["nome"],
)
insumo = por_id.get(id_escolhido)

with st.form("insumo", clear_on_submit=insumo is None):
    nome = st.text_input("Nome", value=insumo["nome"] if insumo else "")
    col1, col2, col3 = st.columns(3)
    custo = col1.number_input(
        "Quanto paguei (R$)", min_value=0.0, step=0.01, format="%.2f", value=float(insumo["custo"]) if insumo else 0.0
    )
    qtde = col2.number_input(
        "Por quanto", min_value=0.0, step=1.0, format="%.3f", value=float(insumo["qtde_compra"]) if insumo else 0.0
    )
    unidade = col3.selectbox("Unidade", UNIDADES, index=UNIDADES.index(insumo["unidade_compra"]) if insumo else 0)
    salvar = st.form_submit_button("Salvar", type="primary")

if salvar:
    dados = {"nome": nome, "custo": custo, "unidade_compra": unidade, "qtde_compra": qtde}
    try:
        if insumo:
            api.put(f"/insumos/{insumo['id_insumo']}", dados)
        else:
            api.post("/insumos", dados)
        api.avisar_depois(f"Insumo {nome.strip()} salvo.")
        st.rerun()
    except api.ErroApi as erro:
        st.error(erro.detail)  # 409 (nome repetido) e 422 (quantidade zero...) já vêm com a mensagem

# --- Usado em e excluir (só para um insumo escolhido) ---
if insumo:
    produtos = api.get(f"/insumos/{insumo['id_insumo']}/produtos")
    if produtos:
        st.caption("Usado em: " + ", ".join(f"{p['nome']} ({numero(p['qtde'])} {insumo['unidade_compra']})" for p in produtos))

    if st.button("Excluir insumo"):
        st.session_state["confirmar_exclusao"] = insumo["id_insumo"]

    if st.session_state.get("confirmar_exclusao") == insumo["id_insumo"]:
        st.warning(f"Excluir {insumo['nome']}? Não dá para desfazer.")
        if st.button("Sim, excluir", type="primary"):
            st.session_state.pop("confirmar_exclusao")
            try:
                api.delete(f"/insumos/{insumo['id_insumo']}")
                api.avisar_depois(f"Insumo {insumo['nome']} excluído.")
                st.rerun()
            except api.ErroApi as erro:
                st.error(erro.detail)  # RN11: em uso
                for produto in erro.dados.get("produtos", []):
                    st.write(f"- {produto['nome']} ({numero(produto['qtde'])} {insumo['unidade_compra']})")