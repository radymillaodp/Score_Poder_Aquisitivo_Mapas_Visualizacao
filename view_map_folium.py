import folium

def criar_mapa_folium(gdf_merged, gdf_bairros, cores_faixa):
    def estilo(feature):
        faixa = feature['properties'].get('faixa')
        cor = cores_faixa.get(faixa, 'gray')
        return {
            'fillColor': cor,
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        }

    def estilo_bairro_com_faixa(feature):
        faixa = feature['properties'].get('faixa_bairro')
        cor = cores_faixa.get(faixa, 'gray')
        return {
            'fillColor': cor,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        }

    centro = [gdf_merged.geometry.centroid.y.mean(), gdf_merged.geometry.centroid.x.mean()]

    m = folium.Map(location=centro, zoom_start=12, tiles='cartodbpositron')

    folium.GeoJson(
        gdf_merged,
        name='Setores - Poder Aquisitivo',
        style_function=estilo,
        tooltip=folium.GeoJsonTooltip(
            fields=['CD_SETOR', 'score_poder_compra', 'faixa'],
            aliases=['Código Setor', 'Score Poder Compra', 'Faixa'],
            localize=True
        )
    ).add_to(m)

    folium.GeoJson(
        gdf_bairros,
        name='Bairros - Faixa Poder Compra',
        style_function=estilo_bairro_com_faixa,
        tooltip=folium.GeoJsonTooltip(
            fields=['NM_SUBDIST', 'score_poder_compra_bairro', 'faixa_bairro'],
            aliases=['Bairro', 'Score Poder Compra Bairro', 'Faixa Poder Compra Bairro'],
            localize=True
        )
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m
