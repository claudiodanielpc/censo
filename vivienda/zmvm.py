##Generar mapa de vivienda deshabitada de la Zona Metropolitana del Valle de México

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import zipfile
import requests

##Seleccionar directorio de trabajo
dir = os.chdir("C:/Users/ALIENWARE/Documents/censo2020/zmvm")



# URLS de datos
urls = ["https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_09_cpv2020_csv.zip",
    "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_13_cpv2020_csv.zip",
        "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_15_cpv2020_csv.zip",
"https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/13_hidalgo.zip",
        "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/09_ciudaddemexico.zip",
        "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/15_mexico.zip"]


# Descomprimir y extraer los archivos


for url in urls:
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()

#Importar archivos
df1=pd.read_csv("conjunto_de_datos/conjunto_de_datos_ageb_urbana_09_cpv2020.csv")
df2=pd.read_csv("conjunto_de_datos/conjunto_de_datos_ageb_urbana_13_cpv2020.csv")
df3=pd.read_csv("conjunto_de_datos/conjunto_de_datos_ageb_urbana_15_cpv2020.csv")


#Pegar bases
frames=[df1,df2,df3]

df=pd.concat(frames)

df.columns = df2.columns.str.lower()
# Filtrar solo datos por AGEB urbana
df = df[df["nom_loc"] == "Total AGEB urbana"]


##Crear claves

df["cve_mun"] =df['entidad'].astype(str).str.zfill(2)+df['mun'].astype(str).str.zfill(3)
df["CVEGEO"] =df['entidad'].astype(str).str.zfill(2)+df['mun'].astype(str).str.zfill(3)+df['loc'].astype(str).str.zfill(4)+ df['ageb'].astype(str).str.zfill(4)
##Identificar a los municipios de la ZMVM

df=df[(df.cve_mun == "09002") | (df.cve_mun == "09003") |
      (df.cve_mun=="09004") | (df.cve_mun=="09005") |
      (df.cve_mun=="09006") | (df.cve_mun=="09007") |
      (df.cve_mun=="09008") | (df.cve_mun=="09009") |
      (df.cve_mun=="09010") | (df.cve_mun=="09011") |
      (df.cve_mun=="09012") | (df.cve_mun=="09013") |
      (df.cve_mun=="09014") | (df.cve_mun=="09015") |
      (df.cve_mun=="09016") | (df.cve_mun=="09017") |
      (df.cve_mun=="13069") | (df.cve_mun=="15002") |
      (df.cve_mun=="15092") | (df.cve_mun=="15108") |
      (df.cve_mun=="15091") | (df.cve_mun=="15099") |
      (df.cve_mun=="15025") | (df.cve_mun=="15016") |
      (df.cve_mun=="15069") | (df.cve_mun=="15057") |
      (df.cve_mun=="15060") | (df.cve_mun=="15015") |
      (df.cve_mun=="15029") | (df.cve_mun=="15095") |
      (df.cve_mun=="15112") | (df.cve_mun=="15046") |
      (df.cve_mun=="15030") | (df.cve_mun=="15044") |
      (df.cve_mun=="15036") | (df.cve_mun=="15053") |
      (df.cve_mun=="15100") | (df.cve_mun=="15038") |
      (df.cve_mun=="15024") | (df.cve_mun=="15121") |
      (df.cve_mun=="15084") | (df.cve_mun=="15010") |
      (df.cve_mun=="15122") | (df.cve_mun=="15094") |
      (df.cve_mun=="15050") | (df.cve_mun=="15011") |
      (df.cve_mun=="15020") | (df.cve_mun=="15059") |
      (df.cve_mun=="15023") | (df.cve_mun=="15028") |
      (df.cve_mun=="15033") | (df.cve_mun=="15017") |
      (df.cve_mun=="15093") | (df.cve_mun=="15083") |
      (df.cve_mun=="15031") | (df.cve_mun=="15070") |
      (df.cve_mun=="15096") | (df.cve_mun=="15109") |
      (df.cve_mun=="15125") | (df.cve_mun=="15061") |
      (df.cve_mun=="15058") | (df.cve_mun=="15022") |
      (df.cve_mun=="15068") | (df.cve_mun=="15081") |
      (df.cve_mun=="15089") | (df.cve_mun=="15037") |
      (df.cve_mun=="15013") | (df.cve_mun=="15065") |
      (df.cve_mun=="15120") | (df.cve_mun=="15039") |
      (df.cve_mun=="15104") | (df.cve_mun=="15075") |
      (df.cve_mun=="15035") | (df.cve_mun=="15103") |
      (df.cve_mun=="15009") | (df.cve_mun=="15034")]

