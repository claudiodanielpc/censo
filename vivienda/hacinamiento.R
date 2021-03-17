##Código para calcular el hacinamiento con los datos del Censo 2020

##Borrar datos del entorno
rm(list=ls())


#Directorio
setwd("C:/Users/ALIENWARE/Documents/censo2020/")

##Crear folders de almacenamiento
dir.create("microdatos")

#Paquetería
if(!require('pacman')) install.packages('pacman')
pacman::p_load(tidyverse, kableExtra)



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

#Descarga de catálogo de entidades federativas====

#Url del catálogo para crear la lista
urlcat<-"https://www.inegi.org.mx/contenidos/app/ageeml/catun_entidad.zip"


#Se crea tempfile para no almacenar los zips
temp<-tempfile()
##Descargar y extraer catálogo
download.file(urlcat,
              destfile = temp)

unzip(temp,
      exdir = "microdatos")
unlink(temp)

#Leer archivo de catálogo y arreglar

cat<-read.csv("microdatos/AGEEML_20211271319772.csv",
              encoding ="latin1" )%>%
  #Remover la última fila
  slice(1:(n()-1))%>%
  #Renombrar y seleccionar la variable de interés
  rename(ent=1,
         nom_ent=2)%>%
  select(ent,nom_ent)

#Datos Censo. Lectura y limpieza====
censo<-read.csv("microdatos/Viviendas00.csv")%>%
  janitor::clean_names()%>%
  #Seleccionar variables
  select(ent,mun,cobertura,estrato,upm,clavivp,
         factor, totcuart,numpers)%>%
  #Omitir viviendas móviles, locales y refugios
  filter(clavivp<7 | clavivp==99)%>%
  #Condición de hacinamiento
  mutate(hac = if_else(
    ((numpers / totcuart) > 2.5),
    "En hacinamiento",
    "Fuera de hacinamiento"
  )
  )%>%
  #Pegar nombres de las entidades
    left_join(cat)

##Gráfica de pastel nacional====
censo%>%
group_by(hac)%>%
  ##Ordenar y suma acumulada para poder acomodar las etiquetas
  tally(wt=factor)%>%
  mutate(pct=n/sum(n)*100)%>%
    arrange(desc(pct)) %>% 
  mutate(pct_cumsum=cumsum(pct))%>%

  ggplot(., aes(x="", y=pct, fill=hac)) +
  geom_bar(stat="identity", width=1, color="white") +
  coord_polar("y", start=0) +
  theme_void() + 
#Ubicación de las etiquetas
    geom_text(aes(y = pct_cumsum-pct/2, 
                  label = format(round(pct,1))),
                color = "black", size=8, fontface="bold") +
  scale_fill_manual("Condición",values=c("#e6550d","#bdbdbd"))+
  labs(
    title ="México. Viviendas particulares habitadas\npor condición de hacinamiento de sus ocupantes, 2020",
    subtitle = "(%)",
    caption = "\nNota: Se excluye la información de los locales no construidos para habitación, viviendas móviles y refugios .\n
Fuente: @claudiodanielpc con datos de INEGI. Censos de Población y Vivienda, 2020.")+
  theme(plot.title = element_text(hjust = 0, size=25,face="bold"),
        plot.subtitle = element_text(hjust = 0, size=15, 
                                     face="italic"),
        plot.caption = element_text(hjust = 0,size=12),
        legend.position = "bottom",
        text=element_text(size=20))

##Salvar
ggsave("microdatos/hacinamiento.png",
       height=10, width=20, units='in', dpi=300)


##Gráfica por entidad federativa====

censo%>%
  group_by(hac,nom_ent)%>%
  tally(wt=factor)%>%
  mutate(pct=n/sum(n)*100)%>%
  filter(hac=="En hacinamiento")%>%
  mutate(nom_ent = fct_reorder(nom_ent, pct))%>%
#Gráfico de barras
    ggplot(.,aes(nom_ent,pct))+
  geom_bar(stat="identity", fill="#c994c7", width=.8) +
  geom_text(aes(label=format(round(pct,1))), vjust=0.5,hjust=0, 
            size=7,fontface="bold")+
  coord_flip() +
  xlab("") +
  theme_minimal()+
  labs(
    title = "Viviendas particulares con ocupantes en condición de hacinamiento por entidad federativa",
    subtitle = "% del total del parque habitacional de cada entidad federativa",
    y = "%",
    x="",
    caption = "
Fuente: @claudiodanielpc con datos de INEGI. Censo de Población y Vivienda, 2020."
  )+
  theme(plot.title = element_text(hjust = 0, size=25,face="bold"),
        plot.subtitle = element_text(hjust = 0, size=18, face="italic"),
        plot.caption = element_text(hjust = 0,size=12),
        legend.position = "none",
        axis.text.x = element_blank(),
        text=element_text(size=20)
        )
#Salvar
ggsave("microdatos/hacentfed.png", height=10, width=20, units='in', dpi=300)
