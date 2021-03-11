
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import zipfile
import requests
import os
import io


##Seleccionar directorio de trabajo y crear carpeta
dir = os.chdir ('C:/Users/ALIENWARE/Documents/censo2020 ')

#Se crea carpeta en donde se almacenarán los mapas
carpeta ="pob"

if not os.path.exists (carpeta):
    os.makedirs (carpeta)


urls = ["https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip",
        "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/mg_2020_integrado.zip"
        ]


# Descomprimir y extraer los archivos
for url in urls:
    r = requests.get (url)
    z = zipfile.ZipFile (io.BytesIO (r.content ))
    z.extractall()

    ##Leer el csv, seleccionar las variables y asignar el tipo


df = pd.read_csv( "ITER_NALCSV20.csv",
                  na_values=["N/D","*"],
                  usecols=["ENTIDAD",
                           "NOM_ENT",
                           "MUN",
                           "NOM_LOC",
                            "POBTOT"
                  ],
                  dtype={"ENTIDAD": str,
                           "NOM_ENT" :str,
                           "MUN": str,
                           "NOM_LOC": str,
                            "POBTOT": int
                  }
                  )

##Dejar los datos únicamente a nivel municipal

df =df[df["NOM_LOC"].isin (["Total del Municipio" ])]

##Construir clave para pegar con shape

df["CVEGEO"] =(df['ENTIDAD'].astype( str ).str.zfill( 2 ) +
                df['MUN'].astype( str ).str.zfill( 3 ))

##Renombrar variable
df = df.rename( columns={'ENTIDAD': 'CVE_ENT'} )

##Modificar variable a string
df["CVE_ENT"] = (df["CVE_ENT"].astype( str ).str.zfill( 2 ))

##Eliminar columnas innecesarias
df = df.drop( columns=['MUN','NOM_LOC',"CVE_ENT"] )

# Crear variable de porcentaje de población
df["pct"] = df["POBTOT"] / df.groupby( ["NOM_ENT"] )["POBTOT"].transform( "sum" ) * 100

##Importar shapes
munshp = gpd.read_file(
    "conjunto_de_datos/00mun.shp",
    dtype={
        "CVE_ENT": str,
        "CVE_MUN": str,
        },
    )

# Pegar datos a shape
munshp = munshp.merge(
    df,
    how="left",
    on="CVEGEO"
    )


#Se crea diccionario con los nombres de las entidades para agregarlos en el título
dicc_ent = munshp.drop_duplicates( subset='CVE_ENT' ).set_index( "CVE_ENT" )["NOM_ENT"].to_dict()


#Loop para generar los mapas de población de las 32 entidades federativas de México



for z in munshp['CVE_ENT'].unique():


    fig,ax = plt.subplots( figsize=(12,12) )
    ax.set_title( f'{dicc_ent[z]}. Población por municipio',
                  fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )

    munshp[munshp['CVE_ENT'] == z].plot( column="pct",
                  cmap="YlOrRd",
                  linewidth=0.2,ax=ax,
                  edgecolor='.5',legend=True,
                  legend_kwds={
                               'orientation': "horizontal"
                                })
    #Se modifica la barra de color de la coropleta
    cb = ax.get_figure().get_axes()[1]
    cb.set_title("%",fontsize=20)
    cb.tick_params(labelsize=20)
    ax.axis( 'off' )
    
    if z == "06": # Colima
        ax.set_ylim(0.74e6, 0.85e6)
        ax.set_xlim(2.19e6, 2.38e6)
    
    # Fuente
    ax.annotate( 'Fuente: Elaborado por CANADEVI Nacional. Gerencia de Fondos de Vivienda\n'
                 'Coordinación de Indicadores de Vivienda con datos de INEGI. Censo de Población y Vivienda 2020',
                 xy=(0.1,.08),
                 xycoords='figure fraction',
                 horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
                 fontname='Century Gothic' )

        # Salvar

    plt.savefig( f'pob/{z}.png',format='png',
                 dpi=600,transparent=False )