# Dejar las variables con las que se trabajarán

df = df[["CVEGEO", "vivpar_des"]]
df["vivpar_des"] = pd.to_numeric(df["vivpar_des"], errors="coerce")


###Traer los shapes y consolidar

#Agebs
s1= gpd.read_file("conjunto_de_datos/09a.shp")
s2= gpd.read_file("conjunto_de_datos/13a.shp")
s3= gpd.read_file("conjunto_de_datos/15a.shp")


#Crear base general
ageb=s1.append(s2)
ageb=ageb.append(s3)

#Clave de municipio para obtener solo las Agebs de la ZMVM

ageb["mun"] =ageb['CVE_ENT'].astype(str).str.zfill(2)+ageb['CVE_MUN'].astype(str).str.zfill(3)


ageb=ageb[(ageb.mun == "09002") | (ageb.mun == "09003") |
      (ageb.mun=="09004") | (ageb.mun=="09005") |
      (ageb.mun=="09006") | (ageb.mun=="09007") |
      (ageb.mun=="09008") | (ageb.mun=="09009") |
      (ageb.mun=="09010") | (ageb.mun=="09011") |
      (ageb.mun=="09012") | (ageb.mun=="09013") |
      (ageb.mun=="09014") | (ageb.mun=="09015") |
      (ageb.mun=="09016") | (ageb.mun=="09017") |
      (ageb.mun=="13069") | (ageb.mun=="15002") |
      (ageb.mun=="15092") | (ageb.mun=="15108") |
      (ageb.mun=="15091") | (ageb.mun=="15099") |
      (ageb.mun=="15025") | (ageb.mun=="15016") |
      (ageb.mun=="15069") | (ageb.mun=="15057") |
      (ageb.mun=="15060") | (ageb.mun=="15015") |
      (ageb.mun=="15029") | (ageb.mun=="15095") |
      (ageb.mun=="15112") | (ageb.mun=="15046") |
      (ageb.mun=="15030") | (ageb.mun=="15044") |
      (ageb.mun=="15036") | (ageb.mun=="15053") |
      (ageb.mun=="15100") | (ageb.mun=="15038") |
      (ageb.mun=="15024") | (ageb.mun=="15121") |
      (ageb.mun=="15084") | (ageb.mun=="15010") |
      (ageb.mun=="15122") | (ageb.mun=="15094") |
      (ageb.mun=="15050") | (ageb.mun=="15011") |
      (ageb.mun=="15020") | (ageb.mun=="15059") |
      (ageb.mun=="15023") | (ageb.mun=="15028") |
      (ageb.mun=="15033") | (ageb.mun=="15017") |
      (ageb.mun=="15093") | (ageb.mun=="15083") |
      (ageb.mun=="15031") | (ageb.mun=="15070") |
      (ageb.mun=="15096") | (ageb.mun=="15109") |
      (ageb.mun=="15125") | (ageb.mun=="15061") |
      (ageb.mun=="15058") | (ageb.mun=="15022") |
      (ageb.mun=="15068") | (ageb.mun=="15081") |
      (ageb.mun=="15089") | (ageb.mun=="15037") |
      (ageb.mun=="15013") | (ageb.mun=="15065") |
      (ageb.mun=="15120") | (ageb.mun=="15039") |
      (ageb.mun=="15104") | (ageb.mun=="15075") |
      (ageb.mun=="15035") | (ageb.mun=="15103") |
      (ageb.mun=="15009") | (ageb.mun=="15034")]

#Pegar los datos al shape
ageb = ageb.merge(df, how="left",on="CVEGEO")
#Reemplazar ceros con Nan
ageb['vivpar_des']=ageb['vivpar_des'].replace(0, np.nan)


#Municipios
s1= gpd.read_file("conjunto_de_datos/09mun.shp")
s2= gpd.read_file("conjunto_de_datos/13mun.shp")
s3= gpd.read_file("conjunto_de_datos/15mun.shp")

muni=s1.append(s2)
muni=muni.append(s3)

