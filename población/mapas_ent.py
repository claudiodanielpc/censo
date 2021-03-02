##Mapas Jalisco y Sinaloa

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import zipfile
import requests
import os
import io

##Seleccionar directorio de trabajo
dir = os.chdir( 'C:/Users/ALIENWARE/Documents/censo2020/jal' )


urls = ['https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/ageb_manzana/RESAGEBURB_14_2020_csv.zip',
        'https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/14_jalisco.zip',
        'https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/ageb_manzana/RESAGEBURB_25_2020_csv.zip',
        'https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/25_sinaloa.zip'
        ]

# Descomprimir y extraer los archivos


for url in urls:
    r = requests.get( url )
    z = zipfile.ZipFile( io.BytesIO( r.content ) )
    z.extractall()


##Jalisco

##Abrir archivo de datos


df = pd.read_csv( 'RESAGEBURB_14CSV20.csv',
                  na_values=['N/D','*'],
                  usecols=[
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
                  dtype={
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
                  )

##Dejar únicamente los datos a nivel manzana
nivelesn = {
    'Total de la entidad',
    'Total del municipio',
    'Total de la localidad urbana',
    'Total AGEB urbana'
    }

df = df[~df['NOM_LOC'].isin( nivelesn )]

# Municipio

df['cve_mun'] = (
        df['ENTIDAD'].str.zfill( 2 ) +
        df['MUN'].str.zfill( 3 )
)

# Manzana
df['CVEGEO'] = (
        df['ENTIDAD'].str.zfill( 2 ) +
        df['MUN'].str.zfill( 3 ) +
        df['LOC'].str.zfill( 4 ) +
        df['AGEB'].str.zfill( 4 ) +
        df['MZA'].str.zfill( 3 )
)

##Filtrar municipios a mapear


municipios = {
    '14008',
    '14023',
    '14063',
    '14073'
    }

df = df[
    df['cve_mun'].isin( municipios )
]

# Crear porcentaje de viviendas particulares habitadas con internet
df['porvivint'] = df['VPH_INTER'] / df['TVIVPARHAB'] * 100

# Importar shapes

mza = gpd.read_file(
    'conjunto_de_datos/14m.shp' )


# Crear claves para filtrar
mza['municipio'] = (
        mza['CVE_ENT'].str.zfill( 2 ) +
        mza['CVE_MUN'].str.zfill( 3 )
)

#Dejar únicamente las manzanas de los municipios requeridos

mza= mza[
    mza['municipio'].isin( municipios )
]

    # Pegar los datos al shape
mza = mza.merge( df,how='left',on='CVEGEO' )


####MAPAS###
##Arandas
mza1 = mza[mza['municipio'] == '14008']

##Internet

fig,ax = plt.subplots( figsize=(12,12) )

ax.set_title( 'Arandas, Jalisco\nViviendas particulares habitadas\nque disponen de internet por manzana\n(%)',
              fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )
#
mza1.plot( column='porvivint',cmap='YlOrBr',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': '% del total de viviendas particulares habitadas'} )

ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'arandas_internet.png',format='png',dpi=600,transparent=False )
plt.show()



##Grado escolaridad

fig,ax = plt.subplots( figsize=(12,12) )

ax.set_title( 'Arandas, Jalisco\nGrado promedio de escolaridad\npor manzana',
              fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )
mza1.plot( column='GRAPROES',cmap='YlGn',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': 'Grado promedio de escolaridad'} )
ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'arandas_gradesc.png',format='png',dpi=600,transparent=False )
plt.show()



# Zapotlán el Grande
mza1 = mza[mza['municipio'] == '14023']


##Internet

fig,ax = plt.subplots( figsize=(12,12) )

ax.set_title(
    'Zapotlán el Grande, Jalisco\nViviendas particulares habitadas\nque disponen de internet por manzana\n(%)',
    fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )
#
mza1.plot( column='porvivint',cmap='YlOrBr',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': '% del total de viviendas particulares habitadas'} )
ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'zapotlánelgrande_internet.png',format='png',dpi=600,transparent=False )
plt.show()

##Grado escolaridad

fig,ax = plt.subplots( figsize=(12,12) )

ax.set_title( 'Zapotlán el Grande, Jalisco\nGrado promedio de escolaridad\npor manzana',
              fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )

mza1.plot( column='GRAPROES',cmap='YlGn',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': 'Grado promedio de escolaridad'} )
ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'zapotlánelgrande_gradesc.png',format='png',dpi=600,transparent=False )
plt.show()

# Ocotlán

mza1 = mza[mza['municipio'] == '14063']


##Internet

fig,ax = plt.subplots( figsize=(12,12) )

ax.set_title( 'Ocotlán, Jalisco\nViviendas particulares habitadas\nque disponen de internet por manzana\n(%)',
              fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )

mza1.plot( column='porvivint',cmap='YlOrBr',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': '% del total de viviendas particulares habitadas'} )
ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'ocotlán_internet.png',format='png',dpi=600,transparent=False )
plt.show()

##Grado escolaridad

fig,ax = plt.subplots( figsize=(12,12) )

ax.set_title( 'Ocotlán, Jalisco\nGrado promedio de escolaridad\npor manzana',
              fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )
#
mza1.plot( column='GRAPROES',cmap='YlGn',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': 'Grado promedio de escolaridad'} )
ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'ocotlán_gradesc.png',format='png',dpi=600,transparent=False )
plt.show()

# San Juan de los Lagos
mza1 = mza[mza['municipio'] == '14073']


##Internet

fig,ax = plt.subplots( figsize=(12,12) )


ax.set_title(
    'San Juan de los Lagos, Jalisco\nViviendas particulares habitadas\nque disponen de internet por manzana\n(%)',
    fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )
#
mza1.plot( column='porvivint',cmap='YlOrBr',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': '% del total de viviendas particulares habitadas'} )
ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'sanjuandeloslagos_internet.png',format='png',dpi=600,transparent=False )
plt.show()

##Grado escolaridad

fig,ax = plt.subplots( figsize=(12,12) )

ax.set_title( 'San Juan de los Lagos, Jalisco\nGrado promedio de escolaridad\npor manzana',
              fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )
#
mza1.plot( column='GRAPROES',cmap='YlGn',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': 'Grado promedio de escolaridad'} )
ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'sanjuandeloslagos_gradesc.png',format='png',dpi=600,transparent=False )
plt.show()





##Sinaloa

##Abrir archivo de datos


df = pd.read_csv( 'RESAGEBURB_25CSV20.csv',
                  na_values=['N/D','*'],
                  usecols=[
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
                  dtype={
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
                  )

##Dejar únicamente los datos a nivel manzana
nivelesn = {
    'Total de la entidad',
    'Total del municipio',
    'Total de la localidad urbana',
    'Total AGEB urbana'
    }

df = df[~df['NOM_LOC'].isin( nivelesn )]

# Municipio

df['cve_mun'] = (
        df['ENTIDAD'].str.zfill( 2 ) +
        df['MUN'].str.zfill( 3 )
)

# Manzana
df['CVEGEO'] = (
        df['ENTIDAD'].str.zfill( 2 ) +
        df['MUN'].str.zfill( 3 ) +
        df['LOC'].str.zfill( 4 ) +
        df['AGEB'].str.zfill( 4 ) +
        df['MZA'].str.zfill( 3 )
)

##Filtrar municipios a mapear


municipios = {
    '25011'
    }

df = df[
    df['cve_mun'].isin( municipios )
]

# Crear porcentaje de viviendas particulares habitadas con internet
df['porvivint'] = df['VPH_INTER'] / df['TVIVPARHAB'] * 100

# Importar shapes

mza = gpd.read_file(
    'conjunto_de_datos/25m.shp' )


# Crear claves para filtrar
mza['municipio'] = (
        mza['CVE_ENT'].str.zfill( 2 ) +
        mza['CVE_MUN'].str.zfill( 3 )
)

#Dejar únicamente las manzanas de los municipios requeridos

mza= mza[
    mza['municipio'].isin( municipios )
]

    # Pegar los datos al shape
mza = mza.merge( df,how='left',on='CVEGEO' )


####MAPAS###
##Guasave
mza1 = mza[mza['municipio'] == '25011']

##Internet

fig,ax = plt.subplots( figsize=(12,12) )

ax.set_title( 'Guasave, Sinaloa\nViviendas particulares habitadas\nque disponen de internet por manzana\n(%)',
              fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )
#
mza1.plot( column='porvivint',cmap='YlOrBr',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': '% del total de viviendas particulares habitadas'} )

ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'guasave_internet.png',format='png',dpi=600,transparent=False )
plt.show()



##Grado escolaridad

fig,ax = plt.subplots( figsize=(12,12) )

ax.set_title( 'Guasave, Sinaloa\nGrado promedio de escolaridad\npor manzana',
              fontsize=20,fontname='Century Gothic',fontweight='bold',color='black' )
mza1.plot( column='GRAPROES',cmap='YlGn',linewidth=0.1,ax=ax,
           edgecolor='.2',legend=True,
           legend_kwds={'label': 'Grado promedio de escolaridad'} )
ax.axis( 'off' )
# Fuente
ax.annotate( 'Fuente: Elaboración propia con datos de INEGI.\nCenso de Población y Vivienda 2020',xy=(0.1,.08),
             xycoords='figure fraction',
             horizontalalignment='left',verticalalignment='top',fontsize=13,color='black',
             fontname='Century Gothic' )
ax.axis( 'equal' )

# Salvar y mostrar
plt.savefig( 'guasave_gradesc.png',format='png',dpi=600,transparent=False )
plt.show()