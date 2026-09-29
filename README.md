# kiuti-streamlit

Interface web do Kiuti (custos, preços e reajustes), cliente da API Kiuti.

## Preparar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .streamlit\secrets.exemplo.toml .streamlit\secrets.toml
```

Edite `.streamlit\secrets.toml` com a URL da API (`API_URL`). Esse arquivo não vai para o Git.

## Rodar

```powershell
.venv\Scripts\Activate.ps1
streamlit run app.py
```

Abre em http://localhost:8501. A API precisa estar no ar em `API_URL`.
