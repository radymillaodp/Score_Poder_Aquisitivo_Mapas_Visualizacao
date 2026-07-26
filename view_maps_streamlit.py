import streamlit as st
import geopandas as gpd
import pandas as pd

# Seu dicionário de cores
cores_faixa = {
    'E — Muito Baixo': '#d73027',
    'D — Baixo': '#fc8d59',
    'C — Médio': '#fee08b',
    'B — Alto': '#91bfdb',
    'A — Muito Alto': '#4575b4'
}

# Função que você já tem para criar mapa
from view_map_folium import criar_mapa_folium

st.title("Mapa Interativo de Poder Aquisitivo")
excel_path = r'C:\Users\odp240024\OneDrive - Odontoprev S.A\Documentos\Documentacao_Primeira_Fase_Desafio_Summer\Terceira_Versao_PoderAquisitivo\PoderAquisitivo_Bairros_Capitais\PE_Bairros_Capitais\resultado_poder_aquisitivo_setores_v3_bairros_brasilia.xlsx'
df = pd.read_excel(excel_path)

codigo_capital = '5300108'

# Carregar shapefile zipado do estado selecionado direto do ZIP
zip_path = r'C:\Users\odp240024\OneDrive - Odontoprev S.A\Documentos\Documentacao_Primeira_Fase_Desafio_Summer\Terceira_Versao_PoderAquisitivo\PoderAquisitivo_Bairros_Capitais\SHP_Setores_UF\DF_setores_CD2022.zip'
shp_in_zip = 'DF_setores_CD2022.shp'

gdf = gpd.read_file(f'zip://{zip_path}!{shp_in_zip}')

# Coluna CD_SETOR do shapefile para merge
gdf['CD_SETOR'] = gdf['CD_SETOR'].astype(str).str.strip()

# Filtrar apenas setores da capital escolhida o shapefile
gdf_capital = gdf[gdf['CD_SETOR'].str.startswith(codigo_capital)].copy()

print(gdf_capital.head())

# Coluna nova com codigo imutável
df['CD_setor_str'] = df['CD_setor'].astype(str)

# Merge com shapefile na coluna CD_SETOR
gdf_merged = gdf_capital.merge(
    df[['CD_setor_str', 'score_poder_compra', 'faixa', 'score_poder_compra_bairro', 'faixa_bairro']],
    left_on='CD_SETOR',
    right_on='CD_setor_str',
    how='left'
)

gdf_bairros = gdf_merged.dissolve(
    by='NM_SUBDIST',
    aggfunc={
        'score_poder_compra_bairro': 'median',
        'faixa_bairro': 'first'
    }
).reset_index()

# Criar o mapa
m = criar_mapa_folium(gdf_merged, gdf_bairros, cores_faixa)

# Gerar HTML do mapa e mostrar no Streamlit
map_html = m._repr_html_()
st.components.v1.html(map_html, width=800, height=600)
