"""Chamadas à API Kiuti. Todas as páginas usam estas funções."""
import requests
import streamlit as st

URL = st.secrets["API_URL"].rstrip("/")


class ErroApi(Exception):
    """Erro vindo da API (ou falta de conexão), com a mensagem pronta para mostrar."""

    def __init__(self, status: int, detail: str, dados: dict | None = None):
        super().__init__(detail)
        self.status = status      # 0 = sem conexão; 401, 404, 409, 422...
        self.detail = detail      # o "detail" da API
        self.dados = dados or {}  # o JSON inteiro do erro (ex.: "campo", "produtos")


def _chamar(metodo: str, caminho: str, corpo=None):
    cabecalhos = {}
    if "token" in st.session_state:
        cabecalhos["Authorization"] = f"Bearer {st.session_state['token']}"
    try:
        # 60 s: a API gratuita "dorme" e demora para acordar.
        resposta = requests.request(metodo, URL + caminho, json=corpo, headers=cabecalhos, timeout=60)
    except requests.RequestException:
        raise ErroApi(0, "Não foi possível conectar à API. Confira a internet e tente de novo.")

    dados = resposta.json() if resposta.content else None
    if resposta.status_code == 401 and caminho != "/auth/login":
        st.session_state.pop("token", None)  # token vencido: a próxima página pede login
    if not resposta.ok:
        detalhe = dados.get("detail", "Erro inesperado.") if isinstance(dados, dict) else "Erro inesperado."
        raise ErroApi(resposta.status_code, detalhe, dados if isinstance(dados, dict) else None)
    return dados


def get(caminho: str):
    return _chamar("GET", caminho)


def post(caminho: str, corpo=None):
    return _chamar("POST", caminho, corpo)


def put(caminho: str, corpo):
    return _chamar("PUT", caminho, corpo)


def delete(caminho: str):
    return _chamar("DELETE", caminho)


def entrar(login: str, senha: str) -> None:
    """POST /auth/login. Guarda o token na sessão do navegador."""
    st.session_state["token"] = post("/auth/login", {"login": login, "senha": senha})["access_token"]


def exigir_login() -> None:
    """Primeira linha de toda página, menos a de login. Sem token, mostra o aviso e para a página."""
    if "token" not in st.session_state:
        st.warning("Faça login para continuar: abra a página **app** no menu ao lado.")
        st.stop()
    if st.sidebar.button("Sair"):
        st.session_state.pop("token", None)
        st.rerun()


def avisar_depois(mensagem: str) -> None:
    """Guarda um aviso para mostrar depois do st.rerun() (que apagaria um st.success comum)."""
    st.session_state["aviso"] = mensagem


def mostrar_aviso() -> None:
    """Mostra o aviso guardado por avisar_depois, se houver."""
    aviso = st.session_state.pop("aviso", None)
    if aviso:
        st.success(aviso)
