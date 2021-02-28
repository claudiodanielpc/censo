import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import zipfile
import requests
import os
import io
from slugify import slugify

csv_args = {
    "na_values": ['N/D', '*'],
    "usecols": [
        'GRAPROES',
        'ENTIDAD',
        'MUN',
        'LOC',
        'AGEB',
        'MZA',
        'VPH_INTER',
        'TVIVPARHAB',
        'NOM_LOC'
    ],
    "dtype": {
        'GRAPROES': float,
        'ENTIDAD': str,
        'MUN': str,
        'LOC': str,
        'AGEB': str,
        'MZA': str,
        'VPH_INTER': float,
        'TVIVPARHAB': float,
        'NOM_LOC': str
    }
}

nivelesn = {
    'Total de la entidad',
    'Total del municipio',
    'Total de la localidad urbana',
    'Total AGEB urbana'
}

informacion = [
    {
        "estado": "Jalisco",
        "archivo": "RESAGEBURB_14CSV20.csv",
        "municipios": [
            ("Arandas", '14008'),
            ("Zapotlán el Grande", '14023'),
            ("Ocotlán", "14063"),
            ("San Juan de los Lagos", "14073"),
        ],
        "shape": 'conjunto_de_datos/14m.shp',
    },
    {
        "estado": "Sinaloa",
        "archivo": "RESAGEBURB_25CSV20.csv",
        "municipios": [
            ("Guasave", '25011'),
        ],
        "shape": 'conjunto_de_datos/25m.shp',
    },
]


def plot(info):
    df = pd.read_csv(info["archivo"], **csv_args)
    df = df[~df['NOM_LOC'].isin(nivelesn)]

    claves_municipios = {cve_mun for nombre_mpo, cve_mun in info["municipios"]}

    # Municipio
    df['cve_mun'] = (
            df['ENTIDAD'].str.zfill(2) +
            df['MUN'].str.zfill(3)
    )

    # Manzana
    df['CVEGEO'] = (
            df['ENTIDAD'].str.zfill(2) +
            df['MUN'].str.zfill(3) +
            df['LOC'].str.zfill(4) +
            df['AGEB'].str.zfill(4) +
            df['MZA'].str.zfill(3)
    )

    # Filtrar municipios a mapear
    df = df[
        df['cve_mun'].isin(claves_municipios)
    ]

    # Crear porcentaje de viviendas particulares habitadas con internet
    df['porvivint'] = df['VPH_INTER'] / df['TVIVPARHAB'] * 100

    # Importar shapes
    mza = gpd.read_file(info["shape"])

    # Crear claves para filtrar
    mza['municipio'] = (
            mza['CVE_ENT'].str.zfill(2) +
            mza['CVE_MUN'].str.zfill(3)
    )

    # Dejar únicamente las manzanas de los municipios requeridos
    mza = mza[
        mza['municipio'].isin(claves_municipios)
    ]

    # Pegar los datos al shape
    mza = mza.merge(df, how='left', on='CVEGEO')

    for nombre_mpo, cve_mun in info["municipios"]:
        municipio = mza[mza['municipio'] == cve_mun]
        nombre_entidad = f'{nombre_mpo}, {info["estado"]}'
        nombre_archivo = slugify(nombre_entidad)

        plot_column(f'{nombre_entidad}\nViviendas particulares habitadas\nque disponen de internet por manzana\n(%)',
                    column="porvivint", municipio=municipio, nombre_archivo=nombre_archivo, cmap="YlOrBr")

        plot_column(f'{nombre_entidad}\nGrado promedio de escolaridad\npor manzana',
                    column="GRAPROES", municipio=municipio, nombre_archivo=nombre_archivo, cmap="YlGn")


def plot_column(titulo, column, municipio, nombre_archivo, cmap):
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_title(titulo,
                 fontsize=20, fontname='Century Gothic', fontweight='bold', color='black')
    #
    municipio.plot(column=column, cmap=cmap, linewidth=0.1, ax=ax,
                   edgecolor='.2', legend=True,
                   legend_kwds={'label': '% del total de viviendas particulares habitadas'})
    ax.axis('off')
    # Fuente
    ax.annotate('Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020', xy=(0.1, .08),
                xycoords='figure fraction',
                horizontalalignment='left', verticalalignment='top', fontsize=13, color='black',
                fontname='Century Gothic')
    ax.axis('equal')
    # Salvar y mostrar
    plt.savefig(f'{nombre_archivo}_{column}.png', format='png', dpi=600, transparent=False)


for info in informacion:
    plot(info)
