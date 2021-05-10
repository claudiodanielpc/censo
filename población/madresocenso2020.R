

##Código para calcular el porcentaje de población con carencia por calidad y espacios de la vivienda 
#con los datos del Censo 2020

##Borrar datos del entorno
rm(list=ls())

memory.limit(9999999999)


#Directorio
setwd("C:/Users/ALIENWARE/Documents/censo2020/")

##Crear folders de almacenamiento
dir.create("microdatos")

#Paquetería====
if(!require('pacman')) install.packages('pacman')
pacman::p_load(tidyverse, 
               sf,
               extrafont)

#Datos Censo. Lectura y filtos====
censo<-read.csv("microdatos/Personas00.csv")%>%
  janitor::clean_names()%>%
  #Condición para detectar a madres
  filter(sexo==3 & hijos_nac_vivos!=0 & edad>=15)%>%
  ##Agregar cero a entidad
  rename(cvegeo=ent)%>%
  mutate(cvegeo=ifelse(nchar(cvegeo)==1,
                    paste0("0",cvegeo),
                    cvegeo))%>%

          group_by(cvegeo)%>%
  summarise(factor=sum(factor))%>%
  ungroup()%>%
  #Calcular porcentaje
  mutate(pct=factor/sum(factor)*100)



##Shapefile====
#Entidad
ent<-st_read("conjunto_de_datos/00ent.shp")%>%
janitor::clean_names()%>%
  #Pegar datos de hacinamiento
  left_join(censo)


# Mapa====
ent%>%
ggplot() +
  # Capa con datos de los municipios
  geom_sf(data=ent,aes(fill = pct),
          colour = "#1C00ff00", size = 0.07) +
  
  # Agrega título, subtítulo y fuente
  labs(title = "Distribución de madres en México por entidad federativa, 2020",
       subtitle = paste0("% del total de mujeres 15 años y más con hijos nacidos vivos\n",
                         censo%>%summarise(format(round((sum(factor)/1000000),1),
                                            big.mark=",")), 
                         " millones de madres en nuestro país"),
       caption = "
Fuente: Elaborado por CANADEVI Nacional. Gerencia de Fondos de Vivienda. Coordinación de Indicadores de Vivienda 
con datos de INEGI. Censo de Población y Vivienda 2020.") +
  #Paleta y título de la leyenda
  scale_fill_distiller("%",
                       palette = "YlOrBr", direction = 1, limits=c(0,15))+
  theme_void(base_family="Century Gothic")+
  theme(plot.title = element_text(hjust = 0, size=30,face="bold"),
        plot.subtitle = element_text(hjust = 0, size=20, face="italic"),
        plot.caption = element_text(hjust = 0,size=15),
        legend.position="right",
        #Fuente y tamaño
        text=element_text(
                          size=20))


#Salvar
ggsave("mapamadresmex.png", height = 10,
       width = 20, units="in", dpi=300)