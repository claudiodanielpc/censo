##Traer los datos del censo para obtener la relación de dependencia de las personas de 60 años y más

import pandas as pd
import requests, io, os, zipfile
import matplotlib.pyplot as plt
import geopandas as gpd

##Seleccionar directorio de trabajo
dir = os.chdir("C:/Users/ALIENWARE/Documents/censo2020")

# URLS de datos
urls = ["https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip"
    "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_09_cpv2020_csv.zip",
        "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/09_ciudaddemexico.zip"]

# Descomprimir y extraer el archivo

for url in urls:
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()

# Llamar a la base de datos
df = pd.read_csv("ITER_NALCSV20.csv")

##Limpieza de base de datos
# Columnas a minúsculas
df.columns = df.columns.str.lower()

# Filtrar solo datos estatales
df = df[df["nom_loc"] == "Total de la Entidad"]

# Crear clave geoestadística
df["CVEGEO"] = df.entidad.map("{:02}".format)

# Dejar las variables con las que se trabajarán

df = df[["CVEGEO", "p_15ymas", "p_60ymas"]]

# Construir la variable de población en edad de trabajar
# Formato de número
df["p_15ymas"] = pd.to_numeric(df["p_15ymas"], errors="coerce")
df["p_60ymas"] = pd.to_numeric(df["p_60ymas"], errors="coerce")

##Obtener la población de 15 años y hasta 59
df["pobtrab"] = df["p_15ymas"] - df["p_60ymas"]

# Construir la variable de relación de dependencia demográfica de la población de 60 y más
df["reldep"] = (df["p_60ymas"] / df["pobtrab"]) * 100

##Importar shapefile del Marco Geostadístico Nacional 2020. Este archivo está almacenado en mi computadora.
mx = gpd.read_file("C:/Users/ALIENWARE/Documents/marcogeoest/mg_sep2019_integrado/conjunto_de_datos/00ent.shp")

#Pegar los datos al shape
mx = mx.merge(df, on="CVEGEO")


##Mapa

fig, ax = plt.subplots(1, figsize=(10,10))

ax.set_title("Relación de dependencia demográfica de la población\n de 60 años y más",
fontsize = 25,fontname = "Century Gothic",fontweight="bold", color = "black")
mx.plot(column='reldep', cmap='GnBu', linewidth=0.1, ax=ax,
        edgecolor='.5', legend=True,
        legend_kwds={'label': "Relación de dependencia\nPoblación de 60 años y más por cada 100 del grupo de 15 a 59 años",
                     'orientation': "horizontal"})
ax.axis('off')
#Fuente
ax.annotate("Nota: La relación de dependencia demográfica de la población\n de 60 años y más de edad es el cociente entre la población de 60 y más años de edad y la población de 15 a 59 años de edad.\n"
            "Fuente: @claudiodanielpc con datos de INEGI. Censo de Población y Vivienda 2020",xy=(0.1, .08), xycoords="figure fraction",
horizontalalignment="left", verticalalignment="top", fontsize=10, color="black",
fontname="Century Gothic")
ax.axis("equal")

#Salvar y mostrar
plt.savefig("reldepmap.png",format="png",dpi=600,transparent=False)
plt.show()


############Caso CDMX por AGEB######
# Llamar a la base de datos
df2 = pd.read_csv("conjunto_de_datos/conjunto_de_datos_ageb_urbana_09_cpv2020.csv")

##Limpieza de base de datos
# Columnas a minúsculas
df2.columns = df2.columns.str.lower()

# Filtrar solo datos por AGEB urbana
df2 = df2[df2["nom_loc"] == "Total AGEB urbana"]

# Crear clave geoestadística
df2["CVEGEO"] =df2['entidad'].astype(str).str.zfill(2)+df2['mun'].astype(str).str.zfill(3)+df2['loc'].astype(str).str.zfill(4)+ df2['ageb'].astype(str).str.zfill(4)


# Dejar las variables con las que se trabajarán

df2 = df2[["CVEGEO", "p_15ymas", "p_60ymas"]]

# Construir la variable de población en edad de trabajar
# Formato de número
df2["p_15ymas"] = pd.to_numeric(df2["p_15ymas"], errors="coerce")
df2["p_60ymas"] = pd.to_numeric(df2["p_60ymas"], errors="coerce")

##Obtener la población de 15 años y hasta 59
df2["pobtrab"] = df2["p_15ymas"] - df2["p_60ymas"]

# Construir la variable de relación de dependencia demográfica de la población de 60 y más
df2["reldep"] = (df2["p_60ymas"] / df2["pobtrab"]) * 100

##Importar shapefile del Marco Geostadístico Nacional 2020. Este archivo está almacenado en mi computadora.
cdmx = gpd.read_file("conjunto_de_datos/09a.shp")

#Pegar los datos al shape
cdmx = cdmx.merge(df2, on="CVEGEO")




##Mapa

fig, ax = plt.subplots(1, figsize=(10,10))

ax.set_title("Relación de dependencia demográfica\n de la población de 60 años y más\n por AGEB urbana",
fontsize = 25,fontname = "Century Gothic",fontweight="bold", color = "black")
cdmx.plot(column='reldep', cmap='GnBu', linewidth=0.1, ax=ax,
        edgecolor='.5', legend=True,
        legend_kwds={'label': "Relación de dependencia\nPoblación de 60 años y más por cada 100 del grupo de 15 a 59 años"})
ax.axis('off')
#Fuente
ax.annotate("Nota: La relación de dependencia demográfica de la población de 60 años y más de edad es el cociente entre la población\n de 60 y más años de edad y la población de 15 a 59 años de edad.\n"
            "Fuente: @claudiodanielpc con datos de INEGI. Censo de Población y Vivienda 2020",xy=(0.1, .08), xycoords="figure fraction",
horizontalalignment="left", verticalalignment="top", fontsize=10, color="black",
fontname="Century Gothic")
ax.axis("equal")

#Salvar y mostrar
plt.savefig("reldepmapcdmx.png",format="png",dpi=600,transparent=False)
plt.show()
