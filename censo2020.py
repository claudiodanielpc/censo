##Traer los datos del censo para analizar vivienda deshabitada

import pandas as pd
import requests, io, os, zipfile
import matplotlib.pyplot as plt

##Seleccionar directorio de trabajo
dir = os.chdir("C:/Users/ALIENWARE/Documents/censo2020")

# URL de los Censos 2020 y 2010

urls = ["https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/iter/ITER_NAL_2020_csv.zip",
        "https://www.inegi.org.mx/contenidos/programas/ccpv/2010/datosabiertos/iter_nal_2010_csv.zip"]

# Descomprimir los archivos de los Censos 2010 y Censo 2020

for url in urls:
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()

##Leer los archivos. Se extraen las columnas con las que se trabajarán
##Censo 2020
df1 = pd.read_csv("ITER_NALCSV20.csv", usecols=["NOM_ENT", "NOM_LOC",
                                                "TVIVPARHAB", "VIVPAR_DES"])

##Censo 2010
df2 = pd.read_csv("iter_00_cpv2010/conjunto_de_datos/iter_00_cpv2010.csv",
                  usecols=["nom_ent", "nom_loc", "tvivparhab", "vivpar_des"])

###
# Limpiar bases
##Transformar a minúsculas la base del censo 2020
df1.columns = df1.columns.str.lower()

##Renombrar Distrito Federal a CDMX en censo 2010
df2['nom_ent'] = df2['nom_ent'].replace(['Distrito Federal'], 'Ciudad de México')

##Filtrar para dejar únicamente los valores de las entidades
df1 = df1[df1["nom_loc"] == "Total de la Entidad"]
df2 = df2[df2["nom_loc"] == "Total de la Entidad"]

##Eliminar variable de nombre de localidad
for df in df1, df2:
    df.drop(columns=["nom_loc"], inplace=True)

##Pegar bases
dfmerge = pd.merge(df1, df2, on="nom_ent")

##Renombrar variables
dfmerge.rename(columns={'tvivparhab_x': 'tvivparhab2020',
                        'vivpar_des_x': 'deshab2020',
                        'tvivparhab_y': 'tvivparhab2010',
                        'vivpar_des_y': 'deshab2010'}, inplace=True)

##transformar a numérico para poder operar
for column in dfmerge.columns:
    try:
        dfmerge[column] = pd.to_numeric(dfmerge[column])
    except (ValueError, AttributeError):
        pass

##Calculamos las tasas de crecimiento promedio anual
##Vivienda particular habitada
dfmerge["tcmavivhab"] = (((dfmerge["tvivparhab2020"] / dfmerge["tvivparhab2010"]) ** (1 / 10)) - 1) * 100

##Vivienda particular deshabitada
dfmerge["tcmavivdes"] = (((dfmerge["deshab2020"] / dfmerge["deshab2010"]) ** (1 / 10)) - 1) * 100

#Diferencia de tasas
dfmerge["dif"] =dfmerge["tcmavivdes"]-dfmerge["tcmavivhab"]



#######
##Se crea una gráfica de dispersión para  comparar las tasas

dfmerge.plot(kind="scatter",figsize=(19, 7),color="#feb24c",
x="tcmavivhab",y="tcmavivdes", s=40)

##Etiquetas de todos los puntos (se omiten ya que se enciman)
#for i, txt in enumerate(dfmerge.nom_ent):
 #   plt.annotate(txt, (dfmerge.tcmavivhab.iat[i],dfmerge.tcmavivdes.iat[i]))

##anotaciones puntuales
plt.text(2.2, 6.6, 'Chiapas')
plt.text(3,-5.7,"Baja California")
plt.text(4.6,1.1,"Quintana Roo")
#diagonal identidad
plt.plot([-7,7],[-7,7],color="black")
#Título
plt.title("Tasa de crecimiento promedio anual de la vivienda particular habitada y particular deshabitada por entidad federativa, 2010-2020\n (%)",
fontsize=14,fontweight="bold", loc="left")
#Límites de x, y
plt.xlim([-7,7])
plt.ylim([-7,7])
##títulos de ejes
plt.xlabel('Tasa de crecimiento promedio anual de viviendas particulares habitadas\nFuente: @claudiodanielpc con información de INEGI. Censo de Población y Vivienda 2020')
plt.ylabel("Tasa de crecimiento promedio anual de viviendas particulares deshabitadas")

##Guardar y mostrar la gráfica
plt.savefig("vivhabdeshab.png",format="png",dpi=600,transparent=False)
plt.show()