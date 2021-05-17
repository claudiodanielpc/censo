import pandas as pd
import geopandas as gpd
import os
import matplotlib.pyplot as plt


##Seleccionar directorio de trabajo
os.chdir("C:/Users/ALIENWARE/Documents/censo2020")




datos = "conjunto_de_datos/conjunto_de_datos_iter_00_cpv2020.csv"


df = pd.read_csv(datos,
                 na_values=["N/D",
                            "*"],

                 usecols=["ENTIDAD",
                           "NOM_ENT",
                           "MUN",
                           "NOM_LOC",
                            "TVIVPARHAB",
                          "VPH_INTER"
                  ],
                  dtype={"ENTIDAD": str,
                           "NOM_ENT" :str,
                           "MUN": str,
                           "NOM_LOC": str,
                            "TVIVPARHAB": float,
                            "VPH_INTER": float
                  }
                  )


#Columnas a minúsculas
df.columns = df.columns.str.lower()



df =df[df["nom_loc"].isin (["Total del Municipio" ])]

##Construir clave para pegar con shape

df["CVEGEO"] =(df["entidad"].astype( str ).str.zfill( 2 ) +
                df['mun'].astype( str ).str.zfill( 3 ))


#Crear variable de porcentaje
df["pct"] = df["vph_inter"]/df["tvivparhab"]*100

#Importar shape

mun= gpd.read_file("conjunto_de_datos/00mun.shp")
#Pegar datos al shape
mun = mun.merge(df, how="left",on="CVEGEO")


#Mapa

fig, ax = plt.subplots(1, figsize=(20,10))
#Título
plt.suptitle("Viviendas particulares habitadas que disponen de internet, 2020",
              x =0.43,
             fontsize = 30,
             fontname = "Century Gothic",
              fontweight="bold",
              color = "black")
# Subtítulo con sumatoria
ax.text(x=0.7e6, y=2.37e6,
        s=f'% del total de viviendas particulares habitadas con internet\n {sum(mun["vph_inter"])/sum(mun["tvivparhab"])*100:.1f} %',
        fontsize=20,
        fontname= "Century Gothic",
        color='black',
        style="italic")
#Capa de información
mun.plot(column='pct',
           cmap='BuGn', ax=ax,
        edgecolor='face', legend=True,
        legend_kwds={'label': "%"})
#Sin ejes
ax.axis('off')
#Fuente
ax.annotate("Fuente: Elaborado por CANADEVI Nacional. Gerencia de Fondos de Vivienda. Coordinación de Indicadores de Vivienda\n con datos de INEGI. Censo de Población y Vivienda 2020",
            xy=(0.1, .08), xycoords="figure fraction",
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=15, color="black",
fontname="Century Gothic")
ax.axis("equal")

#Salvar
plt.savefig("internet.png",
            format="png",dpi=300,transparent=False)
#plt.show()

