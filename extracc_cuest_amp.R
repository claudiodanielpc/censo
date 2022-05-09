#Código para descarga y extracción de los archivos del cuestionario ampliado del Censo 2020 utilizando Winrar

##Borrar datos del entorno
rm(list=ls())
#URL del Censo 2020
url<-"https://inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/Censo2020_CA_eum_csv.zip"

#Establecer directorio de trabajo y crear carpeta de extracción
raiz=setwd("D:/")
dir.create("censo",showWarnings = F)
directorio=paste0(raiz,"censo/")
setwd(directorio)

#Se establece que, si no existe el archivo viviendas, se descargue el zip de la URL de INEGI
if (!file.exists("Viviendas00.CSV")){
  download.file(url,destfile = "censo.zip",quiet = FALSE, mode="wb")
#Usaremos Winrar como opción para extracción
  winrar=shQuote("C:/Program Files/WinRAR/WinRAR")
  file="censo.zip"
  dest=directorio
  #Ejecución de la extracción
  cmd=paste(winrar, ' e ',file, ' -ir!*.*','"',dest,'"',sep='')
  system(cmd)
}
