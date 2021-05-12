import pandas as pd
import geopandas as gpd
import os
import numpy as np
import matplotlib.pyplot as plt


##Seleccionar directorio de trabajo
os.chdir("C:/Users/ALIENWARE/Documents/censo2020")

#Lectura de datos
df = pd.read_csv("microdatos/Personas00.csv")

#LIMPIEZA
#Columnas en minúsculas
df.columns = df.columns.str.lower()

#Filtro de información requerida
df = df[(df["sexo"] == 3) &
        (df["hijos_nac_vivos"] != 0) &
        (df["edad"] >= 15)]


##Crear clave para mapear

df["CVEGEO"] =df['ent'].astype(str).str.zfill(2)


#Tabla colapsada
madre=pd.crosstab(index=df["CVEGEO"],
                           columns="count",
                           values=df["factor"],
                           aggfunc=np.sum, margins=False,
                           margins_name="Total")


##Calcular porcentaje del total
madre["pct"]=madre["count"]/sum(madre["count"])*100


#Importar shape

ent= gpd.read_file("conjunto_de_datos/00ent.shp")
#Pegar datos al shape
ent = ent.merge(madre, how="left",on="CVEGEO")



#Mapa

fig, ax = plt.subplots(1, figsize=(20,10))
#Título
plt.suptitle("Distribución de madres en México por entidad federativa, 2020",
              x =0.43,
             fontsize = 30,
             fontname = "Century Gothic",
              fontweight="bold",
              color = "black")
# Subtítulo con sumatoria
ax.text(x=0.7e6, y=2.37e6,
        s=f'% del total de mujeres 15 años y más con hijos nacidos vivos\n {sum(ent["count"])/1000000:.1f} millones de madres en nuestro país',
        fontsize=20,
        fontname= "Century Gothic",
        color='black',
        style="italic")
#Capa de información
ent.plot(column='pct',
           cmap='YlOrBr', linewidth=0.1, ax=ax,
        edgecolor='.5', legend=True,
        legend_kwds={'label': "%"})
#Sin ejes
ax.axis('off')
#Fuente
ax.annotate("Fuente: @claudiodanielpc con datos de INEGI. Censo de Población y Vivienda 2020",
            xy=(0.1, .08), xycoords="figure fraction",
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=15, color="black",
fontname="Century Gothic")
ax.axis("equal")

#Salvar
plt.savefig("mapamadrespython.png",
            format="png",dpi=600,transparent=False)
#plt.show()