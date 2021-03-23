##Código para calcular el porcentaje de población con carencia por calidad y espacios de la vivienda 
#con los datos del Censo 2020

##Borrar datos del entorno
rm(list=ls())


#Directorio
setwd("C:/Users/ALIENWARE/Documents/censo2020/")

##Crear folders de almacenamiento
dir.create("microdatos")

#Paquetería
if(!require('pacman')) install.packages('pacman')
pacman::p_load(tidyverse,  
               kableExtra,
               sf,
               extrafont,
               srvyr)

#Descarga de archivo muestra Censo 2020====
#url<-"https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/Censo2020_CA_eum_csv.zip"


#Se crea tempfile para no almacenar los zips
#temp<-tempfile()
##Descargar y extraer catálogo
#download.file(url,mode = "wb",
#             destfile = temp)

#unzip(temp,
#     exdir = "microdatos")
#unlink(temp)


#Datos Censo. Lectura y limpieza====
censo<-read.csv("microdatos/Viviendas00.csv")%>%
  janitor::clean_names()%>%
  #Seleccionar variables
  select(ent,mun,cobertura,estrato,upm,clavivp,
         factor, totcuart,numpers,paredes,techos,
         pisos)%>%
  #Omitir viviendas móviles, locales y refugios
  filter(clavivp<7 | clavivp==99)%>%
  #Condición de carencia
  mutate(carencia = if_else(
    ((numpers / totcuart) > 2.5) |
      (paredes %in% 1:5) |
      (techos %in% 1:2) |
      (pisos == 1) ,
    "Carencia",
    "No carencia"
  )
) %>%
  #Construir clavegeostadística
  ##Agregar cero a entidad
  mutate(ent=ifelse(nchar(ent)==1,
                    paste0("0",ent),
                    ent))%>%
  ##Agregar ceros a municipio
  mutate(mun=ifelse(nchar(mun)==1,
                    paste0("00",mun),
                    ifelse(nchar(mun)==2,
                           paste0("0",mun),
                           mun)))%>%
  ##Crear clave geoestadística  
  mutate(cvegeo=paste0(ent,mun))%>%
  #Declarar el factor de expansión
  as_survey(weights=factor)%>%
  #Obtener total de personas y de aquellas con carencia
  group_by(carencia,cvegeo)%>%
  summarise(perscar=survey_total(numpers))%>%
  ungroup()%>%
  group_by(cvegeo)%>%
  mutate(totper=sum(pers))%>%
  filter(carencia=="Carencia")%>%
  #Calcular porcentaje
  mutate(pct=pers/totper*100)%>%
  select(cvegeo,pct)


##Traer shape
#Entidad
ent<-st_read("conjunto_de_datos/00ent.shp")


#Municipios
mun<-st_read("conjunto_de_datos/00mun.shp")%>%
  janitor::clean_names()%>%
  #Pegar datos de hacinamiento
  left_join(censo)


# Mapa

ggplot() +
  # Capa con datos de los municipios
  geom_sf(data=mun,aes(fill = pct),
          colour = "#1C00ff00", size = 0.07) +
  #Capa entidades
  geom_sf(data=ent, color = 'black',alpha=0)+
  # Agrega título, subtítulo y fuente
  labs(title = "Porcentaje de población con carencia por 
calidad y espacios de la vivienda, 2020",
       subtitle = "% del total de habitantes de cada municipio",
       caption = "
Fuente: @claudiodanielpc con datos de INEGI. Censo de Población y Vivienda 2020.") +
  #Paleta y título de la leyenda
  scale_fill_distiller("% Población con carencia",
                       palette = "YlOrBr", direction = 1,
                       na.value = "white")+
  theme_void()+
  theme(plot.title = element_text(hjust = 0, size=30,face="bold"),
        plot.subtitle = element_text(hjust = 0, size=20, face="italic"),
        plot.caption = element_text(hjust = 0,size=15),
        legend.position="right",
        #Fuente y tamaño
        text=element_text("Century Gothic",
                          size=20))


#Salvar
ggsave("calespvivi.png", height = 10,
       width = 20, units="in", dpi=300)