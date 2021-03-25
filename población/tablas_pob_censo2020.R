#Cuadros de los 5 municipios con mayor número de habitantes por entidad federativa

##Borrar datos del entorno
rm(list=ls())


##Ruta de almacenamiento de los archivos generados
setwd("C:/Users/ALIENWARE/Documents/censo2020/pob")


if(!require('pacman')) install.packages('pacman')
pacman::p_load(tidyverse, kableExtra)


##Url ITER Censo 2020

url<-"https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip"


#Descarga de datos====

#Se crea tempfile para no almacenar los zips
temp<-tempfile()
##Descargar y extraer
download.file(url,
              destfile = temp)

unzip(temp,
      exdir = "C:/Users/ALIENWARE/Documents/censo2020")
unlink(temp)


#Lectura y limpieza====
##Importar datos y limpiar
iter<-read.csv("C:/Users/ALIENWARE/Documents/censo2020/iter_00_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_00CSV20.csv",
              encoding ="UTF-8",check.names = T)%>%
  janitor::clean_names()%>%
  ##Renombrar variable de clave de la entidad y darle formato
  rename(entidad=1)%>%
  mutate(entidad=ifelse(nchar(entidad)==1,
                        paste0("0",entidad),entidad))%>%
  #Seleccionar variables a ocupar
  select("entidad","nom_ent", "nom_mun",
         "nom_loc", "pobtot")%>%
  #Filtrar para dejar únicamente datos municipales
    filter(nom_loc=="Total del Municipio")%>%
  ##Calcular porcentaje
  group_by(nom_ent)%>%
  mutate(pct=pobtot/sum(pobtot)*100)%>%
  ##Rankear
  mutate(rank = rank(-pct, ties.method = "last"))%>%
  #Dejar los cinco principales municipios
  filter(rank<=5)%>%
  ungroup()%>%
  ##Ordenar datos de mayor a menor por entidad
  arrange(nom_ent,desc(pobtot))%>%
  #Formato de números
  mutate(pobtot=format(pobtot,big.mark = ","),
         pct=format(round(pct,1)))



#Generar nombres para filtro y números para guardar los archivos
entidades<-unique(iter$nom_ent)
num_ent<-unique(iter$entidad)
  

#Tablas de los cinco principales municipios de acuerdo a población por entidad federativa====


  for (i in seq_along(entidades)) {
    
    iter%>%
      #Filtro de entidad
      filter(nom_ent==entidades[i])%>%
      #Tirar las variables que no se ocuparán
      select(nom_mun,pobtot,pct)%>%    
      ##Crear tabla
      kable(caption=paste(text_spec(entidades[i],bold=T, 
                                    color="black",font_size = 30 ),
                          text_spec(". ",
                                    bold=T, color="black",font_size = 30),
                          text_spec("Principales municipios por número de habitantes",
                                    bold=T, color="black",font_size = 30),
                          sep="\n"),
            format="html",
            align = "c",
            col.names = c("Municipio",
                          "Población",
                          "% del total"))%>%
      kable_styling(full_width = F, font_size = 20,
                    html_font = "Century Gothic")%>%
      row_spec(0, bold = F, color = "black", background = "#feb24c")%>%
      footnote(general = "Elaborado por CANADEVI Nacional. Gerencia de Fondos de Vivienda. 
Coordinación de Indicadores de Vivienda con datos de INEGI. Censo de Población y Vivienda, 2020.",
               general_title = "
Fuente: ",
               threeparttable=T)%>%
      #Salvar
      as_image(file=paste0("C:/Users/ALIENWARE/Documents/censo2020/pob/",
                           num_ent[i],"_1.png"))
  }