muni=muni[(muni.CVEGEO == "09002") | (muni.CVEGEO == "09003") |
      (muni.CVEGEO=="09004") | (muni.CVEGEO=="09005") |
      (muni.CVEGEO=="09006") | (muni.CVEGEO=="09007") |
      (muni.CVEGEO=="09008") | (muni.CVEGEO=="09009") |
      (muni.CVEGEO=="09010") | (muni.CVEGEO=="09011") |
      (muni.CVEGEO=="09012") | (muni.CVEGEO=="09013") |
      (muni.CVEGEO=="09014") | (muni.CVEGEO=="09015") |
      (muni.CVEGEO=="09016") | (muni.CVEGEO=="09017") |
      (muni.CVEGEO=="13069") | (muni.CVEGEO=="15002") |
      (muni.CVEGEO=="15092") | (muni.CVEGEO=="15108") |
      (muni.CVEGEO=="15091") | (muni.CVEGEO=="15099") |
      (muni.CVEGEO=="15025") | (muni.CVEGEO=="15016") |
      (muni.CVEGEO=="15069") | (muni.CVEGEO=="15057") |
      (muni.CVEGEO=="15060") | (muni.CVEGEO=="15015") |
      (muni.CVEGEO=="15029") | (muni.CVEGEO=="15095") |
      (muni.CVEGEO=="15112") | (muni.CVEGEO=="15046") |
      (muni.CVEGEO=="15030") | (muni.CVEGEO=="15044") |
      (muni.CVEGEO=="15036") | (muni.CVEGEO=="15053") |
      (muni.CVEGEO=="15100") | (muni.CVEGEO=="15038") |
      (muni.CVEGEO=="15024") | (muni.CVEGEO=="15121") |
      (muni.CVEGEO=="15084") | (muni.CVEGEO=="15010") |
      (muni.CVEGEO=="15122") | (muni.CVEGEO=="15094") |
      (muni.CVEGEO=="15050") | (muni.CVEGEO=="15011") |
      (muni.CVEGEO=="15020") | (muni.CVEGEO=="15059") |
      (muni.CVEGEO=="15023") | (muni.CVEGEO=="15028") |
      (muni.CVEGEO=="15033") | (muni.CVEGEO=="15017") |
      (muni.CVEGEO=="15093") | (muni.CVEGEO=="15083") |
      (muni.CVEGEO=="15031") | (muni.CVEGEO=="15070") |
      (muni.CVEGEO=="15096") | (muni.CVEGEO=="15109") |
      (muni.CVEGEO=="15125") | (muni.CVEGEO=="15061") |
      (muni.CVEGEO=="15058") | (muni.CVEGEO=="15022") |
      (muni.CVEGEO=="15068") | (muni.CVEGEO=="15081") |
      (muni.CVEGEO=="15089") | (muni.CVEGEO=="15037") |
      (muni.CVEGEO=="15013") | (muni.CVEGEO=="15065") |
      (muni.CVEGEO=="15120") | (muni.CVEGEO=="15039") |
      (muni.CVEGEO=="15104") | (muni.CVEGEO=="15075") |
      (muni.CVEGEO=="15035") | (muni.CVEGEO=="15103") |
      (muni.CVEGEO=="15009") | (muni.CVEGEO=="15034")]

#Ciudad de México
cdmx= gpd.read_file("conjunto_de_datos/09ent.shp")



##Mapa

fig, ax = plt.subplots(1, figsize=(7.5,7.5))

ax.set_title("Zona Metropolitana del Valle de México\nViviendas particulares deshabitadas\n por AGEB urbana",
fontsize = 20,fontname = "Century Gothic",fontweight="bold", color = "black")
#Capa AGEB
ageb.plot(column='vivpar_des', cmap='YlOrBr', linewidth=0.1, ax=ax,
        edgecolor='.5', legend=True,
        legend_kwds={'label': "Número de viviendas"})
#Capa municipios
muni.plot(linewidth=0.3, ax=ax,
        edgecolor='.5', color="#1C00ff00")
#Capa CDMX
cdmx.plot(linewidth=0.6, ax=ax,
        edgecolor="red", color="#1C00ff00")

ax.axis('off')
#Fuente
ax.annotate("Fuente: @claudiodanielpc con datos de INEGI.\nCenso de Población y Vivienda 2020",xy=(0.1, .08), xycoords="figure fraction",
horizontalalignment="left", verticalalignment="top", fontsize=13, color="black",
fontname="Century Gothic")
ax.axis("equal")

#Salvar y mostrar
plt.savefig("vivdeshabzmvm.png",format="png",dpi=600,transparent=False)
plt.show()


