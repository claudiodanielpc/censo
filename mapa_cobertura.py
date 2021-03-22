##Mapa de cobertura de la muestra del Cuestionario Ampliado del Censo 2020

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import os

##Seleccionar directorio de trabajo
os.chdir("C:/Users/ALIENWARE/Documents/censo2020")


##Datos de la muestra del Censo 2020
df = pd.read_csv("microdatos/Viviendas00.csv",
                  #Variables necesarias para el mapa de cobertura
                  usecols = ["COBERTURA",
                             "ENT",
                             "MUN"])

#Shape de municipios
mex = gpd.read_file("conjunto_de_datos/00mun.shp")

# Crear clave geoestadística para pegar en shape
df["CVEGEO"] = (df['ENT'].astype(str).str.zfill(2) +
                df['MUN'].astype(str).str.zfill(3))


##Quitar duplicados
df = df.drop_duplicates(subset=["CVEGEO"])

#Cambiar valores de categoría de cobertura

df["COBERTURA"] = df["COBERTURA"].replace([1, 2, 3],
                                              ["Censado",
                                               "Muestreado",
                                               "Muestra insuficiente"])


##Pegar datos de cobertura a shape
mex = mex.merge(
    df,
    how="left",
    on="CVEGEO"
    )


#Mapa
fig, ax = plt.subplots(figsize=(15, 12))
#Título
ax.set_title('México\nCobertura para el Cuestionario Ampliado\n'
              'por municipio',
               fontsize=20, fontname='Century Gothic',
              fontweight='bold', color='black')

#Capa municipios
mex.plot(ax=ax,
              column="COBERTURA",
            categorical=True,
               cmap="tab20",
              edgecolor="face",
              linewidth=0.4,
              legend=True)

#Sin ejes
ax.axis('off')

# Fuente
ax.annotate('Fuente: @claudiodanielpc con datos de INEGI.\nCenso de Población y Vivienda 2020. Cuestionario ampliado',
                 xy=(0.1, .08),
                 xycoords='figure fraction',
                 horizontalalignment='left',
                 verticalalignment='top',
                 fontsize=16, color='black',
                 fontname='Century Gothic')

#Salvar
plt.savefig("coberturacenso.png", format="png", dpi=600, transparent=False)
