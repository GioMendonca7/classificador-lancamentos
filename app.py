import pandas as pd
import unicodedata
from fuzzywuzzy import process
import streamlit as st

# Função para limpar texto
def limpa_texto(texto):
    if isinstance(texto, str):
        return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8').strip()
    return texto

# Título da página
st.title("🔎 Classificador de Lançamentos")
st.write("Preencha abaixo com o nome do fornecedor e o departamento para obter o código de lançamento e centro de custo.")

# Leitura do Excel embutido no repositório
CAMINHO_EXCEL = "2148 Centro de Custo e Lucro.xlsx"

df_sup = pd.read_excel(CAMINHO_EXCEL, sheet_name='Mapeamento')
df_sup.columns = df_sup.columns.str.strip()
FORN_COL = 'Descrição da conta de contrapartida'
FORN_CODE_COL = 'Classe de custo'
df_sup[FORN_COL] = df_sup[FORN_COL].apply(limpa_texto)
lista_fornecedores = df_sup[FORN_COL].dropna().unique().tolist()

raw_cc = pd.read_excel(CAMINHO_EXCEL, sheet_name='Centro de Custo', header=None)


if arquivo:
    # Carrega os dados
    df_sup = pd.read_excel(arquivo, sheet_name='Mapeamento')
    df_sup.columns = df_sup.columns.str.strip()
    FORN_COL = 'Descrição da conta de contrapartida'
    FORN_CODE_COL = 'Classe de custo'
    df_sup[FORN_COL] = df_sup[FORN_COL].apply(limpa_texto)
    lista_fornecedores = df_sup[FORN_COL].dropna().unique().tolist()

    raw_cc = pd.read_excel(arquivo, sheet_name='Centro de Custo', header=None)
    hdr_idx = raw_cc.apply(lambda row: row.astype(str).str.contains('Centro de Custo', na=False).any(), axis=1).idxmax()
    data_start = hdr_idx + 2
    df_cc = raw_cc.iloc[data_start:, [1, 2]].copy()
    df_cc.columns = ['Centro de Custo', 'Departamento']
    df_cc = df_cc.dropna(subset=['Centro de Custo', 'Departamento'])
    df_cc['Centro de Custo'] = df_cc['Centro de Custo'].astype(int).astype(str)

