#Mapa viviendas particulares habitadas que disponen de energía eléctrica en CDMX
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import os


##Seleccionar directorio de trabajo y crear carpeta
dir = os.chdir ('C:/Users/ALIENWARE/Documents/censo2020 ')


#Importar datos
# Llamar a la base de datos
df = pd.read_csv("conjunto_de_datos/conjunto_de_datos_ageb_urbana_09_cpv2020.csv",
                        na_values=["N/D","*"],
                        usecols=["NOM_LOC",
                                 "ENTIDAD",
                           "MUN",
                           "LOC",
                            "AGEB",
                            "VPH_C_ELEC"],
                            dtype={"NOM_LOC":str,
                                "ENTIDAD": str,
                                   "MUN": str,
                                   "LOC": str,
                                    "AGEB": str,
                                   "VPH_C_ELEC": float}
                 )


##Limpieza de base de datos
# Columnas a minúsculas
df.columns = df.columns.str.lower()

# Filtrar solo datos por AGEB urbana
df = df[df["nom_loc"] == "Total AGEB urbana"]


# Crear clave geoestadística
df["CVEGEO"] =(df['entidad'].astype(str).str.zfill(2)+
               df['mun'].astype(str).str.zfill(3)+
               df['loc'].astype(str).str.zfill(4)+
               df['ageb'].astype(str).str.zfill(4))



##Importar shapes
cdmx=gpd.read_file("conjunto_de_datos/09ent.shp")

agebcdmx = gpd.read_file(
    "conjunto_de_datos/09a.shp")

#Calcular centroide de Agebs
agebcdmx["centroide"]=agebcdmx["geometry"].centroid


#Hacer nueva dataframe y pegar los datos de vienda
cent = agebcdmx[["CVEGEO", "centroide"]]

cent=cent.merge(
    df,
    how="left",
    on="CVEGEO"
    )


##Renombrar variable
cent = cent.rename( columns={'centroide': 'geometry'} )

#Transformar a geodataframe
cent = gpd.GeoDataFrame(cent)



#Mapa
fig,ax = plt.subplots( figsize=(12,12),
                       facecolor='black')
#Título
ax.set_title( 'Ciudad de México\nViviendas particulares habitadas que disponen de energía eléctrica por AGEB Urbana',
               fontsize=20,fontname='Century Gothic',
              fontweight='bold',color='white' )
#Capa entidad
cdmx.plot(ax=ax,color="#000000",
              edgecolor="grey",
              linewidth=0.8)
#Capa AGEBS
agebcdmx.plot(ax=ax,
              color="#000000",
              edgecolor="grey",
              linewidth=0.6)
#Centroides con número de viviendas
cent.plot(ax=ax,
          column="vph_c_elec",
          cmap="Wistia",
          markersize=6)
ax.axis('off')

# Fuente
    ax.annotate( 'Fuente: @claudiodanielpc con datos de INEGI. Censo de Población y Vivienda 2020',
                 xy=(0.1,.08),
                 xycoords='figure fraction',
                 horizontalalignment='left',verticalalignment='top',fontsize=16,color='white',
                 fontname='Century Gothic' )

#Salvar
plt.savefig("cdmxviviluz.png", format="png", dpi=600, transparent=False)