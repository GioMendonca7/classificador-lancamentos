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

# Leitura direta do Excel embutido no repositório
CAMINHO_EXCEL = "2148 Centro de Custo e Lucro.xlsx"

# --- Fornecedores ---
df_sup = pd.read_excel(CAMINHO_EXCEL, sheet_name='Mapeamento')
df_sup.columns = df_sup.columns.str.strip()
FORN_COL = 'Descrição da conta de contrapartida'
FORN_CODE_COL = 'Classe de custo'
df_sup[FORN_COL] = df_sup[FORN_COL].apply(limpa_texto)
lista_fornecedores = df_sup[FORN_COL].dropna().unique().tolist()

# --- Departamentos ---
raw_cc = pd.read_excel(CAMINHO_EXCEL, sheet_name='Centro de Custo', header=None)
hdr_idx = raw_cc.apply(lambda row: row.astype(str).str.contains('Centro de Custo', na=False).any(), axis=1).idxmax()
data_start = hdr_idx + 2
df_cc = raw_cc.iloc[data_start:, [1, 2]].copy()
df_cc.columns = ['Centro de Custo', 'Departamento']
df_cc = df_cc.dropna(subset=['Centro de Custo', 'Departamento'])
df_cc['Centro de Custo'] = df_cc['Centro de Custo'].astype(int).astype(str)
df_cc['Departamento'] = df_cc['Departamento'].apply(limpa_texto)
lista_departamentos = df_cc['Departamento'].tolist()

# Inputs do usuário
fornecedor_input = st.text_input("Fornecedor")
departamento_input = st.text_input("Departamento")

if st.button("🔍 Buscar"):
    if not fornecedor_input or not departamento_input:
        st.warning("Por favor, preencha os dois campos.")
    else:
        fornecedor_input = limpa_texto(fornecedor_input)
        match_forn, score_forn = process.extractOne(fornecedor_input, lista_fornecedores)

        if score_forn >= 70:
            cod_forn = df_sup.loc[df_sup[FORN_COL] == match_forn, FORN_CODE_COL].values[0]
            st.success(f"Fornecedor reconhecido: {match_forn} (confiança {score_forn}%)")
            st.write(f"**Código de Lançamento:** `{cod_forn}`")
        else:
            st.error(f"Fornecedor '{fornecedor_input}' não encontrado.")

        departamento_input = limpa_texto(departamento_input)
        match_depto, score_depto = process.extractOne(departamento_input, lista_departamentos)

        if score_depto >= 70:
            centro_custo = df_cc.loc[df_cc['Departamento'] == match_depto, 'Centro de Custo'].values[0]
            st.success(f"Departamento reconhecido: {match_depto} (confiança {score_depto}%)")
            st.write(f"**Centro de Custo:** `{centro_custo}`")
        else:
            st.error(f"Departamento '{departamento_input}' não encontrado.")

